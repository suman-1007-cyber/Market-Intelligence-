"""Research web retrieval adapter.

This module deliberately accepts retrieved documents as input.
Network acquisition remains delegated to the existing internet layer.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WebDocument:
    url: str
    title: str
    text: str
    retrieved_at: str = ""


def ingest_document(
    url: str,
    title: str,
    text: str,
    retrieved_at: str = "",
) -> WebDocument:
    if not url:
        raise ValueError("Document URL is required.")

    if not text or not text.strip():
        raise ValueError("Document text is required.")

    return WebDocument(
        url=url,
        title=title,
        text=text.strip(),
        retrieved_at=retrieved_at,
    )
