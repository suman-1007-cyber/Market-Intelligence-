import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quality.evidence.freshness import assess
from quality.evidence.conflicts import detect
from quality.evidence.confidence import score
from quality.evidence.certification import certify


def main():
    fresh = assess(
        "2026-10-04T00:00:00+00:00",
        max_age_days=7,
        now="2026-10-05T00:00:00+00:00",
    )

    stale = assess(
        "2026-09-01T00:00:00+00:00",
        max_age_days=7,
        now="2026-10-05T00:00:00+00:00",
    )

    assert fresh["status"] == "fresh"
    assert stale["status"] == "stale"

    facts = [
        {
            "entity": "Alpha",
            "metric": "market_share",
            "value": 42,
            "unit": "%",
            "period": "2026",
            "geography": "India",
            "source_url": "https://source-a.example",
        },
        {
            "entity": "Alpha",
            "metric": "market_share",
            "value": 35,
            "unit": "%",
            "period": "2026",
            "geography": "India",
            "source_url": "https://source-b.example",
        },
    ]

    conflicts = detect(facts)

    assert len(conflicts) == 1
    assert conflicts[0]["spread"] == 7

    confidence = score(
        authority=1.0,
        freshness=1.0,
        corroboration=0.8,
        completeness=1.0,
        methodology=0.9,
    )

    assert 0.0 <= confidence["score"] <= 1.0
    assert abs(confidence["score"] - 0.94) < 1e-9

    good_fact = {
        "entity": "Alpha",
        "metric": "market_share",
        "value": 42,
        "unit": "%",
        "period": "2026",
        "confidence": 0.94,
    }

    certified = certify(
        good_fact,
        confidence_threshold=0.70,
        freshness_status="fresh",
        conflict=False,
    )

    rejected = certify(
        good_fact,
        confidence_threshold=0.70,
        freshness_status="fresh",
        conflict=True,
    )

    assert certified["certified"] is True
    assert certified["status"] == "CERTIFIED"

    assert rejected["certified"] is False
    assert "metric_conflict" in rejected["reasons"]

    print("==============================================")
    print(" MARKET INTELLIGENCE 21-24 MILESTONE")
    print("==============================================")
    print("21. Evidence Freshness           : PASS")
    print("22. Evidence Conflict Detection  : PASS")
    print("23. Confidence Scoring           : PASS")
    print("24. Certification Gate            : PASS")
    print("----------------------------------------------")
    print("Fresh evidence  :", fresh["status"])
    print("Stale evidence  :", stale["status"])
    print("Conflicts found :", len(conflicts))
    print("Confidence      :", confidence["score"])
    print("Certified       :", certified["status"])
    print("Rejected        :", rejected["status"])
    print("==============================================")
    print("MILESTONE 21-24 : PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
