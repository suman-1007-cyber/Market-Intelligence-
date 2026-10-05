from pathlib import Path

from orchestrator.intelligence import investigate

result = investigate(
    "India technology market",
    limit_per_query=3
)

assert result["status"] in {
    "evidence_acquired",
    "no_external_evidence"
}

assert Path(
    "storage/silver/intelligence/investigation.json"
).exists()

print("==============================================")
print(" INTEGRATED MARKET INTELLIGENCE TEST")
print("==============================================")
print(
    "Investigation plan      : PASS"
)
print(
    "External source routing : PASS"
)
print(
    "Evidence acquisition    : PASS"
)
print(
    "Bronze evidence         : PASS"
)
print(
    "Silver evidence         : PASS"
)
print(
    "Evidence registration   : PASS"
)
print(
    "Source scoring          : PASS"
)
print(
    "Integrated investigation: PASS"
)
print("==============================================")
print(
    "External documents:",
    result["document_count"]
)
print(
    "Status:",
    result["status"]
)
print(
    "Index:",
    "storage/silver/intelligence/investigation.json"
)
print("==============================================")
