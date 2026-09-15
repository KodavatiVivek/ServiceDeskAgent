from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from datetime import datetime, timezone

router = APIRouter()
AUDIT_EVENTS: list[dict[str, Any]] = []

class AuditEvent(BaseModel):
    event_type: str
    correlation_id: str | None = None
    user_id: str | None = None
    planner_decision: dict[str, Any] | None = None
    metadata: dict[str, Any] = {}

@router.post("/internal/audit/events")
async def add_audit_event(event: AuditEvent):
    record = event.model_dump()
    record["created_at"] = datetime.now(timezone.utc).isoformat()
    AUDIT_EVENTS.append(record)
    return {"status": "stored", "count": len(AUDIT_EVENTS)}

@router.get("/internal/audit/events")
async def list_audit_events():
    return {"events": AUDIT_EVENTS[-50:]}
