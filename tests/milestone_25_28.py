from sources.authority import score as authority_score
from quality.evidence.triangulation_v2 import analyze
from entities.resolution_confidence import score as entity_score
from audit.lineage import create


def main():
    authority = authority_score({
        "type": "government",
        "domain": "example.gov",
    })

    assert authority["score"] >= 0.80

    facts = [
        {
            "entity": "Alpha",
            "metric": "market_share",
            "value": 42,
            "unit": "%",
            "period": "2026",
            "geography": "India",
            "source_url": "https://a.example",
        },
        {
            "entity": "Alpha",
            "metric": "market_share",
            "value": 42,
            "unit": "%",
            "period": "2026",
            "geography": "India",
            "source_url": "https://b.example",
        },
    ]

    triangulation = analyze(facts)

    assert len(triangulation) == 1
    assert triangulation[0]["source_count"] == 2
    assert triangulation[0]["status"] == "corroborated"

    exact = entity_score("Dassault Systemes", "Dassault Systemes")
    similar = entity_score(
        "Dassault Systemes India",
        "Dassault Systemes",
    )

    assert exact["score"] == 1.0
    assert similar["score"] >= 0.50

    lineage = create(
        source_url="https://example.com/report",
        raw_record={
            "title": "Market Report",
            "value": 42,
        },
        metric="market_share",
        value=42,
        unit="%",
        period="2026",
        entity="Alpha",
        transformation="normalized_percentage",
    )

    assert len(lineage["evidence_hash"]) == 64
    assert lineage["lineage_id"] == lineage["evidence_hash"][:16]
    assert lineage["source_url"] == "https://example.com/report"

    print("==============================================")
    print(" MARKET INTELLIGENCE 25-28 MILESTONE")
    print("==============================================")
    print("25. Source Authority Scoring      : PASS")
    print("26. Source Triangulation         : PASS")
    print("27. Entity Resolution Confidence : PASS")
    print("28. Evidence Lineage             : PASS")
    print("----------------------------------------------")
    print("Authority score :", authority["score"])
    print("Sources checked :", triangulation[0]["source_count"])
    print("Entity exact    :", exact["score"])
    print("Entity similar  :", similar["score"])
    print("Evidence hash   :", lineage["evidence_hash"][:16])
    print("==============================================")
    print("MILESTONE 25-28 : PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
