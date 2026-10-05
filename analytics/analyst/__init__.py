"""Data Analyst Agent subsystem."""

from .agent import DataAnalyst
from .discovery import discover
from .eda import profile
from .findings import AnalystFinding
from .statistics import analyze as analyze_statistics
from .relationships import analyze as analyze_relationships
from .distributions import analyze as analyze_distributions
from .insights import detect

__all__ = [
    "DataAnalyst",
    "AnalystFinding",
    "discover",
    "profile",
    "analyze_statistics",
    "analyze_relationships",
    "analyze_distributions",
    "detect",
]
