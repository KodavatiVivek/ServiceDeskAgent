import httpx
from app.config import settings

async def call_orchestrator(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(settings.orchestrator_url, json=payload)
        response.raise_for_status()
        return response.json()
