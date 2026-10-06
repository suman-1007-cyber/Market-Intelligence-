from __future__ import annotations

from typing import Any


def arrange(sections: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(sections, list):
        raise TypeError("sections must be a list")

    return {
        "section_count": len(sections),
        "sections": [
            {
                "id": str(item.get("id", index)),
                "title": str(item.get("title", "")),
                "order": index,
            }
            for index, item in enumerate(sections)
            if isinstance(item, dict)
        ],
    }
