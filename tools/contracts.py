"""Reviewable upstream contracts: validate approved samples or explicitly probe IPMA."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import yaml
from jsonschema import ValidationError
from openapi_schema_validator import OAS30Validator
from openapi_spec_validator import validate as validate_spec
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT4

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 32 * 1024 * 1024


def read_specs():
    return {
        name: yaml.safe_load((ROOT / f"specs/{name}.yaml").read_text())
        for name in ("open-data", "public-data")
    }


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def response_schema(spec, operation):
    for path, item in spec["paths"].items():
        op = item["get"]
        if op["operationId"] == operation:
            content = op["responses"]["200"]["content"]
            media = next(iter(content))
            return path, op, media, content[media]["schema"]
    raise ValueError(f"Unknown operation {operation}")


def json_body(body):
    def nonfinite(value):
        raise ValueError(f"non-finite JSON value: {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"non-finite JSON number: {value}")
        return number

    return json.loads(body, parse_constant=nonfinite, parse_float=finite_float)


def validate_response(spec, operation, body):
    path, op, media, _schema = response_schema(spec, operation)
    if media.endswith("json") or op.get("x-body-encoding") == "json":
        value = json_body(body)
        uri = "urn:ipma:contract"
        registry = Registry().with_resource(
            uri, Resource.from_contents(spec, default_specification=DRAFT4)
        )
        pointer = path.replace("~", "~0").replace("/", "~1")
        media_pointer = media.replace("/", "~1")
        target = (
            f"{uri}#/paths/{pointer}/get/responses/200/content/{media_pointer}/schema"
        )
        OAS30Validator({"$ref": target}, registry=registry).validate(value)
        return value
    if media == "text/csv":
        rows = list(csv.DictReader(io.StringIO(body.decode("utf-8-sig"))))
        columns = next(csv.reader(io.StringIO(body.decode("utf-8-sig"))))
        columns = [c.strip() for c in columns]
        expected = op["x-csv-columns"]
        missing = set(expected) - set(columns)
        if missing:
            raise ValueError(f"{operation}: missing CSV columns {sorted(missing)}")
        if not rows:
            raise ValueError(f"{operation}: expected at least one CSV data row")
        for row in rows:
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"{operation}: malformed CSV row")
            for column, raw in row.items():
                if column.strip() not in expected or column.strip() in {
                    "time",
                    "zname",
                    "zid",
                }:
                    continue
                if raw.strip() and not math.isfinite(float(raw)):
                    raise ValueError(
                        f"{operation}: non-finite CSV measurement in {column}"
                    )
        return None
    if media == "application/zip":
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            if not archive.namelist() or archive.testzip() is not None:
                raise ValueError("empty or corrupt icon archive")
        return None
    raise ValueError(f"Unsupported media type {media}")


def resolve(spec, schema):
    while "$ref" in schema:
        schema = spec["components"]["schemas"][schema["$ref"].rsplit("/", 1)[1]]
    return schema


def value_type(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, str):
        return "string"
    if isinstance(v, (int, float)):
        return "number"
    if isinstance(v, list):
        return "array"
    return "object"


def unknown_fields(spec, schema, value, path="$", found=None):
    """Report additive shape drift without rejecting unknown fields at runtime."""
    found = set() if found is None else found
    schema = resolve(spec, schema)
    for branch in schema.get("allOf", []):
        unknown_fields(spec, branch, value, path, found)
    if isinstance(value, dict):
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", {})
        for key, child in value.items():
            if key in props:
                unknown_fields(spec, props[key], child, f"{path}.{key}", found)
            elif props:
                found.add(f"{path}.{key}: {value_type(child)}")
            elif isinstance(extra, dict) and extra:
                unknown_fields(spec, extra, child, f"{path}.*", found)
    elif isinstance(value, list):
        for child in value:
            unknown_fields(spec, schema.get("items", {}), child, f"{path}[]", found)
    return sorted(found)


def sample(value):
    """Small structural samples, never regenerated into the spec automatically."""
    if isinstance(value, list):
        # Keep representatives of every key/type combination, not just the first row.
        seen, result = set(), []
        for row in value:
            shape = (
                tuple(sorted((k, value_type(v)) for k, v in row.items()))
                if isinstance(row, dict)
                else value_type(row)
            )
            if shape not in seen or len(result) < 2:
                seen.add(shape)
                result.append(row)
        return result
    if isinstance(value, dict):
        if "features" in value:
            return {
                **value,
                "features": sorted(
                    value["features"], key=lambda feature: len(json.dumps(feature))
                )[:2],
            }
        if "data" in value and isinstance(value["data"], list):
            return {**value, "data": sample(value["data"])}
        if "local" in value and isinstance(value["local"], dict):
            return {**value, "local": dict(list(value["local"].items())[:2])}
        if value and all(isinstance(v, dict) for v in value.values()):
            return {
                time: dict(list(stations.items())[:4])
                for time, stations in list(value.items())[:2]
            }
    return value


def sample_csv(body):
    rows = csv.reader(io.StringIO(body.decode("utf-8-sig")))
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    for _ in range(3):
        row = next(rows, None)
        if row is None:
            break
        writer.writerow(row)
    return output.getvalue().encode()


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ipma-openapi-contract-review/0.1",
            "Accept-Encoding": "identity",
        },
    )

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None

    with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
        body = response.read(LIMIT + 1)
        if len(body) > LIMIT:
            raise ValueError(f"{url}: response exceeds 32 MiB")
        return body, response.headers.get("Content-Type", ""), response.status


def capture(specs, output):
    if output.exists():
        raise ValueError(f"{output} already exists; choose a new review directory")
    output.mkdir(parents=True)
    records = []
    failures = []
    for name, spec in specs.items():
        (output / name).mkdir()
        for path, item in spec["paths"].items():
            op = item["get"]
            actual = path
            for param in op.get("parameters", []):
                actual = actual.replace(
                    "{" + param["name"] + "}", str(param["schema"]["example"])
                )
            url = spec["servers"][0]["url"] + actual
            operation = op["operationId"]
            try:
                body, content_type, status = fetch(url)
                value = validate_response(spec, operation, body)
                _, _, media, schema = response_schema(spec, operation)
                unknown = (
                    unknown_fields(spec, schema, value)
                    if value is not None
                    else [
                        f"CSV.{column}: string"
                        for column in next(
                            csv.reader(io.StringIO(body.decode("utf-8-sig")))
                        )
                        if column.strip() not in op["x-csv-columns"]
                    ]
                    if media == "text/csv"
                    else []
                )
                extension = (
                    "json"
                    if value is not None
                    else "csv"
                    if media == "text/csv"
                    else "zip"
                )
                stored = (
                    (
                        json.dumps(sample(value), ensure_ascii=False, indent=2) + "\n"
                    ).encode()
                    if value is not None
                    else sample_csv(body)
                    if media == "text/csv"
                    else body
                )
                file = f"{name}/{operation}.{extension}"
                (output / file).write_bytes(stored)
                records.append(
                    {
                        "api": name,
                        "operation": operation,
                        "file": file,
                        "url": url,
                        "status": status,
                        "content_type": content_type,
                        "captured_at": dt.datetime.now(dt.UTC).isoformat(),
                        "response_bytes": len(body),
                        "response_sha256": digest(body),
                        "fixture_sha256": digest(stored),
                        "sampled": value is not None or media == "text/csv",
                        "sampling": "structural-source-sample"
                        if value is not None
                        else "csv-header-and-two-rows"
                        if media == "text/csv"
                        else "complete-archive",
                        "observed_additional_fields": unknown,
                    }
                )
                print(f"PASS {name}/{operation} ({len(body)} bytes)", flush=True)
            except (
                ValueError,
                OSError,
                ValidationError,
                yaml.YAMLError,
                zipfile.BadZipFile,
            ) as error:
                failures.append(
                    {
                        "api": name,
                        "operation": operation,
                        "url": url,
                        "error": str(error),
                    }
                )
                print(f"FAIL {name}/{operation}: {error}", flush=True)
    report = {"records": records, "failures": failures}
    (output / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    return report


def validate_fixtures(specs, directory):
    report = json.loads((directory / "manifest.json").read_text())
    if report.get("failures"):
        raise ValueError("approved fixture manifest contains failed probes")
    seen = set()
    for record in report["records"]:
        body = (directory / record["file"]).read_bytes()
        if digest(body) != record["fixture_sha256"]:
            raise ValueError(f"fixture hash mismatch: {record['file']}")
        validate_response(specs[record["api"]], record["operation"], body)
        seen.add((record["api"], record["operation"]))
    expected = {
        (name, item["get"]["operationId"])
        for name, spec in specs.items()
        for item in spec["paths"].values()
    }
    if seen != expected:
        raise ValueError(
            f"fixture coverage mismatch: missing {expected - seen}, extra {seen - expected}"
        )
    print(f"PASS {len(seen)} operation fixtures")


def compare(baseline, candidate):
    old = json.loads((baseline / "manifest.json").read_text())
    new = json.loads((candidate / "manifest.json").read_text())
    before = {
        (r["api"], r["operation"]): set(r["observed_additional_fields"])
        for r in old["records"]
    }
    drift = []
    for row in new["records"]:
        for field in set(row["observed_additional_fields"]) - before.get(
            (row["api"], row["operation"]), set()
        ):
            drift.append(f"{row['api']}/{row['operation']}: {field}")
    (candidate / "drift.json").write_text(
        json.dumps(
            {"new_additional_fields": sorted(drift), "failures": new["failures"]},
            indent=2,
        )
        + "\n"
    )
    if new["failures"]:
        raise ValueError(f"Probe failures require review: {candidate}/manifest.json")
    if drift:
        raise ValueError(
            "New source fields require review:\n" + "\n".join(sorted(drift))
        )
    print(
        "PASS no new unmodeled fields in this probe; optional-field removal cannot be established from finite samples"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "capture", "probe"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    specs = read_specs()
    for name, spec in specs.items():
        validate_spec(spec)
        print(f"PASS {name} OpenAPI 3.0.3 specification", flush=True)
    if args.command == "validate":
        validate_fixtures(specs, ROOT / "fixtures")
    else:
        output = args.output or ROOT / ".artifacts" / dt.datetime.now(dt.UTC).strftime(
            "probe-%Y%m%dT%H%M%SZ"
        )
        report = capture(specs, output)
        if args.command == "probe":
            compare(ROOT / "fixtures", output)
        elif report["failures"]:
            raise ValueError(f"Probe failures require review: {output}/manifest.json")
        print(f"Review output: {output}")


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        OSError,
        ValidationError,
        yaml.YAMLError,
        zipfile.BadZipFile,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
