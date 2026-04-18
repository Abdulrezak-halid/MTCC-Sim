from __future__ import annotations

from environment import DistributionConfig, SimulationConfig


def _base_config() -> SimulationConfig:
    return SimulationConfig(
        scenario_id="normal_load",
        scenario_name="Normal Load",
        horizon_minutes=8 * 60,
        arrival_rate_per_minute=0.9,
        vip_ratio=0.12,
        tier1_agents=12,
        tier2_agents=5,
        ivr_agents=8,
        tier1_resolution_base=0.74,
        tier1_resolution_sensitivity=0.22,
        tier1_service=DistributionConfig(kind="exponential", mean=420.0, minimum=30.0),
        tier2_service=DistributionConfig(kind="normal", mean=620.0, std=120.0, minimum=45.0),
        patience=DistributionConfig(kind="normal", mean=360.0, std=90.0, minimum=25.0),
        ivr_service=DistributionConfig(kind="normal", mean=28.0, std=6.0, minimum=5.0),
        escalation_service_penalty=1.15,
        sla_seconds=60.0,
        timeseries_interval_seconds=60.0,
        replications=30,
    )


def scenario_catalog() -> dict[str, SimulationConfig]:
    base = _base_config()

    peak = SimulationConfig(
        **{
            **base.__dict__,
            "scenario_id": "peak_load",
            "scenario_name": "Peak Load",
            "arrival_rate_per_minute": base.arrival_rate_per_minute * 2.4,
        }
    )

    reduced_staff = SimulationConfig(
        **{
            **base.__dict__,
            "scenario_id": "reduced_staff",
            "scenario_name": "Reduced Staff",
            "tier1_agents": max(1, int(base.tier1_agents * 0.65)),
            "tier2_agents": max(1, int(base.tier2_agents * 0.6)),
        }
    )

    increased_vip = SimulationConfig(
        **{
            **base.__dict__,
            "scenario_id": "increased_vip_ratio",
            "scenario_name": "Increased VIP Ratio",
            "vip_ratio": 0.3,
        }
    )

    improved_efficiency = SimulationConfig(
        **{
            **base.__dict__,
            "scenario_id": "improved_staff_efficiency",
            "scenario_name": "Improved Staff Efficiency",
            "tier1_resolution_base": min(0.92, base.tier1_resolution_base + 0.1),
            "tier1_service": DistributionConfig(kind="exponential", mean=350.0, minimum=25.0),
            "tier2_service": DistributionConfig(kind="normal", mean=540.0, std=90.0, minimum=40.0),
        }
    )

    return {
        base.scenario_id: base,
        peak.scenario_id: peak,
        reduced_staff.scenario_id: reduced_staff,
        increased_vip.scenario_id: increased_vip,
        improved_efficiency.scenario_id: improved_efficiency,
    }
