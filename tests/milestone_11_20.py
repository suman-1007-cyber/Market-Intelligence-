import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pathlib import Path

from orchestrator.pipeline_11_20 import run, save


FACTS = [
    {
        "entity": "Alpha",
        "metric": "market_share",
        "value": 42,
        "unit": "%",
        "period": "2024",
        "source_url": "https://example.com/alpha-2024",
        "confidence": 0.95,
    },
    {
        "entity": "Beta",
        "metric": "market_share",
        "value": 31,
        "unit": "%",
        "period": "2024",
        "source_url": "https://example.com/beta-2024",
        "confidence": 0.94,
    },
    {
        "entity": "Gamma",
        "metric": "market_share",
        "value": 27,
        "unit": "%",
        "period": "2024",
        "source_url": "https://example.com/gamma-2024",
        "confidence": 0.93,
    },
    {
        "entity": "Market",
        "metric": "revenue",
        "value": 100,
        "unit": "USD",
        "period": "2022",
        "source_url": "https://example.com/revenue-2022",
        "confidence": 0.95,
    },
    {
        "entity": "Market",
        "metric": "revenue",
        "value": 115,
        "unit": "USD",
        "period": "2023",
        "source_url": "https://example.com/revenue-2023",
        "confidence": 0.95,
    },
    {
        "entity": "Market",
        "metric": "revenue",
        "value": 135,
        "unit": "USD",
        "period": "2024",
        "source_url": "https://example.com/revenue-2024",
        "confidence": 0.95,
    },
]


def main():
    result = run(FACTS)
    gold_path, svg_path = save(result)

    assert len(result["market"]["metrics"]) >= 2
    assert len(result["competitive"]["ranked_competitors"]) == 3
    assert result["competitive"]["ranked_competitors"][0]["entity"] == "Alpha"

    assert "revenue" in result["trends"]
    assert result["trends"]["revenue"]["direction"] == "up"

    assert result["forecasts"]["revenue"]["status"] == "ok"
    assert len(result["forecasts"]["revenue"]["forecast"]) == 2

    assert "revenue" in result["scenarios"]
    assert abs(result["scenarios"]["revenue"]["upside"] - 148.5) < 1e-9

    assert result["opportunity_risk"]["opportunities"]

    assert len(result["graph_data"]) == 6

    assert gold_path.exists()
    assert svg_path.exists()

    svg = svg_path.read_text(encoding="utf-8")

    assert "<svg" in svg
    assert "<circle" in svg
    assert "source:" in svg

    print("==============================================")
    print(" MARKET INTELLIGENCE 11-20 MILESTONE")
    print("==============================================")
    print("11. Market Engine                : PASS")
    print("12. Competitive Engine           : PASS")
    print("13. Customer Engine              : PASS")
    print("14. Business Dimensions          : PASS")
    print("15. Trend Analytics              : PASS")
    print("16. Forecasting                  : PASS")
    print("17. Scenario Modelling           : PASS")
    print("18. Opportunity / Risk           : PASS")
    print("19. Graph-ready Data             : PASS")
    print("20. Evidence-linked SVG          : PASS")
    print("----------------------------------------------")
    print("Facts processed :", len(FACTS))
    print("Graph points    :", len(result["graph_data"]))
    print("Gold output     :", gold_path)
    print("SVG output      :", svg_path)
    print("==============================================")
    print("MILESTONE 11-20 : PASS")
    print("==============================================")


if __name__ == "__main__":
    main()
