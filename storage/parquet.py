from pathlib import Path
import subprocess
import tempfile
import pandas as pd

def _sql_path(path):
    return str(Path(path).resolve()).replace("'", "''")

def write(df, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        dir="storage/cache",
        delete=False,
        encoding="utf-8"
    ) as f:
        csv_path = Path(f.name)

    try:
        df.to_csv(csv_path, index=False)

        parquet = _sql_path(path)
        csv = _sql_path(csv_path)

        sql = (
            f"COPY (SELECT * FROM read_csv_auto('{csv}')) "
            f"TO '{parquet}' (FORMAT PARQUET);"
        )

        result = subprocess.run(
            ["duckdb", "storage/db/miae.duckdb", "-c", sql],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return path

    finally:
        csv_path.unlink(missing_ok=True)


def read(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        dir="storage/cache",
        delete=False
    ) as f:
        csv_path = Path(f.name)

    try:
        parquet = _sql_path(path)
        csv = _sql_path(csv_path)

        sql = (
            f"COPY (SELECT * FROM read_parquet('{parquet}')) "
            f"TO '{csv}' (HEADER, DELIMITER ',');"
        )

        result = subprocess.run(
            ["duckdb", "storage/db/miae.duckdb", "-c", sql],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return pd.read_csv(csv_path)

    finally:
        csv_path.unlink(missing_ok=True)
