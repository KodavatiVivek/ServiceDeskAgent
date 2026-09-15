from app.servicenow.tools import fetch_incident, create_incident, update_incident
from app.avatier.tools import unlock_account, reset_password
from app.crm.tools import disable_user

def execute_registered_tool(tool_name: str, payload: dict) -> dict:
    if tool_name == "servicenow_fetch_incident":
        return fetch_incident(payload)
    if tool_name == "servicenow_create_incident":
        return create_incident(payload)
    if tool_name == "servicenow_update_incident":
        return update_incident(payload)
    if tool_name == "avatier_unlock_account":
        return unlock_account(payload)
    if tool_name == "avatier_reset_password":
        return reset_password(payload)
    if tool_name == "crm_disable_user":
        return disable_user(payload)

    return {
        "message": f"Tool '{tool_name}' is registered as placeholder only.",
        "payload_received": payload,
    }
