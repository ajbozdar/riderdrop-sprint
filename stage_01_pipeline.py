import sqlite3
import pandas as pd

FILES = {
    "parcels.csv":         "raw_parcels",
    "scans.csv":           "raw_scans",
    "cod_remittances.csv": "raw_remittances",
}

conn = sqlite3.connect("riderdrop.db")

for csv_name, table in FILES.items():
    df = pd.read_csv(f"data/{csv_name}", dtype=str, keep_default_na=False)
    rows_in_file = len(df)

    df.to_sql(table, conn, if_exists="replace", index=False)

    rows_in_table = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{csv_name:<22} file={rows_in_file:>5}  table={rows_in_table:>5}")

    # TODO: stop the program if the two counts differ

    if rows_in_file != rows_in_table:
        raise SystemExit(f"Rows count differ for {table}")

conn.close()
print("Stage 1 complete: all counts match.")
