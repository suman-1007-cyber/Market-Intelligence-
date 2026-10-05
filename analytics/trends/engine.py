import pandas as pd

def growth(df, period="period", value="value"):
    x = df.groupby(period)[value].sum().sort_index()
    return x.pct_change().rename("growth_rate").reset_index()
