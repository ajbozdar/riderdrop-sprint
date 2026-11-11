import sqlite3
import pandas as pd

conn = sqlite3.connect("riderdrop.db")
remits = pd.read_sql(
    "SELECT remittance_id, parcel_id, rider_id, amount, remitted_at FROM raw_remittances",
    conn)

print("before:", list(remits["amount"].head(3)))

remits["amount"] = remits["amount"].str.replace(r"[^\d.]", "", regex=True)
remits["amount"] = pd.to_numeric(remits["amount"], errors="coerce")

print("after: ", list(remits["amount"].head(3)))

remits["rider_id"]    = remits["rider_id"].str.strip().str.upper()
remits["remitted_at"] = pd.to_datetime(remits["remitted_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")

print("unparsed amounts:", remits["amount"].isna().sum())
print("rows:", len(remits), " total Rs", round(remits["amount"].sum()))

remits.to_sql("clean_remittances", conn, if_exists="replace", index=False)
conn.close()
