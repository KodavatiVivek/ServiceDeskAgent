def disable_user(payload: dict) -> dict:
    return {
        "status": "approval_required",
        "message": "CRM disablement requires approval in this scaffold.",
        "target_user": payload.get("target_user"),
    }
