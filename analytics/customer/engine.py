def customer_summary(df, customer="customer", value="value"):
    unique = int(df[customer].nunique()) if customer in df.columns else 0
    total = float(df[value].sum()) if value in df.columns else 0.0
    return {
        "unique_customers": unique,
        "total_value": total,
        "average_value": total / unique if unique else 0.0
    }
