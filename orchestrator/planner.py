KEYWORDS = {
    "market": ["market", "industry", "size", "share", "growth"],
    "competitive": ["competitor", "competition", "rival", "leader"],
    "customer": ["customer", "consumer", "user", "segment"],
    "pricing": ["price", "pricing", "cost"],
    "financial": ["revenue", "profit", "financial", "sales"],
    "geographic": ["country", "region", "geography", "location"],
    "trend": ["trend", "growth", "decline", "change"],
    "forecast": ["forecast", "future", "projection"],
    "risk": ["risk", "threat"],
    "opportunity": ["opportunity", "potential"]
}

def plan(question):
    q = question.lower()
    domains = []
    for domain, words in KEYWORDS.items():
        if any(w in q for w in words):
            domains.append(domain)

    if not domains:
        domains = ["market", "competitive", "customer", "trend"]

    return {
        "question": question,
        "domains": domains,
        "steps": [
            "discover_sources",
            "ingest",
            "validate",
            "conform_entities",
            "calculate_metrics",
            "analyze",
            "forecast",
            "assess_opportunities_and_risks",
            "visualize",
            "report"
        ]
    }
