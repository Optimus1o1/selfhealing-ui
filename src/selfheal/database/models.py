from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TestRunModel(BaseModel):
    id: Optional[int] = None
    run_uuid: str
    project_name: str
    policy: str = "assisted"
    started_at: datetime = Field(default_factory=get_utc_now)
    completed_at: Optional[datetime] = None
    total_steps: int = 0
    passed_count: int = 0
    failed_count: int = 0
    healed_count: int = 0
    status: str = "RUNNING"


class HealingEventModel(BaseModel):
    id: Optional[int] = None
    run_id: Optional[int] = None
    target_key: str
    original_locator: str
    healed_locator: Optional[str] = None
    similarity_score: Optional[float] = None
    score_breakdown_json: Optional[str] = None
    decision: str
    reason: Optional[str] = None
    status: str = "pending_review"  # pending_review, promoted, rejected
    retry_success: bool = False
    latency_ms: float = 0.0
    created_at: datetime = Field(default_factory=get_utc_now)


class LocatorHistoryModel(BaseModel):
    id: Optional[int] = None
    target_key: str
    old_locator: str
    new_locator: str
    similarity_score: float
    change_type: str = "HEALED_PROMOTED"
    promoted_at: datetime = Field(default_factory=get_utc_now)
    approved_by: str = "system"
