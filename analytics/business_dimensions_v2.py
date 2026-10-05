DIMENSIONS = {
    "financial": {
        "revenue",
        "profit",
        "profit_margin",
        "ebitda",
        "cash_flow",
    },
    "pricing": {
        "price",
        "average_price",
        "discount",
        "pricing",
    },
    "geographic": {
        "market_size",
        "population",
        "regional_share",
        "market_share",
    },
}


def analyze(facts):
    result = {
        "financial": [],
        "pricing": [],
        "geographic": [],
    }

    for fact in facts:
        metric = str(fact.get("metric", "")).lower()

        for dimension, metrics in DIMENSIONS.items():
            if metric in metrics:
                result[dimension].append(fact)

    result["counts"] = {
        key: len(value)
        for key, value in result.items()
        if isinstance(value, list)
    }

    return result
