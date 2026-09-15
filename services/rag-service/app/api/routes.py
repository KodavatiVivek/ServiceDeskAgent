from fastapi import APIRouter
from app.schemas.search_request import SearchRequest
from app.schemas.search_response import SearchResponse
from app.retrievers.pam_retriever import search_pam
from app.retrievers.iam_retriever import search_iam
from app.retrievers.network_retriever import search_network
from app.retrievers.cloud_retriever import search_cloud
from app.retrievers.app_retriever import search_app

router = APIRouter()

@router.post("/internal/rag/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    sub = request.sub_domain.lower()
    domain = request.domain.lower()

    if sub == "pam":
        docs = search_pam(request.query, request.top_k)
    elif sub == "iam":
        docs = search_iam(request.query, request.top_k)
    elif domain == "network":
        docs = search_network(request.query, request.top_k)
    elif domain == "cloud":
        docs = search_cloud(request.query, request.top_k)
    elif domain == "application" or sub == "crm":
        docs = search_app(request.query, request.top_k)
    else:
        docs = []

    return {"documents": docs}
