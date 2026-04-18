from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CustomerType(str, Enum):
    NORMAL = "normal"
    VIP = "vip"


@dataclass
class Call:
    call_id: int
    customer_type: CustomerType
    arrival_time_seconds: float
    patience_seconds: float
    ivr_duration_seconds: float
    tier1_service_seconds: float
    tier2_service_seconds: float

    queue_enter_time_seconds: Optional[float] = None
    tier1_start_time_seconds: Optional[float] = None
    tier1_end_time_seconds: Optional[float] = None
    tier2_start_time_seconds: Optional[float] = None
    tier2_end_time_seconds: Optional[float] = None
    abandoned_time_seconds: Optional[float] = None
    escalated: bool = False
    resolved_at_tier1: bool = False

    @property
    def answered(self) -> bool:
        return self.tier1_start_time_seconds is not None
