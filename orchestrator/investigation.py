from pathlib import Path
import pandas as pd

from orchestrator.planner import plan
from sources.discovery import discover
from quality.certification import certify
from quality.triangulation import compare
from evidence.provenance import all as all_evidence
from analytics.pipeline import analyze
from reports.evidence_report import generate

def run(question, data_path=None):
    investigation_plan = plan(question)
    source_plan = discover(question)

    quality = {
        "source_discovery": source_plan,
        "data": None
    }

    analysis = {}
    dataset = None

    if data_path:
        path = Path(data_path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() == ".csv":
            dataset = pd.read_csv(path)
        elif path.suffix.lower() == ".parquet":
            dataset = pd.read_parquet(path)
        else:
            raise ValueError("Supported data files: CSV, Parquet")

        certification = certify(dataset)
        quality["data"] = certification

        if certification["certified"]:
            analysis = analyze(dataset)
        else:
            analysis = {
                "status": "analysis_blocked",
                "reason": "data_not_certified"
            }

    evidence = all_evidence()
    triangulation = compare(evidence)

    report = generate(
        question,
        {
            "investigation": investigation_plan,
            "sources": source_plan
        },
        quality,
        analysis,
        evidence,
        triangulation
    )

    return {
        "question": question,
        "plan": investigation_plan,
        "sources": source_plan,
        "quality": quality,
        "analysis": analysis,
        "evidence_count": len(evidence),
        "triangulation": triangulation,
        "report": str(report)
    }
