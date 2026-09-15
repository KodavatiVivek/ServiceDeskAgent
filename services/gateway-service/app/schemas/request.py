from pydantic import BaseModel, Field
from typing import Optional

class AgentAskRequest(BaseModel):
    user_query: str = Field(..., min_length=1)
    user_id: str = Field(default="anonymous")
    user_role: str = Field(default="employee")
    incident_id: Optional[str] = None
