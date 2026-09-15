from app.retrievers.base import SimpleKeywordRetriever

PAM_DOCS = [
    {
        "title": "CyberArk Password Checkout Failure SOP",
        "source": "data/pam/cyberark_checkout_sop.txt",
        "content": "For CyberArk password checkout failure, first verify safe membership, then confirm that the password object is not locked by another active session. Check CPM reconciliation status and review recent vault activity logs. If authorization fails, route the incident to PAM Operations."
    },
    {
        "title": "PAM Safe Membership Troubleshooting",
        "source": "data/pam/safe_membership.txt",
        "content": "When a user cannot access a CyberArk safe, validate AD group membership, CyberArk safe permissions, platform policy, and whether synchronization has completed. Refresh membership only after confirming manager approval."
    },
    {
        "title": "PAM Escalation Matrix",
        "source": "data/pam/escalation_matrix.txt",
        "content": "PAM password checkout, vault access, and privileged session launch failures should be assigned to PAM Operations. High-risk privileged account unlocks require PAM L2 approval."
    }
]

def search_pam(query: str, top_k: int = 5):
    return SimpleKeywordRetriever(PAM_DOCS).search(query, top_k)
