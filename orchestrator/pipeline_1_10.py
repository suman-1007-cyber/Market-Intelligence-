
from pathlib import Path
import json

from ingestion.tabular.reader import ingest
from quality.tabular_validation import validate, infer_types
from evidence.article_claims import extract
from quality.gold_pipeline import normalize, certify
from quality.triangulation import run as triangulate
from entities.resolution import resolve
from semantic.business_layer import build
from analytics.certified import run as analytics_run

def run(table_path, article_records):
    table = ingest(table_path)
    validated = {}

    for sheet, rows in table["sheets"].items():
        check = validate(rows)

        if check["valid"]:
            validated[sheet] = {
                "rows": check["rows"],
                "headers": check["headers"],
                "types": infer_types(check["rows"]),
                "quality_score": check["quality_score"]
            }

    claims = []

    from internet.providers.http import get
    from internet.content.cleaner import extract_article_text

    for record in article_records:
        if record.get("evidence_type") != "FULL_ARTICLE":
            continue

        url = record.get("article_url", "")

        if not url:
            continue

        try:
            response = get(url)
        except Exception:
            continue

        if not response["ok"]:
            continue

        try:
            html = response["data"].decode(
                "utf-8",
                errors="ignore"
            )

            article = extract_article_text(html)

            if not article.get("ok"):
                continue

            claims.extend(
                extract(
                    article["text"],
                    source_url=url,
                    title=record.get("title", "")
                )
            )
        except Exception:
            continue

    normalized = normalize(claims)
    gold, rejected = certify(normalized)
    gold = triangulate(gold)

    names = []

    for sheet in validated.values():
        for row in sheet["rows"]:
            for key in (
                "Company",
                "company",
                "Product",
                "product"
            ):
                if row.get(key):
                    names.append(row[key])

    entities = resolve(names)

    semantic = build(gold)
    analytics = analytics_run(gold)

    result = {
        "tabular": {
            "format": table["format"],
            "sheets": list(table["sheets"].keys()),
            "validated": validated
        },
        "claims": {
            "extracted": len(claims),
            "normalized": len(normalized),
            "gold": len(gold),
            "rejected": len(rejected)
        },
        "gold_facts": gold,
        "entities": entities,
        "semantic": semantic,
        "analytics": analytics
    }

    output = Path(
        "storage/gold/pipeline_1_10.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return result
