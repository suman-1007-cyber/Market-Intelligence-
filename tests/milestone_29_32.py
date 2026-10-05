import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quality.evidence.reliability import aggregate
from quality.evidence.conflict_resolution import resolve
from quality.evidence.decision import decide
from audit.evidence_audit import audit


def main():
    reliability = aggregate(
        authority=0.95,
        freshness=0.95,
        corroboration=0.90,
        completeness=0.95,
        methodology=0.90,
    )

    assert reliability["status"] == "high"
    assert reliability["score"] >= 0.90

    facts = [
        {
            "value": 42,
            "confidence": 0.94,
            "source_url": "https://a.example",
        },
        {
            "value": 43,
            "confidence": 0.90,
            "source_url": "https://b.example",
        },
    ]

    resolved = resolve(facts)

    assert resolved["status"] == "resolved"
    assert resolved["selected"]["value"] == 42

    conflict_facts = [
        {
            "value": 42,
            "confidence": 0.94,
            "source_url": "https://a.example",
        },
        {
            "value": 60,
            "confidence": 0.90,
            "source_url": "https://b.example",
        },
    ]

    conflict = resolve(conflict_facts)

    assert conflict["status"] == "conflict"

    certified = decide(
        confidence=0.94,
        freshness_status="fresh",
        conflict_status="resolved",
        required_fields=True,
    )

    rejected = decide(
        confidence=0.60,
        freshness_status="fresh",
        conflict_status="resolved",
        required_fields=True,
    )

    assert certified["certified"] is True
    assert rejected["certified"] is False
    assert "low_confidence" in rejected["reasons"]

    audit_result = audit(
        facts=facts,
        certified_facts=[facts[0]],
        rejected_facts=[facts[1]],
        conflicts=[],
        lineage_records=[{"lineage_id": "abc"}],
    )

    assert audit_result["input_facts"] == 2
    assert audit_result["certified_facts"] == 1
    assert audit_result["rejected_facts"] == 1
    assert audit_result["audit_status"] == "PASS"

    print("==============================================")
    print(" MARKET INTELLIGENCE 29-32 MILESTONE")
    print("==============================================")
    print("29. Source Reliability Aggregation : PASS")
    print("30. Conflict Resolution            : PASS")
    print("31. Certification Decision Engine  : PASS")
    print("32. End-to-End Evidence Audit      : PASS")
    print("----------------------------------------------")
    print("Reliability score :", reliability["score"])
    print("Reliability status:", reliability["status"])
    print("Conflict handling :", conflict["status"])
    print("Certification     :", certified["status"])
    print("Rejected evidence :", rejected["status"])
    print("Audit status      :", audit_result["audit_status"])
    print("==============================================")
    print("MILESTONE 29-32 : PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
