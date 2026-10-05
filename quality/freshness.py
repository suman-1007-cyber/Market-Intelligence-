import pandas as pd

def check_date_column(df, column):
    if column not in df.columns:
        return {"valid": False, "error": f"Missing column: {column}"}
    dates = pd.to_datetime(df[column], errors="coerce")
    return {
        "valid": bool(dates.notna().any()),
        "min": str(dates.min()),
        "max": str(dates.max())
    }
