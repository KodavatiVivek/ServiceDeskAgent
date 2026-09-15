from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.schemas.request import AgentAskRequest
from app.schemas.response import AgentAskResponse
from app.clients.orchestrator_client import call_orchestrator

router = APIRouter()

@router.post("/api/v1/agent/ask", response_model=AgentAskResponse)
async def ask_agent(request: AgentAskRequest):
    correlation_id = str(uuid4())
    payload = request.model_dump()
    payload["correlation_id"] = correlation_id

    try:
        result = await call_orchestrator(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call orchestrator-service: {str(exc)}"
        )

    result.setdefault("correlation_id", correlation_id)
    return result
