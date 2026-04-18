from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[1]
SIMULATION_DIR = ROOT_DIR / "simulation"

if str(SIMULATION_DIR) not in sys.path:
    sys.path.insert(0, str(SIMULATION_DIR))

from run_simulation import run_scenarios  # noqa: E402
from scenarios import scenario_catalog  # noqa: E402

app = FastAPI(title="Call Center Simulation API", version="0.2.0")

DEFAULT_RESULTS_PATH = ROOT_DIR / "simulation" / "results" / "latest_results.json"
FALLBACK_RESULTS_PATH = ROOT_DIR / "simulation" / "simulation" / "results" / "latest_results.json"
ENV_RESULTS_KEY = "CALLCENTER_RESULTS_PATH"


class RunSimulationRequest(BaseModel):
    scenario: str | list[str] = Field(default="all", description="Scenario id, list of ids, or 'all'.")
    seed: int = Field(default=20260418, ge=0)
    replications: int | None = Field(default=None, ge=1)
    output_path: str | None = Field(default=None, description="Optional custom output path for JSON export.")
    save_output: bool = Field(default=True)


class RunSimulationResponse(BaseModel):
    meta: dict[str, Any]
    comparison: list[dict[str, Any]]
    output_path: str | None


def _normalize_scenarios(scenario_input: str | list[str]) -> list[str]:
    catalog = scenario_catalog()

    if isinstance(scenario_input, str):
        if scenario_input == "all":
            return list(catalog.keys())
        if scenario_input not in catalog:
            raise HTTPException(status_code=400, detail=f"Unknown scenario '{scenario_input}'.")
        return [scenario_input]

    unknown = [sid for sid in scenario_input if sid not in catalog]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown scenario ids: {', '.join(unknown)}")

    if not scenario_input:
        raise HTTPException(status_code=400, detail="Scenario list cannot be empty.")

    return scenario_input


def _resolve_results_path(override: str | None = None) -> Path:
    if override:
        path = Path(override)
        return path if path.is_absolute() else ROOT_DIR / path

    env_path = os.getenv(ENV_RESULTS_KEY)
    if env_path:
        env_file = Path(env_path)
        return env_file if env_file.is_absolute() else ROOT_DIR / env_file

    if DEFAULT_RESULTS_PATH.exists():
        return DEFAULT_RESULTS_PATH

    if FALLBACK_RESULTS_PATH.exists():
        return FALLBACK_RESULTS_PATH

    return DEFAULT_RESULTS_PATH


def _read_exported_payload(path_override: str | None = None) -> tuple[dict[str, Any], Path]:
    results_path = _resolve_results_path(path_override)

    if not results_path.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                "No simulation output file found. Run /run-simulation first or provide CALLCENTER_RESULTS_PATH."
            ),
        )

    try:
        payload = json.loads(results_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in results file: {exc}") from exc

    return payload, results_path


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run-simulation", response_model=RunSimulationResponse)
def run_simulation(request: RunSimulationRequest) -> RunSimulationResponse:
    scenario_ids = _normalize_scenarios(request.scenario)
    payload = run_scenarios(
        scenario_ids=scenario_ids,
        base_seed=request.seed,
        replications=request.replications,
    )

    output_path: str | None = None
    if request.save_output:
        resolved_output = _resolve_results_path(request.output_path)
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        resolved_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        output_path = str(resolved_output)

    return RunSimulationResponse(meta=payload["meta"], comparison=payload["comparison"], output_path=output_path)


@app.get("/compare-scenarios")
def compare_scenarios(results_path: str | None = Query(default=None)) -> dict[str, Any]:
    payload, source_path = _read_exported_payload(results_path)
    return {
        "meta": payload.get("meta", {}),
        "comparison": payload.get("comparison", []),
        "source_path": str(source_path),
    }


@app.get("/get-metrics")
def get_metrics(
    scenario_id: str | None = Query(default=None, description="Optional scenario id filter."),
    results_path: str | None = Query(default=None),
) -> dict[str, Any]:
    payload, source_path = _read_exported_payload(results_path)
    scenarios = payload.get("scenarios", [])

    if scenario_id is None:
        return {
            "meta": payload.get("meta", {}),
            "scenario_count": len(scenarios),
            "aggregates": [
                {
                    "scenario_id": scenario.get("scenario", {}).get("scenario_id"),
                    "scenario_name": scenario.get("scenario", {}).get("name"),
                    "kpis": scenario.get("aggregates", {}).get("kpis", {}),
                    "confidence_intervals_95": scenario.get("aggregates", {}).get(
                        "confidence_intervals_95", {}
                    ),
                }
                for scenario in scenarios
            ],
            "source_path": str(source_path),
        }

    selected = [s for s in scenarios if s.get("scenario", {}).get("scenario_id") == scenario_id]
    if not selected:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found in exported results.")

    scenario = selected[0]
    return {
        "meta": payload.get("meta", {}),
        "scenario": scenario.get("scenario", {}),
        "aggregates": scenario.get("aggregates", {}),
        "replication_count": len(scenario.get("replications", [])),
        "source_path": str(source_path),
    }
