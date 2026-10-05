def geography_summary(df, geography="geography", value="value"):
    return (
        df.groupby(geography)[value]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
