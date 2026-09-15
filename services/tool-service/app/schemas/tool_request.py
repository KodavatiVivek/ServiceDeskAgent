from pydantic import BaseModel
from typing import Any

class ToolExecutionRequest(BaseModel):
    tool_name: str
    payload: dict[str, Any] = {}
    user_context: dict[str, Any] = {}
    correlation_id: str | None = None
