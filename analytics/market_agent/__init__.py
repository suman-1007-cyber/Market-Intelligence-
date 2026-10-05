"""Market Intelligence Agent package."""

from .agent import MarketIntelligenceAgent
from .intelligence import synthesize
from .opportunity import analyze as analyze_opportunity
from .sizing import analyze as analyze_sizing
from .trends import analyze as analyze_trend

__all__ = [
    "MarketIntelligenceAgent",
    "synthesize",
    "analyze_opportunity",
    "analyze_sizing",
    "analyze_trend",
]
