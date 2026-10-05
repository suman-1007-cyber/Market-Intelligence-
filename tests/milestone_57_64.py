"""Integration test for Research Agent milestones 57-64."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analytics.research import (
    DeepResearchAgent,
    discover,
    ingest_document,
    plan,
    synthesize,
    verify,
)


def main() -> None:
    print("=" * 46)
    print(" RESEARCH AGENT — MILESTONES 57–64")
    print("=" * 46)

    research_plan = plan(
        "What is the market growth trend?"
    )

    assert research_plan.steps
    assert "discover_sources" in research_plan.steps
    print("57 Research Planner         : PASS")

    sources = discover([
        {
            "url": "https://example.com/source-a",
            "title": "Source A",
            "publisher": "Publisher A",
            "authority": 0.9,
        },
        {
            "url": "https://example.com/source-b",
            "title": "Source B",
            "publisher": "Publisher B",
            "authority": 0.8,
        },
    ])

    assert len(sources) == 2
    print("58 Source Discovery         : PASS")

    document = ingest_document(
        "https://example.com/article",
        "Market Article",
        "Market evidence text.",
    )

    assert document.text == "Market evidence text."
    print("59 Web Research             : PASS")

    news = [
        {
            "title": "Market Update",
            "url": "https://example.com/news",
            "publisher": "Example News",
        }
    ]

    from analytics.research.news import normalize

    normalized_news = normalize(news)

    assert len(normalized_news) == 1
    print("60 News Intelligence        : PASS")

    from analytics.research.documents import normalize as normalize_doc

    normalized_doc = normalize_doc(
        "https://example.com/report.pdf",
        "Report",
        "PDF-derived evidence.",
        "pdf",
        5,
    )

    assert normalized_doc.pages == 5
    print("61 Document/PDF Research    : PASS")

    checked = verify(
        "Market grew",
        [
            "https://example.com/source-a",
            "https://example.com/source-b",
        ],
    )

    assert checked.verified
    assert checked.confidence == 1.0
    print("62 Evidence Verification   : PASS")

    synthesis = synthesize([])

    assert synthesis["finding_count"] == 0
    print("63 Research Synthesis       : PASS")

    agent = DeepResearchAgent()

    result = agent.investigate(
        "Did the market grow?",
        [
            {"url": "https://example.com/a"},
            {"url": "https://example.com/b"},
        ],
        [
            {
                "claim": "Market grew",
                "supporting_sources": [
                    "https://example.com/a",
                    "https://example.com/b",
                ],
            }
        ],
    )

    assert result["agent_id"] == "deep-research-agent"
    assert result["verification"][0].verified
    assert result["synthesis"]["verified_count"] == 1
    print("64 Deep Research Agent     : PASS")

    print("-" * 46)
    print("RESEARCH AGENT : PASS")
    print("=" * 46)


if __name__ == "__main__":
    main()
