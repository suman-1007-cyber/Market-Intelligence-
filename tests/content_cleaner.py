from internet.content.cleaner import extract_article_text

google_html = """
<html>
<style>body{font-family:Google Sans} .abc{color:red}</style>
<script>var x=1;</script>
<body>
Google Search
Sign in
Google News
Google Apps
</body>
</html>
"""

result = extract_article_text(google_html)

assert result["ok"] is False
assert result["reason"] == "google_ui_or_non_article"

article_html = """
<html>
<head><title>Market Growth</title></head>
<body>
<article>
The global technology market grew significantly during 2026.
Companies reported higher revenue and stronger customer demand.
The market is expected to continue expanding over the next year.
</article>
</body>
</html>
"""

result = extract_article_text(article_html)

assert result["ok"] is True
assert "global technology market" in result["text"]

print("==============================================")
print(" ARTICLE CONTENT CLEANER TEST")
print("==============================================")
print("Google UI rejection : PASS")
print("Article extraction  : PASS")
print("Garbage filtering    : PASS")
print("==============================================")
