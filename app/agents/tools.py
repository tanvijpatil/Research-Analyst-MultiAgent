from app.data.sample_documents import SAMPLE_DOCUMENTS

def search_library(query: str) -> str:
    """Search the local sample research library and return relevant excerpts with source titles."""
    terms = {word.lower().strip(".,?!:;()[]{}") for word in query.split() if len(word) > 2}
    ranked = []
    for doc in SAMPLE_DOCUMENTS:
        text = f"{doc['title']} {doc['category']} {doc['content']}".lower()
        score = sum(1 for term in terms if term in text)
        if score:
            ranked.append((score, doc))
    ranked.sort(key=lambda item: item[0], reverse=True)
    if not ranked:
        return "No matching documents were found in the local sample library."
    results = []
    for _, doc in ranked[:4]:
        results.append(
            f"Source: {doc['title']} | Category: {doc['category']}\\n"
            f"Excerpt: {doc['content']}"
        )
    return "\\n\\n".join(results)
