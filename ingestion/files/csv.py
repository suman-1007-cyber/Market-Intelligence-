from pathlib import Path
import pandas as pd
from storage.parquet import write

def ingest_csv(path, output="storage/bronze/data.parquet"):
    path = Path(path)
    df = pd.read_csv(path)
    write(df, output)
    return df, output
