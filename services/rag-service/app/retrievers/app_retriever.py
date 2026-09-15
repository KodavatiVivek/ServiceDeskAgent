from app.retrievers.base import SimpleKeywordRetriever

APP_DOCS = [
    {
        "title": "CRM Offboarding SOP",
        "source": "data/app/crm_offboarding.txt",
        "content": "For CRM offboarding, validate termination ticket, disable the user account instead of deleting it, remove CRM roles, revoke active sessions, and update ServiceNow work notes."
    }
]

def search_app(query: str, top_k: int = 5):
    return SimpleKeywordRetriever(APP_DOCS).search(query, top_k)
