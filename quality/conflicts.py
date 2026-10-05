def detect_conflicts(df, keys, value_column):
    if not all(k in df.columns for k in keys):
        return []
    g = df.groupby(keys)[value_column].nunique(dropna=True)
    return g[g > 1].reset_index().to_dict("records")
