from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

from evidence.provenance import all as all_evidence
from evidence.claims.schema import Claim

OUTPUT = Path("evidence/claims/claims.jsonl")

NUMBER = r"(?:\d+(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)"

PATTERNS = [
    (
        "percentage",
        re.compile(
            rf"(?P<value>{NUMBER})\s*%"
        )
    ),
    (
        "currency",
        re.compile(
            rf"(?P<currency>USD|INR|EUR|GBP|\$|₹|€|£)\s*"
            rf"(?P<value>{NUMBER})"
        )
    ),
    (
        "currency_suffix",
        re.compile(
            rf"(?P<value>{NUMBER})\s*"
            rf"(?P<unit>million|billion|trillion|crore|lakh)"
        )
    ),
    (
        "number",
        re.compile(
            rf"(?P<value>{NUMBER})"
        )
    )
]

METRIC_WORDS = {
    "revenue": "revenue",
    "sales": "sales",
    "market size": "market_size",
    "market share": "market_share",
    "growth": "growth",
    "profit": "profit",
    "users": "users",
    "customers": "customers",
    "price": "price",
    "valuation": "valuation",
    "investment": "investment",
    "employees": "employees"
}

def _number(value):
    return float(value.replace(",", ""))

def _metric(text):
    lower = text.lower()

    for phrase, metric in sorted(
        METRIC_WORDS.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        if phrase in lower:
            return metric

    return None

def _context(text, start, end, radius=180):
    left = max(0, start - radius)
    right = min(len(text), end + radius)

    return " ".join(
        text[left:right].split()
    )

def _extract_document(evidence):
    path = evidence.get("raw_path")

    if not path:
        return []

    file = Path(path)

    if not file.exists():
        return []

    try:
        text = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        return []

    claims = []

    for pattern_name, pattern in PATTERNS:
        for match in pattern.finditer(text):
            value = _number(
                match.group("value")
            )

            context = _context(
                text,
                match.start(),
                match.end()
            )

            metric = _metric(context)

            if not metric and pattern_name == "number":
                continue

            unit = None
            currency = None

            if pattern_name == "percentage":
                unit = "percent"

            if pattern_name == "currency":
                currency = match.group(
                    "currency"
                )

            if pattern_name == "currency_suffix":
                unit = match.group("unit")

            claim_id = hashlib.sha256(
                (
                    f"{evidence.get('evidence_id')}"
                    f"|{context}"
                    f"|{value}"
                ).encode()
            ).hexdigest()[:24]

            claims.append(
                Claim(
                    claim_id=claim_id,
                    evidence_id=evidence.get(
                        "evidence_id"
                    ),
                    source_url=evidence.get(
                        "url"
                    ),
                    title=evidence.get(
                        "source",
                        ""
                    ),
                    claim=context,
                    metric=metric,
                    value=value,
                    unit=unit,
                    currency=currency,
                    period=None,
                    geography=None,
                    entity=None,
                    confidence=float(
                        evidence.get(
                            "confidence",
                            0.5
                        )
                    ),
                    extraction_method=(
                        "deterministic_regex_context"
                    )
                )
            )

    return claims

def extract_all():
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    evidence = all_evidence()
    seen = set()
    claims = []

    for item in evidence:
        for claim in _extract_document(item):
            if claim.claim_id in seen:
                continue

            seen.add(claim.claim_id)
            claims.append(claim)

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        for claim in claims:
            f.write(
                claim.to_json() + "\n"
            )

    return claims
