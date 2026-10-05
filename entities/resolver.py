import re

def normalize_name(value):
    if value is None:
        return None
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def resolve(values):
    return {v: normalize_name(v) for v in values}
