"""Data Quality Agent subsystem."""

from .agent import DataQualityAgent
from .anomalies import detect as detect_anomalies
from .duplicates import detect as detect_duplicates
from .inspector import inspect
from .investigator import investigate
from .missing import analyze as analyze_missing
from .schema import compare

__all__ = [
    "DataQualityAgent",
    "inspect",
    "analyze_missing",
    "detect_duplicates",
    "detect_anomalies",
    "compare",
    "investigate",
]
