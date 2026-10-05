from xml.etree import ElementTree as ET
from urllib.parse import urljoin

def _text(element):
    if element is None:
        return ""

    return " ".join(
        "".join(element.itertext()).split()
    )

def parse(data, base_url=""):
    root = ET.fromstring(data)

    results = []

    for item in root.findall(".//item"):
        title = _text(item.find("title"))
        link = _text(item.find("link"))
        description = _text(item.find("description"))
        pubdate = _text(item.find("pubDate"))

        if link:
            link = urljoin(base_url, link)

        results.append({
            "title": title,
            "url": link,
            "description": description,
            "published": pubdate
        })

    atom_ns = "{http://www.w3.org/2005/Atom}"

    for entry in root.findall(
        f".//{atom_ns}entry"
    ):
        title = _text(entry.find(f"{atom_ns}title"))
        summary = _text(entry.find(f"{atom_ns}summary"))
        updated = _text(entry.find(f"{atom_ns}updated"))

        link = ""

        for element in entry.findall(
            f"{atom_ns}link"
        ):
            href = element.attrib.get("href")

            if href:
                link = urljoin(base_url, href)
                break

        if link:
            results.append({
                "title": title,
                "url": link,
                "description": summary,
                "published": updated
            })

    return results
