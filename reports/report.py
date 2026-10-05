from pathlib import Path
from datetime import datetime, timezone
import json

def generate(title, sections, output="reports/report.md"):
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "> Evidence-first deterministic analysis.",
        ""
    ]

    for heading, content in sections:
        lines += [f"## {heading}", ""]
        if isinstance(content, (dict, list)):
            lines += ["```json", json.dumps(content, indent=2, default=str), "```", ""]
        else:
            lines += [str(content), ""]

    p.write_text("\n".join(lines), encoding="utf-8")
    return p
