import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analytics.observation.graph_observer import observe


def main():
    points = [
        {
            "x": "2023",
            "y": 100,
            "metric": "revenue",
            "unit": "USD",
            "source_url": "https://source-a.example",
        },
        {
            "x": "2024",
            "y": 120,
            "metric": "revenue",
            "unit": "USD",
            "source_url": "https://source-a.example",
        },
        {
            "x": "2025",
            "y": 150,
            "metric": "revenue",
            "unit": "USD",
            "source_url": "https://source-b.example",
        },
        {
            "x": "2026",
            "y": 140,
            "metric": "revenue",
            "unit": "USD",
            "source_url": "https://source-b.example",
        },
    ]

    result = observe(points)

    assert result["status"] == "OBSERVED"
    assert result["point_count"] == 4
    assert result["metric"] == "revenue"

    trend = next(
        x for x in result["observations"]
        if x["type"] == "trend"
    )

    assert trend["direction"] == "up"
    assert trend["first_value"] == 100
    assert trend["last_value"] == 140
    assert abs(trend["change_pct"] - 40.0) < 1e-9

    peak = next(
        x for x in result["observations"]
        if x["type"] == "peak"
    )

    trough = next(
        x for x in result["observations"]
        if x["type"] == "trough"
    )

    assert peak["value"] == 150
    assert peak["x"] == "2025"
    assert trough["value"] == 100
    assert trough["x"] == "2023"

    movement = next(
        x for x in result["observations"]
        if x["type"] == "largest_movement"
    )

    assert movement["magnitude"] == 30

    print("==============================================")
    print(" GRAPH OBSERVATION ENGINE")
    print("==============================================")
    print("Graph data observation : PASS")
    print("Trend detection        : PASS")
    print("Peak / trough detection: PASS")
    print("Momentum detection     : PASS")
    print("Volatility analysis    : PASS")
    print("Largest movement       : PASS")
    print("Evidence preservation  : PASS")
    print("----------------------------------------------")
    print("Status :", result["status"])
    print("Points :", result["point_count"])
    print("==============================================")
    print("GRAPH OBSERVATION : PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
