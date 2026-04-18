from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Any

import simpy

from environment import SimulationConfig
from entities import Call, CustomerType
from resources import CallCenterResources


@dataclass
class MetricsCollector:
    config: SimulationConfig
    calls_arrived: int = 0
    calls_answered: int = 0
    calls_abandoned: int = 0
    calls_resolved_tier1: int = 0
    calls_escalated: int = 0
    calls_completed: int = 0
    calls_in_system_end: int = 0

    wait_times_seconds: list[float] = field(default_factory=list)
    tier1_service_seconds: list[float] = field(default_factory=list)
    tier2_service_seconds: list[float] = field(default_factory=list)

    vip_wait_times_seconds: list[float] = field(default_factory=list)
    normal_wait_times_seconds: list[float] = field(default_factory=list)

    answered_within_sla: int = 0
    tier1_busy_seconds: float = 0.0
    tier2_busy_seconds: float = 0.0

    queue_series: list[dict[str, float]] = field(default_factory=list)
    utilization_series: list[dict[str, float]] = field(default_factory=list)
    throughput_series: list[dict[str, float]] = field(default_factory=list)

    def record_arrival(self) -> None:
        self.calls_arrived += 1

    def record_answered(self, call: Call) -> None:
        if call.queue_enter_time_seconds is None or call.tier1_start_time_seconds is None:
            return
        wait = max(0.0, call.tier1_start_time_seconds - call.queue_enter_time_seconds)
        self.calls_answered += 1
        self.wait_times_seconds.append(wait)

        if call.customer_type == CustomerType.VIP:
            self.vip_wait_times_seconds.append(wait)
        else:
            self.normal_wait_times_seconds.append(wait)

        if wait <= self.config.sla_seconds:
            self.answered_within_sla += 1

    def record_tier1_service(self, duration_seconds: float) -> None:
        self.tier1_service_seconds.append(max(0.0, duration_seconds))
        self.tier1_busy_seconds += max(0.0, duration_seconds)

    def record_tier2_service(self, duration_seconds: float) -> None:
        self.tier2_service_seconds.append(max(0.0, duration_seconds))
        self.tier2_busy_seconds += max(0.0, duration_seconds)

    def record_escalation(self) -> None:
        self.calls_escalated += 1

    def record_resolved_tier1(self) -> None:
        self.calls_resolved_tier1 += 1

    def record_completed(self) -> None:
        self.calls_completed += 1

    def record_abandoned(self) -> None:
        self.calls_abandoned += 1

    def set_calls_in_system_end(self, value: int) -> None:
        self.calls_in_system_end = max(0, value)

    def observe_timeseries(self, env: simpy.Environment, resources: CallCenterResources) -> None:
        t = float(env.now)
        self.queue_series.append(
            {
                "t": t,
                "tier1": float(len(resources.tier1.queue)),
                "tier2": float(len(resources.tier2.queue)),
                "vip_queue": float(sum(1 for req in resources.tier1.queue if req.priority == 0)),
                "normal_queue": float(sum(1 for req in resources.tier1.queue if req.priority > 0)),
            }
        )
        self.utilization_series.append(
            {
                "t": t,
                "tier1": float(resources.tier1.count / resources.tier1.capacity),
                "tier2": float(resources.tier2.count / resources.tier2.capacity),
            }
        )
        self.throughput_series.append(
            {
                "t": t,
                "answered_cumulative": float(self.calls_answered),
                "abandoned_cumulative": float(self.calls_abandoned),
            }
        )

    def to_kpis(self) -> dict[str, float]:
        answered = max(1, self.calls_answered)
        horizon_seconds = max(1.0, self.config.horizon_minutes * 60.0)

        return {
            "calls_arrived": float(self.calls_arrived),
            "calls_answered": float(self.calls_answered),
            "calls_abandoned": float(self.calls_abandoned),
            "calls_completed": float(self.calls_completed),
            "calls_escalated": float(self.calls_escalated),
            "calls_in_system_end": float(self.calls_in_system_end),
            "avg_wait_seconds": mean(self.wait_times_seconds) if self.wait_times_seconds else 0.0,
            "avg_service_seconds_tier1": mean(self.tier1_service_seconds) if self.tier1_service_seconds else 0.0,
            "avg_service_seconds_tier2": mean(self.tier2_service_seconds) if self.tier2_service_seconds else 0.0,
            "abandonment_rate": self.calls_abandoned / max(1, self.calls_arrived),
            "sla_compliance_rate": self.answered_within_sla / answered,
            "utilization_tier1": min(1.0, self.tier1_busy_seconds / (horizon_seconds * self.config.tier1_agents)),
            "utilization_tier2": min(1.0, self.tier2_busy_seconds / (horizon_seconds * self.config.tier2_agents)),
            "avg_wait_seconds_vip": mean(self.vip_wait_times_seconds) if self.vip_wait_times_seconds else 0.0,
            "avg_wait_seconds_normal": mean(self.normal_wait_times_seconds) if self.normal_wait_times_seconds else 0.0,
        }

    def to_timeseries(self) -> dict[str, list[dict[str, float]]]:
        return {
            "queue_length": self.queue_series,
            "utilization": self.utilization_series,
            "throughput": self.throughput_series,
        }


def summarize_replications(replications: list[dict[str, Any]]) -> dict[str, Any]:
    if not replications:
        return {"kpis": {}, "confidence_intervals_95": {}}

    metric_names = list(replications[0]["kpis"].keys())
    sample_count = len(replications)

    kpi_means: dict[str, float] = {}
    ci: dict[str, dict[str, float]] = {}

    for metric in metric_names:
        values = [float(rep["kpis"][metric]) for rep in replications]
        avg = mean(values)
        kpi_means[metric] = avg

        if sample_count == 1:
            ci[metric] = {"mean": avg, "lower": avg, "upper": avg}
            continue

        m = avg
        variance = sum((v - m) ** 2 for v in values) / (sample_count - 1)
        std = variance ** 0.5
        margin = 1.96 * std / (sample_count ** 0.5)
        ci[metric] = {"mean": avg, "lower": avg - margin, "upper": avg + margin}

    return {"kpis": kpi_means, "confidence_intervals_95": ci}
