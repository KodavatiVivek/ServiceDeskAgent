from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"service": "orchestrator-service", "status": "ok"}
