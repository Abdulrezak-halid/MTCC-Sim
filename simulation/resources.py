from __future__ import annotations

from dataclasses import dataclass

import simpy


@dataclass
class CallCenterResources:
    ivr: simpy.Resource
    tier1: simpy.PriorityResource
    tier2: simpy.PriorityResource


def build_resources(env: simpy.Environment, ivr_agents: int, tier1_agents: int, tier2_agents: int) -> CallCenterResources:
    return CallCenterResources(
        ivr=simpy.Resource(env, capacity=ivr_agents),
        tier1=simpy.PriorityResource(env, capacity=tier1_agents),
        tier2=simpy.PriorityResource(env, capacity=tier2_agents),
    )
