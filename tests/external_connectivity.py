from internet.providers.router import search

result = search(
    "India technology market",
    limit=5
)

print("==============================================")
print(" EXTERNAL SOURCE CONNECTIVITY TEST")
print("==============================================")
print("Provider:", result.get("provider"))
print("Results :", len(result.get("results", [])))

for item in result.get("results", []):
    print("----------------------------------------------")
    print("Title:", item.get("title"))
    print("URL  :", item.get("url"))

print("==============================================")

if not result.get("results"):
    print("EXTERNAL SEARCH: NO RESULTS")
    print("This indicates network/provider access failure.")
else:
    print("EXTERNAL SEARCH: PASS")
