from analytics.market.engine import market_share, market_summary
from analytics.competitive.engine import competitor_ranking, concentration
from analytics.forecasting.engine import linear_forecast
from analytics.opportunity_risk import assess

def analyze(df):
    result = {
        "rows": int(len(df))
    }

    if "value" in df.columns:
        result["market"] = market_summary(df)
        if "company" in df.columns:
            result["market_share"] = market_share(df).to_dict("records")
            result["competitor_ranking"] = competitor_ranking(df).to_dict("records")
            result["concentration"] = concentration(df)

        values = df["value"].astype(float).tolist()

        if len(values) >= 3:
            result["forecast"] = linear_forecast(values, 4)

            if len(values) >= 2 and values[-2] != 0:
                recent_growth = (
                    values[-1] - values[-2]
                ) / abs(values[-2])

                result["recent_growth"] = recent_growth
                result["opportunity_risk"] = assess(
                    growth=recent_growth,
                    concentration=result.get("concentration", {}).get("hhi")
                )

    return result
