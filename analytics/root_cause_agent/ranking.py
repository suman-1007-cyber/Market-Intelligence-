from __future__ import annotations

from typing import Any


def rank(
    drivers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ranked = []

    for index, driver in enumerate(drivers, start=1):
        item = dict(driver)
        item["rank"] = index

        strength = item["absolute_correlation"]

        if strength >= 0.70:
            item["strength"] = "HIGH"
        elif strength >= 0.40:
            item["strength"] = "MEDIUM"
        else:
            item["strength"] = "LOW"

        ranked.append(item)

    return ranked
