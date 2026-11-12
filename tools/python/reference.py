"""Generate the GitHub-readable reference from the canonical OpenAPI documents."""

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def type_name(schema):
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[1]
    if "allOf" in schema:
        return " & ".join(type_name(s) for s in schema["allOf"])
    if "oneOf" in schema:
        return " or ".join(type_name(s) for s in schema["oneOf"])
    if schema.get("type") == "array":
        return f"array<{type_name(schema.get('items', {}))}>"
    if schema.get("type") == "object" and not schema.get("properties"):
        return f"map<string, {type_name(schema.get('additionalProperties', {}))}>"
    value = schema.get("type", "source JSON")
    return value + (" or null" if schema.get("nullable") else "")


def render(name, spec):
    lines = [
        f"# IPMA {name}: upstream HTTP reference",
        "",
        "Generated from the canonical specification; do not edit this document directly.",
        "",
        "[OpenAPI YAML](openapi.yaml) · [Capture provenance](fixtures/manifest.json)",
        "",
        spec["info"]["description"],
        "",
        f"Base URL: `{spec['servers'][0]['url']}`",
        "",
        f"Verified: {spec['x-last-verified']} · Evidence: [{spec['x-source-status']}]({spec['externalDocs']['url']})",
        "",
        "## Operations",
        "",
        "| Operation | HTTP path |",
        "| --- | --- |",
    ]
    for path, item in spec["paths"].items():
        lines.append(f"| `{item['get']['operationId']}` | `GET {path}` |")
    for path, item in spec["paths"].items():
        op = item["get"]
        lines += [
            "",
            f"## {op['operationId']}",
            "",
            op["summary"],
            "",
            f"`GET {path}`",
            "",
            op["description"],
            "",
        ]
        for parameter in op.get("parameters", []):
            schema = parameter["schema"]
            limits = {
                key: schema[key]
                for key in ("minimum", "maximum", "enum")
                if key in schema
            }
            lines += [
                f"- `{parameter['name']}`: {parameter['description']} Example: `{schema['example']}`. Constraints: `{limits}`."
            ]
        content = op["responses"]["200"]["content"]
        media = next(iter(content))
        lines += [
            "",
            f"Success: **200**, `{media}`, `{type_name(content[media]['schema'])}`.",
            "",
            f"[Captured response]({op['x-captured-fixture']}) · [Source evidence]({op['x-evidence']['url']})",
            "",
            "HTTP 4xx/5xx bodies have no guaranteed JSON schema. Other statuses are unexpected responses.",
        ]
        if "x-reference-discrepancy" in op:
            lines += [
                "",
                "**Reference discrepancy:** " + op["x-reference-discrepancy"],
                "",
                "Published path: `" + op["x-published-path"] + "`.",
            ]
        if "x-csv-columns" in op:
            lines += [
                "",
                "CSV is returned as raw bytes. Columns and units:",
                "",
                "| Column | Meaning |",
                "| --- | --- |",
            ]
            lines += [
                f"| `{key}` | {cell(description)} |"
                for key, description in op["x-csv-columns"].items()
            ]
    lines += [
        "",
        "## Schemas",
        "",
        "Unknown source fields are accepted and preserved in generated `extra` maps. Optional known null fields deserialize, but generated `Option` fields collapse null and omission; retain the original response bytes if that distinction matters.",
    ]
    for key, schema in spec["components"]["schemas"].items():
        lines += [
            "",
            f"### {key}",
            "",
            schema.get("description", ""),
            "",
            f"Shape: `{type_name(schema)}`.",
        ]
        if "properties" in schema:
            lines += [
                "",
                "| Source field | Type | Required | Meaning |",
                "| --- | --- | --- | --- |",
            ]
            for field, field_schema in schema["properties"].items():
                required = "yes" if field in schema.get("required", []) else "no"
                lines.append(
                    f"| `{field}` | {cell(type_name(field_schema))} | {required} | {cell(field_schema.get('description', ''))} |"
                )
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name in ("open-data", "public-data"):
        spec = yaml.safe_load((ROOT / f"{name}/openapi.yaml").read_text())
        output = ROOT / f"{name}/reference.md"
        source = render(name, spec)
        if args.check:
            if output.read_text() != source:
                raise SystemExit(
                    f"{output} is stale; run just generate from the repository root"
                )
        else:
            output.write_text(source)
        print(f"{'verified' if args.check else 'generated'} {name} reference")


if __name__ == "__main__":
    main()
