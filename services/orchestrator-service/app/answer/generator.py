from typing import Any

def generate_answer(
    user_query: str,
    decision: dict,
    retrieved_docs: list[dict[str, Any]],
    tool_results: list[dict[str, Any]],
) -> str:
    parts: list[str] = []

    if decision.get("sub_domain") == "pam":
        parts.append("This looks like a PAM/CyberArk support issue.")
    elif decision.get("domain") != "general":
        parts.append(f"This looks like a {decision.get('domain')} / {decision.get('sub_domain')} support issue.")
    else:
        parts.append("I reviewed the request and prepared a support response.")

    if retrieved_docs:
        parts.append("Based on the available SOP or KB context, the recommended next steps are:")
        for idx, doc in enumerate(retrieved_docs[:3], start=1):
            snippet = doc.get("content", "").strip().replace("\n", " ")
            if len(snippet) > 240:
                snippet = snippet[:240] + "..."
            parts.append(f"{idx}. {snippet}")
    else:
        parts.append("I could not find approved SOP context for this request in the current knowledge base.")

    for result in tool_results:
        tool_name = result.get("tool_name")
        status = result.get("status")
        if tool_name == "servicenow_fetch_incident" and status == "success":
            incident = result.get("data", {})
            parts.append(
                f"ServiceNow context: incident {incident.get('number')} is currently "
                f"{incident.get('state')} and assigned to {incident.get('assignment_group')}."
            )
        elif tool_name == "servicenow_create_incident" and status == "success":
            parts.append(f"Created ServiceNow incident {result.get('data', {}).get('incident_number')}.")

    if decision.get("approval_required"):
        parts.append("This request requires approval before any sensitive action can be executed.")

    return "\n\n".join(parts)
