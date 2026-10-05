import re
from html import unescape
from html.parser import HTMLParser

class ArticleTextParser(HTMLParser):
    SKIP = {
        "script", "style", "noscript", "svg",
        "path", "iframe", "nav", "footer", "header"
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth:
            return

        text = re.sub(r"\s+", " ", data).strip()

        if len(text) >= 25:
            self.parts.append(text)

def clean_html(html):
    if not html:
        return ""

    parser = ArticleTextParser()

    try:
        parser.feed(html)
        parser.close()
    except Exception:
        return ""

    text = "\n".join(parser.parts)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

def is_google_ui(text):
    if not text:
        return True

    lower = text.lower()

    ui_markers = [
        "google search",
        "sign in",
        "google news",
        "google apps",
    ]

    hits = sum(marker in lower for marker in ui_markers)

    # Google wrapper pages commonly expose several UI labels together.
    if hits >= 2:
        return True

    return False


def extract_article_text(html):
    text = clean_html(html)

    if is_google_ui(text):
        return {
            "ok": False,
            "reason": "google_ui_or_non_article",
            "text": ""
        }

    if len(text) < 120:
        return {
            "ok": False,
            "reason": "insufficient_article_text",
            "text": ""
        }

    return {
        "ok": True,
        "reason": "article_text",
        "text": text
    }
