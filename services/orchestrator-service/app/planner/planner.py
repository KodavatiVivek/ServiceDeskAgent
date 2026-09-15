import re
from app.planner.schemas import PlannerDecision

def simple_planner(user_query: str, incident_id: str | None = None) -> PlannerDecision:
    q = user_query.lower()

    sub_domain = "general"
    domain = "general"
    intent = "general_support"
    retrieval_required = True
    selected_tools: list[str] = []

    if any(word in q for word in ["cyberark", "pam", "password checkout", "vault", "safe membership"]):
        domain = "security"
        sub_domain = "pam"
        intent = "password_checkout_failure"
        selected_tools.append("pam_retriever")
    elif any(word in q for word in ["iam", "account locked", "mfa", "password reset"]):
        domain = "security"
        sub_domain = "iam"
        intent = "iam_support"
        selected_tools.append("iam_retriever")
    elif any(word in q for word in ["vpn", "dns", "firewall", "proxy"]):
        domain = "network"
        sub_domain = "vpn" if "vpn" in q else "network"
        intent = "network_support"
        selected_tools.append("network_retriever")
    elif any(word in q for word in ["aws", "azure", "cloud"]):
        domain = "cloud"
        sub_domain = "aws" if "aws" in q else "azure" if "azure" in q else "cloud"
        intent = "cloud_support"
        selected_tools.append("cloud_retriever")

    detected_incident = incident_id
    if not detected_incident:
        match = re.search(r"INC\d+", user_query, flags=re.IGNORECASE)
        if match:
            detected_incident = match.group(0).upper()

    servicenow_context_required = bool(detected_incident)
    tool_required = False

    if servicenow_context_required:
        tool_required = True
        selected_tools.append("servicenow_fetch_incident")

    if "create ticket" in q or "create incident" in q or "raise ticket" in q:
        tool_required = True
        selected_tools.append("servicenow_create_incident")

    approval_required = any(word in q for word in ["unlock", "reset password", "disable", "remove access", "terminate"])
    risk_level = "medium" if approval_required else "low"

    if any(word in q for word in ["disable crm", "terminate", "remove access"]):
        domain = "application"
        sub_domain = "crm"
        intent = "offboarding"
        tool_required = True
        approval_required = True
        risk_level = "high"
        selected_tools.extend(["crm_disable_user", "servicenow_update_incident"])

    return PlannerDecision(
        intent=intent,
        domain=domain,
        sub_domain=sub_domain,
        incident_id=detected_incident,
        servicenow_context_required=servicenow_context_required,
        retrieval_required=retrieval_required,
        tool_required=tool_required,
        approval_required=approval_required,
        selected_tools=list(dict.fromkeys(selected_tools)),
        risk_level=risk_level,
        confidence=0.85,
    )
