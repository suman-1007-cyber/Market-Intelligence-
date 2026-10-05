from datetime import datetime, timezone


def parse_timestamp(value):
    if not value:
        return None

    text = str(value).strip()

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def assess(retrieved_at, max_age_days, now=None):
    retrieved = parse_timestamp(retrieved_at)

    if retrieved is None:
        return {
            "status": "unknown",
            "age_days": None,
            "max_age_days": float(max_age_days),
        }

    current = (
        parse_timestamp(now)
        if now
        else datetime.now(timezone.utc)
    )

    age_days = (current - retrieved).total_seconds() / 86400

    if age_days < 0:
        status = "future_timestamp"
    elif age_days <= float(max_age_days):
        status = "fresh"
    else:
        status = "stale"

    return {
        "status": status,
        "age_days": age_days,
        "max_age_days": float(max_age_days),
    }
