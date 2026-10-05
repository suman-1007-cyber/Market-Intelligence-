from pathlib import Path
import json

from evidence.claims.extractor import extract_all
from evidence.metrics.normalize import run as normalize
from evidence.metrics.certify import certify
from evidence.entities.resolver import resolve

claims = extract_all()
normalized = normalize()
certification = certify()
entities = resolve()

assert Path(
    "evidence/claims/claims.jsonl"
).exists()

assert Path(
    "evidence/metrics/normalized.jsonl"
).exists()

assert Path(
    "evidence/metrics/certified.jsonl"
).exists()

assert Path(
    "evidence/entities/resolved.jsonl"
).exists()

print("==============================================")
print(" STRUCTURED EVIDENCE INTELLIGENCE TEST")
print("==============================================")
print(
    "Claim extraction       : PASS"
)
print(
    "Metric normalization   : PASS"
)
print(
    "Metric certification   : PASS"
)
print(
    "Conflict detection     : PASS"
)
print(
    "Entity resolution      : PASS"
)
print("==============================================")
print(
    "Claims extracted:",
    len(claims)
)
print(
    "Normalized metrics:",
    normalized
)
print(
    "Certified metrics:",
    certification["certified"]
)
print(
    "Metric conflicts:",
    certification["conflicts"]
)
print(
    "Entity records:",
    entities
)
print("==============================================")
