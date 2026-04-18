from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import simpy

from environment import RandomStreams, SimulationConfig
from metrics import MetricsCollector, summarize_replications
from processes import arrivals_process, timeseries_sampler
from resources import build_resources
from scenarios import scenario_catalog


ENGINE_VERSION = "0.1.0"


def _build_replication_payload(
    replication_id: int,
    seed: int,
    metrics: MetricsCollector,
) -> dict[str, Any]:
    return {
        "replication_id": replication_id,
        "seed": seed,
        "kpis": metrics.to_kpis(),
    }


def run_replication(config: SimulationConfig, seed: int, replication_id: int) -> tuple[dict[str, Any], dict[str, Any]]:
    env = simpy.Environment()
    streams = RandomStreams(seed)
    resources = build_resources(
        env=env,
        ivr_agents=config.ivr_agents,
        tier1_agents=config.tier1_agents,
        tier2_agents=config.tier2_agents,
    )
    metrics = MetricsCollector(config=config)
    active_calls: set[int] = set()

    env.process(arrivals_process(env, resources, config, streams, metrics, active_calls))
    env.process(timeseries_sampler(env, resources, config, metrics))

    horizon_seconds = config.horizon_minutes * 60.0
    env.run(until=horizon_seconds)

    metrics.set_calls_in_system_end(len(active_calls))

    replication_payload = _build_replication_payload(replication_id=replication_id, seed=seed, metrics=metrics)
    return replication_payload, metrics.to_timeseries()


def run_scenario(config: SimulationConfig, base_seed: int, replications: int | None = None) -> dict[str, Any]:
    run_replications = replications if replications is not None else config.replications
    all_replications: list[dict[str, Any]] = []
    representative_timeseries: dict[str, Any] = {}

    for replication_id in range(1, run_replications + 1):
        seed = base_seed + (replication_id * 101)
        rep_payload, timeseries = run_replication(config=config, seed=seed, replication_id=replication_id)
        all_replications.append(rep_payload)
        if replication_id == 1:
            representative_timeseries = timeseries

    aggregated = summarize_replications(all_replications)

    return {
        "meta": {
            "run_id": f"{config.scenario_id}-{base_seed}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": ENGINE_VERSION,
            "random_seed_policy": "deterministic_sequence",
        },
        "scenario": {
            "scenario_id": config.scenario_id,
            "name": config.scenario_name,
            "parameters": asdict(config),
        },
        "replications": all_replications,
        "aggregates": aggregated,
        "timeseries": representative_timeseries,
    }


def run_scenarios(scenario_ids: list[str], base_seed: int, replications: int | None = None) -> dict[str, Any]:
    catalog = scenario_catalog()
    selected = [catalog[sid] for sid in scenario_ids]

    scenario_results = [run_scenario(config=sc, base_seed=base_seed, replications=replications) for sc in selected]

    summary_rows: list[dict[str, Any]] = []
    for result in scenario_results:
        kpis = result["aggregates"]["kpis"]
        summary_rows.append(
            {
                "scenario_id": result["scenario"]["scenario_id"],
                "scenario_name": result["scenario"]["name"],
                "avg_wait_seconds": kpis.get("avg_wait_seconds", 0.0),
                "abandonment_rate": kpis.get("abandonment_rate", 0.0),
                "sla_compliance_rate": kpis.get("sla_compliance_rate", 0.0),
                "utilization_tier1": kpis.get("utilization_tier1", 0.0),
                "utilization_tier2": kpis.get("utilization_tier2", 0.0),
            }
        )

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": ENGINE_VERSION,
            "base_seed": base_seed,
            "scenario_count": len(summary_rows),
        },
        "scenarios": scenario_results,
        "comparison": summary_rows,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-tier call center simulation scenarios.")
    parser.add_argument(
        "--scenario",
        type=str,
        default="all",
        help="Scenario id from catalog or 'all'.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260418,
        help="Base random seed.",
    )
    parser.add_argument(
        "--replications",
        type=int,
        default=None,
        help="Override replication count per scenario.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="simulation/results/latest_results.json",
        help="Output JSON file path.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    catalog = scenario_catalog()

    if args.scenario == "all":
        scenario_ids = list(catalog.keys())
    elif args.scenario in catalog:
        scenario_ids = [args.scenario]
    else:
        valid = ", ".join(catalog.keys())
        raise ValueError(f"Unknown scenario '{args.scenario}'. Valid values: all, {valid}")

    payload = run_scenarios(scenario_ids=scenario_ids, base_seed=args.seed, replications=args.replications)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Saved simulation results to {output_path}")


if __name__ == "__main__":
    main()
