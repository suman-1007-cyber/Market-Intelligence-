import re

def normalize(value):
    if value is None:
        return None

    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def normalize_column(df, column):
    if column in df.columns:
        df[column] = df[column].map(normalize)

    return df
