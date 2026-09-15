from pydantic import BaseModel
from typing import Any

class SearchRequest(BaseModel):
    query: str
    domain: str = "general"
    sub_domain: str = "general"
    top_k: int = 5
    user_context: dict[str, Any] = {}
    correlation_id: str | None = None
