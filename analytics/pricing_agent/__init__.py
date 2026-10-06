"""Pricing Intelligence package."""

from .agent import PricingIntelligenceAgent
from .analysis import analyze as analyze_price
from .competitive import analyze as analyze_competitive_pricing
from .data import normalize, normalize_many
from .discounts import analyze as analyze_discount
from .elasticity import analyze as analyze_elasticity
from .intelligence import analyze as analyze_pricing_intelligence
from .opportunity import analyze as analyze_pricing_opportunity
from .optimization import optimize
from .risk import analyze as analyze_pricing_risk
from .segmentation import segment

__all__ = [
    "PricingIntelligenceAgent",
    "normalize",
    "normalize_many",
    "analyze_price",
    "analyze_elasticity",
    "analyze_competitive_pricing",
    "segment",
    "analyze_discount",
    "optimize",
    "analyze_pricing_risk",
    "analyze_pricing_opportunity",
    "analyze_pricing_intelligence",
]
