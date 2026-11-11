import sqlite3
from datetime import datetime

conn = sqlite3.connect("riderdrop.db")
conn.execute("DROP TABLE IF EXISTS dq_results")
conn.execute("""CREATE TABLE dq_results (
    check_name TEXT, passed INTEGER, detail TEXT, run_at TEXT)""")

def one(sql):
    return conn.execute(sql).fetchone()[0]

def record(name, passed, detail):
    conn.execute("INSERT INTO dq_results VALUES (?, ?, ?, ?)",
                 (name, int(passed), detail, datetime.now().isoformat(timespec="seconds")))
    print("OK  " if passed else "FAIL", name, "-", detail)

# 1. parcel_id unique and not null
rows     = one("SELECT COUNT(*) FROM clean_parcels")
distinct = one("SELECT COUNT(DISTINCT parcel_id) FROM clean_parcels")
nulls    = one("SELECT COUNT(*) FROM clean_parcels WHERE parcel_id IS NULL")
record("parcel_id unique and not null",
       rows == distinct and nulls == 0, f"{rows} rows, {distinct} distinct, {nulls} null")

# 2. reconciliation, with echoes counted INDEPENDENTLY
raw      = one("SELECT COUNT(*) FROM raw_scans")
clean    = one("SELECT COUNT(*) FROM clean_scans")
rejected = one("SELECT COUNT(*) FROM rejected_scans")
echoes   = one("""SELECT COUNT(*) FROM clean_scans_all
                  WHERE parcel_id IN (SELECT parcel_id FROM clean_parcels)
                    AND scan_id NOT IN (SELECT scan_id FROM clean_scans)""")
record("raw scans = clean + rejected + echoes",
       raw == clean + rejected + echoes,
       f"{raw} = {clean} + {rejected} + {echoes}")

# 3. nothing delivered before it was booked
backwards = one("SELECT COUNT(*) FROM parcel_final WHERE delivered_date < booked_date")
record("no delivery before booking", backwards == 0, f"{backwards} parcels")

conn.commit()
failed = one("SELECT COUNT(*) FROM dq_results WHERE passed = 0")
conn.close()
if failed:
    raise SystemExit(f"{failed} check(s) failed. Do not present the numbers yet.")
print("All checks passed.")
