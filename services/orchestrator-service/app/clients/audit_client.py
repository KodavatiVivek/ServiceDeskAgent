import httpx
from app.config import settings

async def send_audit_event(payload: dict) -> None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(settings.audit_service_url, json=payload)
    except Exception:
        # Audit failure should not break user response in this scaffold.
        return None
