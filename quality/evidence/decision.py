def decide(
    confidence,
    freshness_status,
    conflict_status,
    required_fields=True,
    threshold=0.70,
):
    reasons = []

    if float(confidence) < threshold:
        reasons.append("low_confidence")

    if freshness_status not in {"fresh", "current"}:
        reasons.append("not_fresh")

    if conflict_status == "conflict":
        reasons.append("unresolved_conflict")

    if not required_fields:
        reasons.append("missing_required_fields")

    certified = not reasons

    return {
        "certified": certified,
        "status": "CERTIFIED" if certified else "REJECTED",
        "confidence": float(confidence),
        "threshold": float(threshold),
        "reasons": reasons,
    }
