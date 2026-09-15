from pydantic import BaseModel
from typing import Optional, Literal

class PlannerDecision(BaseModel):
    intent: str
    domain: str
    sub_domain: str
    incident_id: Optional[str] = None
    servicenow_context_required: bool = False
    retrieval_required: bool = False
    tool_required: bool = False
    approval_required: bool = False
    selected_tools: list[str] = []
    risk_level: Literal["low", "medium", "high"] = "low"
    confidence: float = 0.8
