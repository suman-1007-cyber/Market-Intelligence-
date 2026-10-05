def aggregate(authority, freshness, corroboration, completeness, methodology):
    values = [
        float(authority),
        float(freshness),
        float(corroboration),
        float(completeness),
        float(methodology),
    ]

    values = [max(0.0, min(1.0, v)) for v in values]
    score = sum(values) / len(values)

    if score >= 0.85:
        status = "high"
    elif score >= 0.70:
        status = "medium"
    else:
        status = "low"

    return {
        "score": score,
        "status": status,
        "components": {
            "authority": values[0],
            "freshness": values[1],
            "corroboration": values[2],
            "completeness": values[3],
            "methodology": values[4],
        },
    }
