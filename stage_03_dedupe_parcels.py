import sqlite3

conn = sqlite3.connect("riderdrop.db")

conn.executescript("""
DROP TABLE IF EXISTS clean_parcels;
DROP TABLE IF EXISTS merge_log;

CREATE TABLE clean_parcels (
    parcel_id     TEXT PRIMARY KEY,
    booked_date   TEXT,
    promised_date TEXT,
    zone          TEXT,
    rider_id      TEXT,
    cod_amount    REAL,
    updated_at    TEXT
);

INSERT INTO clean_parcels
SELECT parcel_id, booked_date, promised_date, zone, rider_id, cod_amount, updated_at
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY parcel_id
                                 ORDER BY updated_at DESC) AS rn
    FROM clean_parcels_all
)
WHERE rn = 1;

CREATE TABLE merge_log AS
SELECT parcel_id, updated_at AS dropped_updated_at,
       'superseded by a row with a later updated_at' AS reason
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY parcel_id
                                 ORDER BY updated_at DESC) AS rn
    FROM clean_parcels_all
)
WHERE rn > 1;
""")
conn.commit()

for table in ("clean_parcels", "merge_log"):
    n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(table, n)
conn.close()
