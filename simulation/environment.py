from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

DistributionKind = Literal["exponential", "normal", "uniform"]


@dataclass(frozen=True)
class DistributionConfig:
    kind: DistributionKind
    mean: float
    std: float = 0.0
    minimum: float = 0.01


@dataclass(frozen=True)
class SimulationConfig:
    scenario_id: str
    scenario_name: str
    horizon_minutes: float
    arrival_rate_per_minute: float
    vip_ratio: float
    tier1_agents: int
    tier2_agents: int
    ivr_agents: int
    tier1_resolution_base: float
    tier1_resolution_sensitivity: float
    tier1_service: DistributionConfig
    tier2_service: DistributionConfig
    patience: DistributionConfig
    ivr_service: DistributionConfig
    escalation_service_penalty: float
    sla_seconds: float
    timeseries_interval_seconds: float
    replications: int


class RandomStreams:
    def __init__(self, seed: int) -> None:
        self._rng = np.random.default_rng(seed)

    def random(self) -> float:
        return float(self._rng.random())

    def poisson_interval_minutes(self, rate_per_minute: float) -> float:
        if rate_per_minute <= 0:
            return float("inf")
        return float(self._rng.exponential(1.0 / rate_per_minute))

    def sample_distribution(self, config: DistributionConfig) -> float:
        if config.kind == "exponential":
            value = self._rng.exponential(config.mean)
        elif config.kind == "normal":
            value = self._rng.normal(config.mean, config.std)
        elif config.kind == "uniform":
            low = max(config.minimum, config.mean - config.std)
            high = max(low + 1e-6, config.mean + config.std)
            value = self._rng.uniform(low, high)
        else:
            raise ValueError(f"Unsupported distribution kind: {config.kind}")

        return float(max(config.minimum, value))
