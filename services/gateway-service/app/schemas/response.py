from pydantic import BaseModel
from typing import Any

class AgentAskResponse(BaseModel):
    correlation_id: str
    answer: str
    domain: str | None = None
    sub_domain: str | None = None
    sources: list[dict[str, Any]] = []
    tool_results: list[dict[str, Any]] = []
