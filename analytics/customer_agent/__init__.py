"""Customer Intelligence package."""

from .agent import CustomerIntelligenceAgent
from .behavior import analyze as analyze_behavior
from .churn import analyze as analyze_churn
from .cohorts import analyze as analyze_cohorts
from .ltv import calculate
from .opportunity import analyze as analyze_opportunity
from .profiling import profile
from .retention import analyze as analyze_retention
from .risk import analyze as analyze_risk
from .segmentation import segment

__all__ = [
    "CustomerIntelligenceAgent",
    "segment",
    "profile",
    "analyze_cohorts",
    "analyze_retention",
    "analyze_churn",
    "calculate",
    "analyze_behavior",
    "analyze_opportunity",
    "analyze_risk",
]
