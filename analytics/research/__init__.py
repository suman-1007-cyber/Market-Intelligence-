"""Research Agent subsystem."""

from .agent import DeepResearchAgent
from .documents import ResearchDocument
from .news import NewsItem
from .planner import ResearchPlan, plan
from .sources import ResearchSource, discover
from .synthesis import ResearchFinding, synthesize
from .verify import VerifiedClaim, verify
from .web import WebDocument, ingest_document

__all__ = [
    "DeepResearchAgent",
    "ResearchPlan",
    "ResearchSource",
    "ResearchDocument",
    "WebDocument",
    "NewsItem",
    "VerifiedClaim",
    "ResearchFinding",
    "plan",
    "discover",
    "ingest_document",
    "verify",
    "synthesize",
]
