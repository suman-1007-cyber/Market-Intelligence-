def total(df, column):
    return float(df[column].sum())

def average(df, column):
    return float(df[column].mean())

def median(df, column):
    return float(df[column].median())

def growth(current, previous):
    if previous == 0:
        return None

    return (current - previous) / previous

def share(value, total_value):
    if total_value == 0:
        return 0.0

    return value / total_value
