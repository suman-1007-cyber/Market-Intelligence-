"""Pricing intelligence aggregation."""

from typing import Any

from .analysis import analyze as analyze_price
from .competitive import analyze as analyze_competitive
from .discounts import analyze as analyze_discount
from .elasticity import analyze as analyze_elasticity
from .opportunity import analyze as analyze_opportunity
from .optimization import optimize
from .risk import analyze as analyze_risk


def analyze(
    current_price: float,
    cost: float,
    units: float,
    competitor_prices: list[float],
    old_price: float,
    new_price: float,
    old_quantity: float,
    new_quantity: float,
    list_price: float | None = None,
    candidate_prices: list[float] | None = None,
    expected_units: list[float] | None = None,
) -> dict[str, Any]:
    if list_price is None:
        list_price = current_price

    if candidate_prices is None:
        candidate_prices = [current_price]

    if expected_units is None:
        expected_units = [units]

    price_analysis = analyze_price(
        price=current_price,
        cost=cost,
        units=units,
    )

    competitive_analysis = analyze_competitive(
        own_price=current_price,
        competitor_prices=competitor_prices,
    )

    elasticity = analyze_elasticity(
        old_price=old_price,
        new_price=new_price,
        old_quantity=old_quantity,
        new_quantity=new_quantity,
    )

    discount = analyze_discount(
        list_price=list_price,
        selling_price=current_price,
        units=units,
    )

    optimization = optimize(
        current_price=current_price,
        cost=cost,
        candidate_prices=candidate_prices,
        expected_units=expected_units,
    )

    risk = analyze_risk(
        price_analysis,
        competitive_analysis,
        discount,
    )

    opportunity = analyze_opportunity(
        optimization,
        competitive_analysis,
        elasticity,
    )

    return {
        "price": price_analysis,
        "competitive": competitive_analysis,
        "elasticity": elasticity,
        "discount": discount,
        "optimization": optimization,
        "risk": risk,
        "opportunity": opportunity,
    }
