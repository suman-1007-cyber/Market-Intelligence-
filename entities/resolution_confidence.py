def score(candidate, canonical):
    candidate = str(candidate or "").strip().lower()
    canonical = str(canonical or "").strip().lower()

    if not candidate or not canonical:
        return {
            "score": 0.0,
            "status": "unresolved",
        }

    if candidate == canonical:
        return {
            "score": 1.0,
            "status": "exact",
        }

    candidate_tokens = set(candidate.replace("-", " ").split())
    canonical_tokens = set(canonical.replace("-", " ").split())

    if not candidate_tokens or not canonical_tokens:
        return {
            "score": 0.0,
            "status": "unresolved",
        }

    intersection = len(candidate_tokens & canonical_tokens)
    union = len(candidate_tokens | canonical_tokens)

    similarity = intersection / union

    if similarity >= 0.80:
        status = "high"
    elif similarity >= 0.50:
        status = "medium"
    else:
        status = "low"

    return {
        "score": similarity,
        "status": status,
    }
