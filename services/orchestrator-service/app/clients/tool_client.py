import httpx
from app.config import settings

async def execute_tool(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(settings.tool_service_url, json=payload)
        response.raise_for_status()
        return response.json()
