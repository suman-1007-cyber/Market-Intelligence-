def scenario(value, changes):
    base = float(value)

    results = {}

    for name, change in changes.items():
        adjusted = base * (1.0 + float(change))
        results[name] = adjusted

    return results
