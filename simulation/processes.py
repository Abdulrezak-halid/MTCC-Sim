from __future__ import annotations

import simpy

from entities import Call, CustomerType
from environment import RandomStreams, SimulationConfig
from metrics import MetricsCollector
from resources import CallCenterResources


def _priority_for(call: Call) -> int:
    return 0 if call.customer_type == CustomerType.VIP else 1


def _dynamic_tier1_resolution_probability(config: SimulationConfig, resources: CallCenterResources) -> float:
    pressure = len(resources.tier1.queue) / max(1, resources.tier1.capacity)
    pressure_factor = min(1.0, pressure / 3.0)
    probability = config.tier1_resolution_base - (config.tier1_resolution_sensitivity * pressure_factor)
    return max(0.05, min(0.95, probability))


def _create_call(call_id: int, now_seconds: float, config: SimulationConfig, streams: RandomStreams) -> Call:
    customer_type = CustomerType.VIP if streams.random() < config.vip_ratio else CustomerType.NORMAL
    return Call(
        call_id=call_id,
        customer_type=customer_type,
        arrival_time_seconds=now_seconds,
        patience_seconds=streams.sample_distribution(config.patience),
        ivr_duration_seconds=streams.sample_distribution(config.ivr_service),
        tier1_service_seconds=streams.sample_distribution(config.tier1_service),
        tier2_service_seconds=streams.sample_distribution(config.tier2_service) * config.escalation_service_penalty,
    )


def handle_call(
    env: simpy.Environment,
    call: Call,
    resources: CallCenterResources,
    config: SimulationConfig,
    streams: RandomStreams,
    metrics: MetricsCollector,
    active_calls: set[int],
) -> simpy.Process: # type: ignore
    active_calls.add(call.call_id)

    with resources.ivr.request() as ivr_req:
        yield ivr_req
        yield env.timeout(call.ivr_duration_seconds)

    call.queue_enter_time_seconds = float(env.now)
    tier1_req = resources.tier1.request(priority=_priority_for(call))
    patience_timeout = env.timeout(call.patience_seconds)
    tier1_result = yield tier1_req | patience_timeout

    if tier1_req not in tier1_result:
        call.abandoned_time_seconds = float(env.now)
        tier1_req.cancel()
        metrics.record_abandoned()
        active_calls.discard(call.call_id)
        return

    call.tier1_start_time_seconds = float(env.now)
    metrics.record_answered(call)

    yield env.timeout(call.tier1_service_seconds)
    call.tier1_end_time_seconds = float(env.now)
    metrics.record_tier1_service(call.tier1_service_seconds)
    resources.tier1.release(tier1_req)

    resolution_probability = _dynamic_tier1_resolution_probability(config, resources)
    if streams.random() <= resolution_probability:
        call.resolved_at_tier1 = True
        metrics.record_resolved_tier1()
        metrics.record_completed()
        active_calls.discard(call.call_id)
        return

    call.escalated = True
    metrics.record_escalation()

    with resources.tier2.request(priority=_priority_for(call)) as tier2_req:
        yield tier2_req
        call.tier2_start_time_seconds = float(env.now)
        yield env.timeout(call.tier2_service_seconds)
        call.tier2_end_time_seconds = float(env.now)
        metrics.record_tier2_service(call.tier2_service_seconds)

    metrics.record_completed()
    active_calls.discard(call.call_id)


def arrivals_process(
    env: simpy.Environment,
    resources: CallCenterResources,
    config: SimulationConfig,
    streams: RandomStreams,
    metrics: MetricsCollector,
    active_calls: set[int],
) -> simpy.Process: # type: ignore
    call_id = 0
    horizon_seconds = config.horizon_minutes * 60.0

    while env.now < horizon_seconds:
        interval_minutes = streams.poisson_interval_minutes(config.arrival_rate_per_minute)
        yield env.timeout(interval_minutes * 60.0)
        if env.now > horizon_seconds:
            break

        call_id += 1
        metrics.record_arrival()
        call = _create_call(call_id, float(env.now), config, streams)
        env.process(handle_call(env, call, resources, config, streams, metrics, active_calls))


def timeseries_sampler(
    env: simpy.Environment,
    resources: CallCenterResources,
    config: SimulationConfig,
    metrics: MetricsCollector,
) -> simpy.Process: # type: ignore
    horizon_seconds = config.horizon_minutes * 60.0
    sample_interval = max(1.0, config.timeseries_interval_seconds)

    while env.now <= horizon_seconds:
        metrics.observe_timeseries(env, resources)
        yield env.timeout(sample_interval)
