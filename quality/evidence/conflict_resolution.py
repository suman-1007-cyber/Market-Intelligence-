def resolve(facts, tolerance=0.05):
    if not facts:
        return {
            "status": "no_evidence",
            "selected": None,
            "reason": "no_facts",
        }

    ranked = sorted(
        facts,
        key=lambda x: float(x.get("confidence", 0.0)),
        reverse=True,
    )

    values = []
    for fact in ranked:
        try:
            values.append(float(fact["value"]))
        except (KeyError, TypeError, ValueError):
            pass

    if not values:
        return {
            "status": "unresolved",
            "selected": None,
            "reason": "no_numeric_values",
        }

    minimum = min(values)
    maximum = max(values)

    if minimum == 0:
        spread = 0.0 if maximum == 0 else 1.0
    else:
        spread = abs(maximum - minimum) / abs(minimum)

    if spread <= tolerance:
        return {
            "status": "resolved",
            "selected": ranked[0],
            "reason": "values_within_tolerance",
            "spread": spread,
        }

    return {
        "status": "conflict",
        "selected": None,
        "reason": "material_value_difference",
        "spread": spread,
        "candidates": ranked,
    }
