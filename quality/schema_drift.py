def detect_schema_drift(previous, current):
    old = {f["name"]: f for f in previous.get("fields", [])}
    new = {f["name"]: f for f in current.get("fields", [])}

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []

    for name in sorted(set(old) & set(new)):
        if old[name].get("data_type") != new[name].get("data_type"):
            changed.append({
                "field": name,
                "from": old[name].get("data_type"),
                "to": new[name].get("data_type"),
            })

    return {
        "drift": bool(added or removed or changed),
        "added": added,
        "removed": removed,
        "changed": changed,
    }
