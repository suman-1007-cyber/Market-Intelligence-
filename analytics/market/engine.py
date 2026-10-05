import pandas as pd

def market_share(df, value="value", entity="company"):
    total = df[value].sum()
    out = df.groupby(entity, dropna=False)[value].sum().reset_index()
    out["market_share"] = 0.0 if total == 0 else out[value] / total
    return out.sort_values("market_share", ascending=False)

def market_summary(df, value="value"):
    return {
        "total_market": float(df[value].sum()),
        "average_value": float(df[value].mean()),
        "median_value": float(df[value].median()),
        "observations": int(len(df))
    }
