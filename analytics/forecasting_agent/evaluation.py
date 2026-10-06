from __future__ import annotations

from typing import Any, Iterable


def evaluate(actual: Iterable[float], predicted: Iterable[float]) -> dict[str, Any]:
    actual_values = [float(value) for value in actual]
    predicted_values = [float(value) for value in predicted]

    if not actual_values or not predicted_values:
        raise ValueError("actual and predicted must not be empty")

    if len(actual_values) != len(predicted_values):
        raise ValueError("actual and predicted must have equal length")

    errors = [
        actual_value - predicted_value
        for actual_value, predicted_value in zip(actual_values, predicted_values)
    ]

    absolute_errors = [abs(error) for error in errors]
    mae = sum(absolute_errors) / len(absolute_errors)

    non_zero_actual = [
        abs(value)
        for value in actual_values
        if value != 0
    ]

    if non_zero_actual:
        mape = (
            sum(
                abs(error) / abs(actual_value)
                for error, actual_value in zip(errors, actual_values)
                if actual_value != 0
            )
            / len(non_zero_actual)
        )
    else:
        mape = None

    return {
        "mae": mae,
        "mape": mape,
        "errors": errors,
        "count": len(errors),
    }
