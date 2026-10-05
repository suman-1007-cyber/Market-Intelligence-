VALID_UNITS = {
    None,
    "percent",
    "absolute",
    "million",
    "billion",
    "trillion",
    "crore",
    "lakh"
}

CURRENCY = {
    "USD", "INR", "EUR", "GBP",
    "$", "₹", "€", "£"
}

def validate(row):
    unit = row.get("unit")
    currency = row.get("currency")

    valid_unit = unit in VALID_UNITS

    valid_currency = (
        currency is None
        or currency in CURRENCY
    )

    value = row.get("normalized_value")

    numeric = isinstance(
        value,
        (int, float)
    )

    return {
        "valid_unit": valid_unit,
        "valid_currency": valid_currency,
        "numeric": numeric,
        "valid": (
            valid_unit
            and valid_currency
            and numeric
        )
    }
