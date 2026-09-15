from app.retrievers.base import SimpleKeywordRetriever

IAM_DOCS = [
    {
        "title": "IAM Account Unlock SOP",
        "source": "data/iam/account_unlock.txt",
        "content": "For IAM account lock issues, verify user identity, check lockout reason, validate MFA status, and follow approved unlock workflow. High-risk admin accounts require manager approval."
    }
]

def search_iam(query: str, top_k: int = 5):
    return SimpleKeywordRetriever(IAM_DOCS).search(query, top_k)
