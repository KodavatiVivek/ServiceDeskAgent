from app.retrievers.base import SimpleKeywordRetriever

CLOUD_DOCS = [
    {
        "title": "Cloud Access Troubleshooting",
        "source": "data/cloud/access_sop.txt",
        "content": "For AWS or Azure access issues, verify role assignment, group membership, conditional access policy, account status, and recent IAM policy changes."
    }
]

def search_cloud(query: str, top_k: int = 5):
    return SimpleKeywordRetriever(CLOUD_DOCS).search(query, top_k)
