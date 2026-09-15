from pydantic import BaseModel
from typing import Any

class SearchResponse(BaseModel):
    documents: list[dict[str, Any]]
