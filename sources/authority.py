def score(source):
    source_type = str(source.get("type", "")).lower()
    domain = str(source.get("domain", "")).lower()

    score = 0.50
    reasons = []

    if source_type in {"government", "regulator", "official"}:
        score += 0.30
        reasons.append("primary_authoritative_source")

    elif source_type in {"company", "filing", "exchange"}:
        score += 0.20
        reasons.append("primary_business_source")

    elif source_type in {"research", "academic"}:
        score += 0.15
        reasons.append("research_source")

    elif source_type in {"news", "media"}:
        score += 0.05
        reasons.append("secondary_media_source")

    if domain.endswith(".gov") or ".gov." in domain:
        score += 0.10
        reasons.append("government_domain")

    if domain.endswith(".edu") or ".ac." in domain:
        score += 0.05
        reasons.append("academic_domain")

    score = min(score, 1.0)

    return {
        "score": score,
        "reasons": reasons,
    }
