def unlock_account(payload: dict) -> dict:
    return {
        "status": "approval_required",
        "message": "Account unlock requires approval in this scaffold.",
        "target_user": payload.get("target_user"),
    }

def reset_password(payload: dict) -> dict:
    return {
        "status": "approval_required",
        "message": "Password reset requires approval in this scaffold.",
        "target_user": payload.get("target_user"),
    }
