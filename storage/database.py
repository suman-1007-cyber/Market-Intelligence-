from pathlib import Path
import subprocess

DB = Path("storage/db/miae.duckdb")

def query(sql: str):
    DB.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(
        ["duckdb", str(DB), "-csv", "-c", sql],
        text=True, capture_output=True
    )
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p.stdout

def execute(sql: str):
    DB.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(
        ["duckdb", str(DB), "-c", sql],
        text=True, capture_output=True
    )
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p.stdout
