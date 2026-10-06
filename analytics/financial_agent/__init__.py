"""Financial Intelligence package."""

from .agent import FinancialIntelligenceAgent
from .cashflow import analyze as analyze_cashflow
from .data import normalize, normalize_many
from .forecast import forecast
from .health import analyze as analyze_health
from .intelligence import analyze as analyze_financial_intelligence
from .opportunity import analyze as analyze_opportunity
from .profitability import analyze as analyze_profitability
from .ratios import analyze as analyze_ratios
from .risk import analyze as analyze_risk
from .trends import analyze as analyze_trends

__all__ = [
    "FinancialIntelligenceAgent",
    "normalize",
    "normalize_many",
    "analyze_profitability",
    "analyze_cashflow",
    "analyze_ratios",
    "analyze_trends",
    "analyze_health",
    "analyze_risk",
    "forecast",
    "analyze_opportunity",
    "analyze_financial_intelligence",
]
