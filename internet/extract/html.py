from html.parser import HTMLParser
from pathlib import Path
import re

class TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth == 0:
            text = re.sub(r"\s+", " ", data).strip()
            if text:
                self.parts.append(text)

def extract(path):
    data = Path(path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    parser = TextExtractor()
    parser.feed(data)

    text = "\n".join(parser.parts)

    return {
        "text": text,
        "characters": len(text),
        "words": len(text.split())
    }
