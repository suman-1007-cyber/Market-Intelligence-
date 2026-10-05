from .registry import enabled

KEYWORDS = {
    "market": ["market", "industry", "market size", "market share", "growth"],
    "competitive": ["competitor", "competition", "rival", "leader"],
    "customer": ["customer", "consumer", "user", "segment"],
    "financial": ["revenue", "sales", "profit", "financial"],
    "pricing": ["price", "pricing", "cost"],
    "geographic": ["country", "region", "geography"],
    "trend": ["trend", "growth", "decline"],
    "forecast": ["forecast", "projection", "future"],
    "risk": ["risk", "threat"],
    "opportunity": ["opportunity", "potential"]
}

def discover(question):
    q = question.lower()
    domains = []

    for domain, words in KEYWORDS.items():
        if any(word in q for word in words):
            domains.append(domain)

    if not domains:
        domains = ["market", "competitive", "customer", "trend"]

    sources = enabled()

    return {
        "domains": domains,
        "source_classes": [s["type"] for s in sources],
        "source_count": len(sources),
        "query_terms": q.split()
    }
