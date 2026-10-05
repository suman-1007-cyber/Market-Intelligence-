def financial_summary(df, revenue="revenue"):
    if revenue not in df.columns:
        return {}
    return {
        "total_revenue": float(df[revenue].sum()),
        "average_revenue": float(df[revenue].mean()),
        "minimum_revenue": float(df[revenue].min()),
        "maximum_revenue": float(df[revenue].max())
    }
