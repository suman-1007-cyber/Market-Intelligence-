def certify(
    fact,
    confidence_threshold=0.70,
    freshness_status="fresh",
    conflict=False,
):
    reasons = []

    confidence = float(fact.get("confidence", 0.0))

    if confidence < float(confidence_threshold):
        reasons.append("confidence_below_threshold")

    if freshness_status not in ("fresh", "current"):
        reasons.append("evidence_not_fresh")

    if conflict:
        reasons.append("metric_conflict")

    required = (
        "entity",
        "metric",
        "value",
        "unit",
        "period",
    )

    for field in required:
        if fact.get(field) in (None, ""):
            reasons.append(f"missing_{field}")

    certified = len(reasons) == 0

    return {
        "certified": certified,
        "status": "CERTIFIED" if certified else "REJECTED",
        "confidence": confidence,
        "reasons": reasons,
    }
