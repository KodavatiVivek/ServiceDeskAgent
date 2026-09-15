from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from app.planner.planner import simple_planner
from app.clients.rag_client import search_rag
from app.clients.tool_client import execute_tool
from app.clients.audit_client import send_audit_event
from app.answer.generator import generate_answer
from app.guardrails.input_guardrails import validate_input
from app.guardrails.output_guardrails import validate_output

router = APIRouter()

class OrchestrateRequest(BaseModel):
    user_query: str
    user_id: str = "anonymous"
    user_role: str = "employee"
    incident_id: Optional[str] = None
    correlation_id: Optional[str] = None

@router.post("/internal/orchestrate")
async def orchestrate(request: OrchestrateRequest):
    safe, reason = validate_input(request.user_query)
    if not safe:
        raise HTTPException(status_code=400, detail=reason)

    decision = simple_planner(request.user_query, request.incident_id)
    retrieved_docs: list[dict[str, Any]] = []
    tool_results: list[dict[str, Any]] = []

    if decision.retrieval_required:
        rag_payload = {
            "query": request.user_query,
            "domain": decision.domain,
            "sub_domain": decision.sub_domain,
            "top_k": 5,
            "user_context": {
                "user_id": request.user_id,
                "role": request.user_role,
            },
            "correlation_id": request.correlation_id,
        }
        try:
            rag_result = await search_rag(rag_payload)
            retrieved_docs = rag_result.get("documents", [])
        except Exception as exc:
            retrieved_docs = [{
                "title": "RAG service unavailable",
                "content": f"RAG retrieval failed: {str(exc)}",
                "source": "system",
                "score": 0.0,
            }]

    for tool_name in decision.selected_tools:
        if tool_name.endswith("_retriever"):
            continue

        tool_payload = {
            "tool_name": tool_name,
            "payload": {
                "incident_id": decision.incident_id,
                "short_description": request.user_query,
                "domain": decision.domain,
                "sub_domain": decision.sub_domain,
            },
            "user_context": {
                "user_id": request.user_id,
                "role": request.user_role,
            },
            "correlation_id": request.correlation_id,
        }

        try:
            result = await execute_tool(tool_payload)
            tool_results.append(result)
        except Exception as exc:
            tool_results.append({
                "tool_name": tool_name,
                "status": "failed",
                "error": str(exc),
            })

    raw_answer = generate_answer(
        user_query=request.user_query,
        decision=decision.model_dump(),
        retrieved_docs=retrieved_docs,
        tool_results=tool_results,
    )
    final_answer = validate_output(raw_answer)

    response = {
        "correlation_id": request.correlation_id or "",
        "answer": final_answer,
        "domain": decision.domain,
        "sub_domain": decision.sub_domain,
        "sources": [
            {
                "title": doc.get("title"),
                "source": doc.get("source"),
                "score": doc.get("score"),
            }
            for doc in retrieved_docs
        ],
        "tool_results": tool_results,
        "planner_decision": decision.model_dump(),
    }

    await send_audit_event({
        "event_type": "agent_request_completed",
        "correlation_id": request.correlation_id,
        "user_id": request.user_id,
        "planner_decision": decision.model_dump(),
    })

    return response
