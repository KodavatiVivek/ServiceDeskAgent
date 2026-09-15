from app.retrievers.base import SimpleKeywordRetriever

NETWORK_DOCS = [
    {
        "title": "VPN Troubleshooting SOP",
        "source": "data/network/vpn_sop.txt",
        "content": "For VPN issues, check user network connectivity, MFA completion, device compliance, VPN client version, DNS resolution, and recent firewall policy changes."
    }
]

def search_network(query: str, top_k: int = 5):
    return SimpleKeywordRetriever(NETWORK_DOCS).search(query, top_k)
