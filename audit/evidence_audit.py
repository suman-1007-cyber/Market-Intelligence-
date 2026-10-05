from datetime import datetime, timezone


def audit(
    facts,
    certified_facts,
    rejected_facts,
    conflicts,
    lineage_records,
):
    total = len(facts)
    certified = len(certified_facts)
    rejected = len(rejected_facts)

    certification_rate = (
        certified / total
        if total
        else 0.0
    )

    return {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "input_facts": total,
        "certified_facts": certified,
        "rejected_facts": rejected,
        "certification_rate": certification_rate,
        "conflicts": len(conflicts),
        "lineage_records": len(lineage_records),
        "lineage_coverage": (
            len(lineage_records) / total
            if total
            else 0.0
        ),
        "audit_status": (
            "PASS"
            if certified + rejected == total
            and len(lineage_records) >= certified
            else "REVIEW"
        ),
    }
