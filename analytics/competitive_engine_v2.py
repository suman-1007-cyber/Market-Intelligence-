def analyze(facts):
    rows = [
        f for f in facts
        if f.get("metric") == "market_share"
        and f.get("entity")
    ]

    ranked = sorted(
        rows,
        key=lambda x: float(x.get("value", 0)),
        reverse=True,
    )

    return {
        "ranked_competitors": [
            {
                "entity": row["entity"],
                "market_share": float(row["value"]),
                "unit": row.get("unit"),
                "source_url": row.get("source_url"),
            }
            for row in ranked
        ]
    }
