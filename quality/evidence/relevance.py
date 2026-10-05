import re

METRIC_CONTEXT = {
    "revenue": ["revenue", "turnover", "sales"],
    "sales": ["sales", "sold", "units sold"],
    "market_size": ["market size", "market worth", "market valued", "market value"],
    "market_share": ["market share", "share of the market"],
    "growth": ["growth", "grew", "increase", "increased", "decline", "declined"],
    "profit": ["profit", "net income", "operating income"],
    "customers": ["customers", "customer base", "users", "subscribers"],
    "investment": ["investment", "invested", "funding", "raised"],
    "valuation": ["valuation", "valued at"],
    "price": ["price", "pricing", "cost"],
    "employees": ["employees", "workforce", "staff"]
}

def classify(text):
    lower = (text or "").lower()

    matches = []

    for metric, words in METRIC_CONTEXT.items():
        for word in words:
            if word in lower:
                matches.append(metric)
                break

    return list(dict.fromkeys(matches))

def relevance_score(row):
    text = row.get("claim", "")
    metrics = classify(text)

    score = 0.0

    if metrics:
        score += 0.50

    if row.get("source_url"):
        score += 0.10

    if row.get("evidence_id"):
        score += 0.10

    confidence = float(
        row.get("confidence", 0.0)
    )

    score += min(confidence, 1.0) * 0.30

    return {
        "score": round(min(score, 1.0), 4),
        "metrics": metrics
    }
