import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analytics.visualization.decision.selector import select


def check(question, rows, expected):
    result = select(question, rows)
    assert result["status"] == "SELECTED"
    assert result["primary_visualization"] == expected
    return result


def main():
    trend = check(
        "How has revenue changed over time?",
        [
            {"year": 2024, "revenue": 100},
            {"year": 2025, "revenue": 120},
        ],
        "line",
    )

    ranking = check(
        "Which competitor has the highest market share?",
        [
            {"company": "A", "market_share": 40},
            {"company": "B", "market_share": 30},
        ],
        "horizontal_bar",
    )

    relationship = check(
        "Is advertising spend related to sales?",
        [
            {"ad_spend": 100, "sales": 500},
            {"ad_spend": 150, "sales": 620},
        ],
        "scatter",
    )

    distribution = check(
        "What is the distribution of customer revenue?",
        [
            {"revenue": 100},
            {"revenue": 150},
            {"revenue": 200},
        ],
        "histogram",
    )

    composition = check(
        "What is the market share composition?",
        [
            {"company": "A", "share": 40},
            {"company": "B", "share": 35},
            {"company": "C", "share": 25},
        ],
        "stacked_bar",
    )

    forecast = check(
        "Show actual versus forecast revenue over time.",
        [
            {"year": 2024, "actual": 100},
            {"year": 2025, "actual": 120},
        ],
        "forecast_line",
    )

    outlier = check(
        "Find unusual customer values.",
        [
            {"customer": "A", "value": 10},
            {"customer": "B", "value": 12},
            {"customer": "C", "value": 100},
        ],
        "box_plot",
    )

    geographic = check(
        "Compare sales by geographic region.",
        [
            {"region": "West", "sales": 100},
            {"region": "East", "sales": 120},
        ],
        "map",
    )

    flow = check(
        "Show customer movement from source to destination.",
        [
            {"source": "A", "destination": "B", "value": 10},
            {"source": "B", "destination": "C", "value": 8},
        ],
        "sankey",
    )

    assert "alternative_visualizations" in trend
    assert len(ranking["alternative_visualizations"]) >= 1
    assert len(relationship["alternative_visualizations"]) >= 1
    assert len(distribution["alternative_visualizations"]) >= 1
    assert len(composition["alternative_visualizations"]) >= 1
    assert len(forecast["alternative_visualizations"]) >= 1
    assert len(outlier["alternative_visualizations"]) >= 1
    assert len(geographic["alternative_visualizations"]) >= 1
    assert len(flow["alternative_visualizations"]) >= 1

    print("==============================================")
    print(" VISUALIZATION INTELLIGENCE ENGINE")
    print("==============================================")
    print("Trend selection          : PASS")
    print("Ranking selection        : PASS")
    print("Relationship selection  : PASS")
    print("Distribution selection  : PASS")
    print("Composition selection   : PASS")
    print("Forecast selection      : PASS")
    print("Outlier selection       : PASS")
    print("Geographic selection    : PASS")
    print("Flow selection          : PASS")
    print("Alternative selection   : PASS")
    print("----------------------------------------------")
    print("Visualization intelligence: PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
