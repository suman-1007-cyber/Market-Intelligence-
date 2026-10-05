
VALID_UNITS = {
    "percent",
    "currency",
    "count",
    "ratio",
    "units"
}

def normalize(claims):
    result = []

    for claim in claims:
        item = dict(claim)
        item["normalized_value"] = float(
            item["normalized_value"]
        )
        item["normalized_unit"] = str(
            item["normalized_unit"]
        ).lower()
        result.append(item)

    return result

def certify(claims):
    gold = []
    rejected = []

    for claim in claims:
        try:
            value = float(claim["normalized_value"])
        except Exception:
            rejected.append({
                **claim,
                "rejection_reason": "non_numeric"
            })
            continue

        if not claim.get("metric"):
            rejected.append({
                **claim,
                "rejection_reason": "missing_metric"
            })
            continue

        if claim.get("normalized_unit") not in VALID_UNITS:
            rejected.append({
                **claim,
                "rejection_reason": "invalid_unit"
            })
            continue

        fact = dict(claim)
        fact["normalized_value"] = value
        fact["gold_status"] = "CERTIFIED"
        gold.append(fact)

    return gold, rejected
