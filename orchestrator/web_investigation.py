from pathlib import Path
import json

from sources.discovery import discover
from evidence.web.collector import collect

def investigate(question, limit=5):
    source_plan = discover(question)

    queries = [
        question,
        f"{question} market size",
        f"{question} market share",
        f"{question} competitors"
    ]

    all_results = []
    seen = set()

    for query in queries:
        result = collect(query, limit=limit)

        for item in result["results"]:
            url = item.get("url")

            if url and url not in seen:
                seen.add(url)
                all_results.append(item)

    output = {
        "question": question,
        "domains": source_plan["domains"],
        "source_classes": source_plan["source_classes"],
        "documents": all_results,
        "document_count": len(all_results)
    }

    Path("storage/silver/web/investigation.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8"
    )

    return output
