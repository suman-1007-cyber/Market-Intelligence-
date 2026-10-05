import json
from internet.news.resolver import resolve


data = json.load(
    open(
        "storage/silver/intelligence/investigation.json",
        encoding="utf-8"
    )
)

item = data["documents"][0]

title = item.get("title", "")

if " - " in title:
    clean_title, publisher = title.rsplit(" - ", 1)
else:
    clean_title = title
    publisher = ""

print("==============================================")
print(" NEWS ARTICLE RESOLVER TEST")
print("==============================================")
print("TITLE    :", clean_title)
print("PUBLISHER:", publisher)
print("----------------------------------------------")

result = resolve(
    title=clean_title,
    publisher=publisher,
    exclude_url=item.get("url", "")
)

print("Resolved :", result["ok"])

if result["ok"]:
    print("Article  :", result["article_url"])
    print("Provider :", result["provider"])
    print("Score    :", result["score"])
    print("Text     :", len(result["text"]), "chars")
    print("Status   : PASS")
else:
    print("Reason   :", result["reason"])
    print("Status   : RESOLUTION_FAILED")

print("==============================================")
