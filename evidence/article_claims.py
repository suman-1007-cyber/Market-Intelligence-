
import re
import hashlib

PATTERNS = [
    (
        "growth_rate",
        re.compile(
            r"(\d+(?:\.\d+)?)\s*%\s*"
            r"(?:year[- ]over[- ]year|YoY|growth)",
            re.I
        )
    ),
    (
        "percentage",
        re.compile(r"(\d+(?:\.\d+)?)\s*%")
    )
]

def extract(text, source_url="", title=""):
    claims = []

    if not text:
        return claims

    for metric, pattern in PATTERNS:
        for match in pattern.finditer(text):
            value = float(match.group(1))

            claims.append({
                "claim_id": "claim_" + hashlib.sha256(
                    (source_url + "|" + match.group(0)).encode()
                ).hexdigest()[:20],
                "claim": match.group(0),
                "metric": metric,
                "value": value,
                "unit": "percent",
                "normalized_value": value,
                "normalized_unit": "percent",
                "source_url": source_url,
                "title": title,
                "confidence": 0.85
            })

    return claims
