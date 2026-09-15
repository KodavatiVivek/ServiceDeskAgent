from fastapi import APIRouter, HTTPException
from app.schemas.tool_request import ToolExecutionRequest
from app.middleware.rbac_check import is_tool_allowed
from app.registry.tool_registry import execute_registered_tool

router = APIRouter()

@router.post("/internal/tools/execute")
async def execute_tool(request: ToolExecutionRequest):
    allowed, reason = is_tool_allowed(request.tool_name, request.user_context)
    if not allowed:
        raise HTTPException(status_code=403, detail=reason)

    data = execute_registered_tool(request.tool_name, request.payload)

    return {
        "tool_name": request.tool_name,
        "status": "success",
        "data": data,
        "correlation_id": request.correlation_id,
    }
