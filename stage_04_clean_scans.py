import sqlite3
import pandas as pd

conn = sqlite3.connect("riderdrop.db")

scans = pd.read_sql("SELECT scan_id, parcel_id, status, scanned_at, rider_id FROM raw_scans", conn)
scans["status"]     = scans["status"].str.strip().str.lower()
scans["scanned_at"] = pd.to_datetime(scans["scanned_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
scans.to_sql("clean_scans_all", conn, if_exists="replace", index=False)

conn.executescript("""
DROP TABLE IF EXISTS rejected_scans;
DROP TABLE IF EXISTS clean_scans;

CREATE TABLE rejected_scans AS
SELECT s.*, 'parcel_id not found in clean_parcels' AS reason
FROM clean_scans_all s
WHERE s.parcel_id NOT IN (SELECT parcel_id FROM clean_parcels);

CREATE TABLE clean_scans AS
SELECT scan_id, parcel_id, status, scanned_at, rider_id
FROM (
    SELECT s.*,
           LAG(scanned_at) OVER (PARTITION BY parcel_id, parcel_id
                                 ORDER BY scanned_at) AS prev_scan
    FROM clean_scans_all s
    WHERE s.parcel_id IN (SELECT parcel_id FROM clean_parcels)
)
WHERE prev_scan IS NULL
   OR strftime('%s', scanned_at) - strftime('%s', prev_scan) > 120;
""")
conn.commit()

for table in ("raw_scans", "clean_scans", "rejected_scans"):
    print(table, conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
conn.close()
