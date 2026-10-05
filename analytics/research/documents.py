"""Document/PDF research normalization."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchDocument:
    source_url: str
    title: str
    text: str
    document_type: str = "document"
    pages: int | None = None


def normalize(
    source_url: str,
    title: str,
    text: str,
    document_type: str = "document",
    pages: int | None = None,
) -> ResearchDocument:
    if not source_url:
        raise ValueError("Document source URL is required.")

    if not text.strip():
        raise ValueError("Document text cannot be empty.")

    return ResearchDocument(
        source_url=source_url,
        title=title,
        text=text,
        document_type=document_type,
        pages=pages,
    )
