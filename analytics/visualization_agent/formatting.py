from __future__ import annotations


def format_number(value: float, decimals: int = 2) -> str:
    decimals = max(0, min(6, int(decimals)))
    return f"{float(value):,.{decimals}f}"


def format_percent(value: float, decimals: int = 1) -> str:
    decimals = max(0, min(6, int(decimals)))
    return f"{float(value) * 100:.{decimals}f}%"
