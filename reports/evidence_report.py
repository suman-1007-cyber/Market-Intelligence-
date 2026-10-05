from pathlib import Path
from datetime import datetime, timezone
import json

def generate(
    question,
    plan,
    quality,
    analysis,
    evidence,
    triangulation,
    output="reports/market_intelligence_report.md"
):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Market Intelligence Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Question",
        "",
        question,
        "",
        "## Investigation Plan",
        "",
        "```json",
        json.dumps(plan, indent=2),
        "```",
        "",
        "## Data Quality",
        "",
        "```json",
        json.dumps(quality, indent=2, default=str),
        "```",
        "",
        "## Analysis",
        "",
        "```json",
        json.dumps(analysis, indent=2, default=str),
        "```",
        "",
        "## Evidence",
        "",
        "```json",
        json.dumps(evidence, indent=2, default=str),
        "```",
        "",
        "## Source Triangulation",
        "",
        "```json",
        json.dumps(triangulation, indent=2, default=str),
        "```",
        "",
        "## Evidence Rule",
        "",
        "Every conclusion must be traceable to source, raw evidence, "
        "certified data, metric calculation, analysis and visualization.",
        ""
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
