from pathlib import Path
import json

PATH = Path("sources/registry.json")

DEFAULT = {
    "sources": [
        {
            "id": "official_company",
            "type": "official_company",
            "authority": 0.95,
            "enabled": True
        },
        {
            "id": "government",
            "type": "official_government",
            "authority": 1.00,
            "enabled": True
        },
        {
            "id": "regulatory",
            "type": "regulatory_filing",
            "authority": 0.98,
            "enabled": True
        },
        {
            "id": "research",
            "type": "recognized_research",
            "authority": 0.85,
            "enabled": True
        },
        {
            "id": "news",
            "type": "reputable_news",
            "authority": 0.75,
            "enabled": True
        }
    ]
}

def ensure():
    PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PATH.exists():
        PATH.write_text(json.dumps(DEFAULT, indent=2), encoding="utf-8")
    return json.loads(PATH.read_text(encoding="utf-8"))

def enabled():
    return [x for x in ensure()["sources"] if x.get("enabled", True)]
