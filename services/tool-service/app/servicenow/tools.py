def fetch_incident(payload: dict) -> dict:
    incident_id = payload.get("incident_id") or "INC-DEMO-1001"
    return {
        "number": incident_id,
        "state": "In Progress",
        "priority": "3",
        "assignment_group": "PAM Operations",
        "short_description": payload.get("short_description") or "CyberArk password checkout failure",
        "latest_work_note": "User reported checkout failure. Safe membership and CPM reconciliation should be verified.",
    }

def create_incident(payload: dict) -> dict:
    return {
        "incident_number": "INC-DEMO-2001",
        "assignment_group": "PAM Operations",
        "state": "New",
        "short_description": payload.get("short_description", "Service Desk Agent generated incident"),
    }

def update_incident(payload: dict) -> dict:
    return {
        "incident_number": payload.get("incident_id") or "INC-DEMO-1001",
        "updated": True,
        "work_note": payload.get("work_note", "Updated by Service Desk Agent"),
    }
