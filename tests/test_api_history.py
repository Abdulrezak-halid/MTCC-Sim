from __future__ import annotations

import json
import unittest
from pathlib import Path

from api.main import RunSimulationRequest, get_run, list_runs, run_simulation

ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "contracts" / "simulation-output.schema.json"


class ApiHistoryTests(unittest.TestCase):
    def test_run_simulation_persists_history(self) -> None:
        response = run_simulation(
            RunSimulationRequest(scenario="normal_load", seed=101, replications=1, save_output=True)
        )

        self.assertIsNotNone(response.run_id)
        self.assertIsNotNone(response.output_path)
        self.assertGreaterEqual(len(response.comparison), 1)

        history = list_runs()
        self.assertGreaterEqual(len(history), 1)
        self.assertTrue(any(record.run_id == response.run_id for record in history))

        fetched = get_run(response.run_id)
        self.assertEqual(fetched["record"]["run_id"], response.run_id)
        self.assertIn("payload", fetched)
        self.assertEqual(fetched["payload"]["meta"]["run_id"], response.run_id)

    def test_run_record_structure(self) -> None:
        response = run_simulation(
            RunSimulationRequest(scenario="normal_load", seed=202, replications=1, save_output=True)
        )
        record = get_run(response.run_id)["record"]

        self.assertIn("base_seed", record)
        self.assertIn("scenario_count", record)
        self.assertIn("scenario_ids", record)
        self.assertIsInstance(record["scenario_ids"], list)


class SchemaShapeTests(unittest.TestCase):
    def test_exported_result_matches_schema_shape(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError as exc:  # pragma: no cover
            self.fail(f"jsonschema is required for this test: {exc}")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        payload_path = ROOT_DIR / "simulation" / "results" / "latest_results.json"
        payload = json.loads(payload_path.read_text(encoding="utf-8"))

        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(payload), key=lambda error: error.path)
        self.assertEqual([], errors, msg="\n".join(error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
