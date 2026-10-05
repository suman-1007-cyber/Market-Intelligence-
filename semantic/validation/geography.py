GEOGRAPHIES = {
    "india": "India",
    "united states": "United States",
    "usa": "United States",
    "us": "United States",
    "china": "China",
    "japan": "Japan",
    "uk": "United Kingdom",
    "united kingdom": "United Kingdom",
    "europe": "Europe",
    "asia": "Asia",
    "asia pacific": "Asia Pacific",
    "global": "Global",
    "worldwide": "Global"
}

def detect(text):
    lower = (text or "").lower()

    matches = []

    for key, value in GEOGRAPHIES.items():
        if key in lower:
            matches.append(value)

    return list(dict.fromkeys(matches))
