
import re
import hashlib

STOP = {
    "the", "india", "market", "sector",
    "company", "limited", "ltd", "inc"
}

def canonical(name):
    text = str(name or "").lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)

    return " ".join(
        w for w in text.split()
        if w not in STOP
    )

def resolve(names):
    entities = {}
    mapping = {}

    for name in names:
        c = canonical(name)

        if not c:
            continue

        entity_id = "entity_" + hashlib.sha256(
            c.encode()
        ).hexdigest()[:16]

        mapping[name] = entity_id

        entity = entities.setdefault(
            entity_id,
            {
                "entity_id": entity_id,
                "canonical_name": c,
                "aliases": []
            }
        )

        if name not in entity["aliases"]:
            entity["aliases"].append(name)

    return {
        "mapping": mapping,
        "entities": list(entities.values())
    }
