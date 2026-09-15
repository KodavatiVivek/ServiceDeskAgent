from typing import Any

class SimpleKeywordRetriever:
    def __init__(self, documents: list[dict[str, Any]]):
        self.documents = documents

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        q_terms = set(query.lower().split())
        scored = []

        for doc in self.documents:
            content = (doc.get("title", "") + " " + doc.get("content", "")).lower()
            score = sum(1 for term in q_terms if term in content)
            if score > 0:
                result = dict(doc)
                result["score"] = round(score / max(len(q_terms), 1), 3)
                scored.append(result)

        scored.sort(key=lambda d: d["score"], reverse=True)
        return scored[:top_k]
