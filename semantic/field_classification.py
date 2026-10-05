def classify_field(name, data_type):
    n = name.lower().strip()
    if any(x in n for x in ("date", "period", "month", "year", "time", "timestamp")):
        return "time"
    if any(x in n for x in ("company", "competitor", "customer", "product", "brand", "entity")):
        return "entity"
    if any(x in n for x in ("country", "state", "city", "region", "geography", "location")):
        return "geography"
    if any(x in n for x in ("revenue", "sales", "price", "cost", "profit", "volume", "share", "rate", "count", "amount")):
        return "measure"
    if data_type == "numeric":
        return "measure"
    return "dimension"
