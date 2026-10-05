def score(
    authority=0.5,
    freshness=0.5,
    corroboration=0.5,
    completeness=0.5,
    methodology=0.5,
):
    components = [
        float(authority),
        float(freshness),
        float(corroboration),
        float(completeness),
        float(methodology),
    ]

    components = [
        max(0.0, min(1.0, value))
        for value in components
    ]

    return {
        "score": sum(components) / len(components),
        "components": {
            "authority": components[0],
            "freshness": components[1],
            "corroboration": components[2],
            "completeness": components[3],
            "methodology": components[4],
        },
    }
