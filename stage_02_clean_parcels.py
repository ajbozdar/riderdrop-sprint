import sqlite3
import pandas as pd
from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"]

def to_date(text):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

conn = sqlite3.connect("riderdrop.db")
df = pd.read_sql("SELECT * FROM raw_parcels", conn)

df["booked_date"]   = df["booked_date"].map(to_date)
df["promised_date"] = df["promised_date"].map(to_date)
df["zone"]          = df["zone"].str.strip().str.title()
df["rider_id"]      = df["rider_id"].str.strip().str.upper()
df["cod_amount"]    = pd.to_numeric(df["cod_amount"])
df["updated_at"]    = pd.to_datetime(df["updated_at"])

print("unparsed booked dates:", df["booked_date"].isna().sum())
print("zones:", sorted(df["zone"].unique()))

df.to_sql("clean_parcels_all", conn, if_exists="replace", index=False)
conn.close()
