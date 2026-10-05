def forecast(values, periods=1):
    values = [float(v) for v in values]

    if len(values) < 2:
        return {
            "status": "insufficient_data",
            "forecast": [],
        }

    n = len(values)
    x = list(range(n))

    mean_x = sum(x) / n
    mean_y = sum(values) / n

    denominator = sum(
        (xi - mean_x) ** 2
        for xi in x
    )

    if denominator == 0:
        slope = 0.0
    else:
        slope = sum(
            (xi - mean_x) * (yi - mean_y)
            for xi, yi in zip(x, values)
        ) / denominator

    intercept = mean_y - slope * mean_x

    predictions = []

    for step in range(1, int(periods) + 1):
        future_x = n - 1 + step
        predicted = intercept + slope * future_x

        predictions.append({
            "period_offset": step,
            "value": predicted,
        })

    return {
        "status": "ok",
        "method": "linear_regression",
        "slope": slope,
        "intercept": intercept,
        "forecast": predictions,
    }
