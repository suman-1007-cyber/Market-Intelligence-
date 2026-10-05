def duplicate_report(df):
    return {
        "duplicates": int(df.duplicated().sum()),
        "rows": int(len(df))
    }
