import pandas as pd

def competitor_ranking(df, company="company", value="value"):
    return (
        df.groupby(company)[value]
        .sum()
        .sort_values(ascending=False)
        .reset_index(name=value)
    )

def concentration(df, company="company", value="value"):
    ranked = competitor_ranking(df, company, value)
    total = ranked[value].sum()
    if total == 0:
        return {"hhi": 0.0}
    shares = ranked[value] / total
    return {"hhi": float((shares ** 2).sum() * 10000)}
