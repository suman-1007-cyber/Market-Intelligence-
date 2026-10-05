from pathlib import Path
import pandas as pd

def load(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix in (".json", ".jsonl"):
        return pd.read_json(path, lines=suffix == ".jsonl")

    if suffix == ".parquet":
        return pd.read_parquet(path)

    raise ValueError(f"Unsupported file type: {suffix}")
