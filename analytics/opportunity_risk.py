def assess(market_share=None, growth=None, concentration=None):
    opportunities = []
    risks = []

    if growth is not None:
        if growth > 0.10:
            opportunities.append("High market growth")
        elif growth < 0:
            risks.append("Market contraction")

    if market_share is not None and market_share < 0.10:
        opportunities.append("Low-share expansion opportunity")

    if concentration is not None and concentration > 2500:
        risks.append("High market concentration")

    return {
        "opportunities": opportunities,
        "risks": risks
    }
