import numpy as np

def linear_forecast(values, horizon=4):
    y = np.asarray(values, dtype=float)
    if len(y) < 3:
        return []
    x = np.arange(len(y), dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(y), len(y) + horizon)
    return [float(slope * i + intercept) for i in future_x]
