import re

YEAR = re.compile(
    r"\b(?:19|20)\d{2}\b"
)

QUARTER = re.compile(
    r"\bQ[1-4]\s*(?:FY)?\s*(?:19|20)?\d{2}\b",
    re.IGNORECASE
)

def detect(text):
    text = text or ""

    quarters = QUARTER.findall(text)

    if quarters:
        return quarters[0]

    years = YEAR.findall(text)

    if years:
        return years[0]

    lower = text.lower()

    if "last year" in lower:
        return "last_year"

    if "this year" in lower:
        return "current_year"

    if "next year" in lower:
        return "next_year"

    return None
