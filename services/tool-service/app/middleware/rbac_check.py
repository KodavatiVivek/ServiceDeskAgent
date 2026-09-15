def is_tool_allowed(tool_name: str, user_context: dict) -> tuple[bool, str | None]:
    role = user_context.get("role", "employee")

    read_tools = {"servicenow_fetch_incident", "servicenow_search_similar_incidents"}
    write_tools = {"servicenow_create_incident", "servicenow_update_incident"}
    sensitive_tools = {"avatier_unlock_account", "avatier_reset_password", "crm_disable_user"}

    if tool_name in read_tools:
        return True, None

    if tool_name in write_tools and role in {"l1_support", "l2_support", "manager", "admin"}:
        return True, None

    if tool_name in sensitive_tools and role in {"manager", "admin"}:
        return True, None

    return False, f"Role '{role}' is not allowed to execute tool '{tool_name}'."
