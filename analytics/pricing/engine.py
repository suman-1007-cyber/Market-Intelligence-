def pricing_summary(df, price="price"):
    if price not in df.columns:
        return {}
    return {
        "average_price": float(df[price].mean()),
        "median_price": float(df[price].median()),
        "minimum_price": float(df[price].min()),
        "maximum_price": float(df[price].max())
    }
