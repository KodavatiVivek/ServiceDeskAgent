from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class IngestionRequest(BaseModel):
    domain: str
    source_path: str | None = None

@router.post("/internal/ingest")
async def ingest(request: IngestionRequest):
    return {
        "status": "accepted",
        "message": "Ingestion pipeline placeholder. Add PDF, SharePoint, chunking, embedding, and indexing here.",
        "domain": request.domain,
        "source_path": request.source_path,
    }
