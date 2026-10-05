import re

STOPWORDS = {
    "The", "This", "That", "These", "Those",
    "Market", "Industry", "Company", "Companies",
    "India", "Global", "United", "States",
    "Revenue", "Sales", "Growth", "Customers"
}

def detect(text):
    text = text or ""

    candidates = re.findall(
        r"\b[A-Z][A-Za-z0-9&.-]{2,}(?:\s+[A-Z][A-Za-z0-9&.-]{2,}){0,3}\b",
        text
    )

    output = []

    for candidate in candidates:
        candidate = candidate.strip()

        if candidate in STOPWORDS:
            continue

        if candidate not in output:
            output.append(candidate)

    return output[:10]
