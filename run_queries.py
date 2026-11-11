import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect("riderdrop.db")

for sql_file in sorted(Path("queries").glob("q*.sql")):
    df = pd.read_sql(sql_file.read_text(), conn)
    out = Path("results") / f"{sql_file.stem}.csv"
    df.to_csv(out, index=False)
    print(f"{sql_file.name}: {len(df)} rows -> {out}")

conn.close()
