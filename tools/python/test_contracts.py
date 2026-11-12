import copy
import tempfile
import unittest
from pathlib import Path

from jsonschema import ValidationError

from contracts import (
    ROOT,
    capture,
    compare,
    load_report,
    read_specs,
    response_schema,
    sample,
    unknown_fields,
    validate_fixtures,
    validate_response,
)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs = read_specs()

    def test_nullable_numeric_variants_and_future_fields_are_valid(self):
        spec = self.specs["public-data"]
        for number in (None, 0, -2.5, "0", "-99.0", "", " 2.5e1 "):
            import json

            body = json.dumps(
                [
                    {
                        "globalIdLocal": 1110600,
                        "dataPrev": "2026-11-12T10:00:00",
                        "idPeriodo": 777,
                        "tMed": number,
                        "future": True,
                    }
                ]
            ).encode()
            validate_response(spec, "get_forecast", body)
        _, _, _, schema = response_schema(spec, "get_forecast")
        self.assertEqual(
            unknown_fields(spec, schema, [{"future": True}]), ["$[].future: boolean"]
        )

    def test_shape_and_known_type_drift_are_rejected(self):
        spec = self.specs["public-data"]
        for body in (
            b"{}",
            b'[{"globalIdLocal":1110600}]',
            b'[{"globalIdLocal":1110600,"dataPrev":"x","tMed":"rain"}]',
            b'[{"globalIdLocal":1110600,"dataPrev":"x","tMed":true}]',
        ):
            with self.assertRaises(ValidationError):
                validate_response(spec, "get_forecast", body)

    def test_public_and_open_warning_envelopes_remain_separate(self):
        with self.assertRaises(ValidationError):
            validate_response(self.specs["public-data"], "get_warnings", b"[]")
        with self.assertRaises(ValidationError):
            validate_response(self.specs["open-data"], "get_warnings", b'{"data":[]}')
        validate_response(self.specs["public-data"], "get_warnings", b'{"data":[]}')
        validate_response(self.specs["open-data"], "get_warnings", b"[]")

    def test_dynamic_timestamp_and_station_keys_are_not_unknown_fields(self):
        spec = self.specs["open-data"]
        _, _, _, schema = response_schema(spec, "get_observations")
        value = {
            "2026-11-12T10:00": {
                "1200535": None,
                "1200536": {"temperatura": 0, "future": 1},
            }
        }
        self.assertEqual(unknown_fields(spec, schema, value), ["$.*.*.future: number"])

    def test_sampling_retains_distinct_record_shapes_and_numeric_types(self):
        values = [
            {"x": "1"},
            {"x": "2"},
            {"x": "3"},
            {"x": 1},
            {"x": None},
            {"x": "4", "future": True},
        ]
        self.assertEqual(len(sample(values)), 5)

    def test_climate_contract_rejects_missing_columns_and_nonnumeric_measurements(self):
        import csv
        import io

        spec = self.specs["open-data"]
        _, op, _, _ = response_schema(spec, "get_climate_temperature")
        columns = list(op["x-csv-columns"])

        def encode(values):
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(columns)
            writer.writerow(values)
            return output.getvalue().encode()

        values = ["2026-11-12 00:00:00+00:00", "Lisboa", "1106"] + ["-99"] * (
            len(columns) - 3
        )
        validate_response(spec, "get_climate_temperature", encode(values))
        values[-1] = "cloudy"
        with self.assertRaises(ValueError):
            validate_response(spec, "get_climate_temperature", encode(values))
        with self.assertRaises(ValueError):
            validate_response(spec, "get_climate_temperature", b"time,zid\nx,1106\n")

    def test_capture_roundtrips_independent_api_fixture_manifests(self):
        from unittest.mock import patch

        report = load_report(ROOT)
        responses = {
            record["url"]: (
                (ROOT / record["file"]).read_bytes(),
                record["content_type"],
                record["status"],
            )
            for record in report["records"]
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate"
            with patch(
                "contracts.fetch", side_effect=lambda url: responses[url]
            ) as fetch:
                capture(self.specs, output)
                self.assertEqual(fetch.call_count, 24)
            validate_fixtures(self.specs, output)
            # The API-local manifests also work without the combined probe report.
            (output / "manifest.json").unlink()
            validate_fixtures(self.specs, output)
            compare(ROOT, output)
            for name, count in [("open-data", 20), ("public-data", 4)]:
                local = load_report(output, [name])
                self.assertEqual(len(local["records"]), count)
                self.assertTrue(
                    all(record["api"] == name for record in local["records"])
                )

    def test_probe_reports_added_fields_without_silently_rewriting_baseline(self):
        import json

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "old"
            new = root / "new"
            old.mkdir()
            new.mkdir()
            record = {
                "api": "public-data",
                "operation": "get_forecast",
                "observed_additional_fields": [],
            }
            baseline = json.dumps({"records": [record], "failures": []})
            (old / "manifest.json").write_text(baseline)
            updated = copy.deepcopy(record)
            updated["observed_additional_fields"] = ["$[].future: boolean"]
            (new / "manifest.json").write_text(
                json.dumps({"records": [updated], "failures": []})
            )
            with self.assertRaises(ValueError):
                compare(old, new)
            self.assertEqual((old / "manifest.json").read_text(), baseline)
            self.assertTrue((new / "drift.json").exists())


if __name__ == "__main__":
    unittest.main()
