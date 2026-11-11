import sqlite3

conn = sqlite3.connect("riderdrop.db")

conn.executescript("""
DROP TABLE IF EXISTS parcel_final;

CREATE TABLE parcel_final (
    parcel_id      TEXT PRIMARY KEY,
    zone           TEXT,
    rider_id       TEXT,
    booked_date    TEXT,
    promised_date  TEXT,
    cod_amount     REAL,
    final_status   TEXT,
    delivered_date TEXT,
    cod_due        REAL,
    on_time        INTEGER
);

INSERT INTO parcel_final
WITH last_scan AS (
    SELECT parcel_id, status, scanned_at,
           ROW_NUMBER() OVER (PARTITION BY parcel_id
                              ORDER BY scanned_at DESC) AS rn
    FROM clean_scans
)
SELECT p.parcel_id, p.zone, p.rider_id, p.booked_date, p.promised_date, p.cod_amount,
       COALESCE(ls.status, 'no_scan')                                AS final_status,
       CASE WHEN ls.status = 'delivered'
            THEN date(ls.scanned_at) END                             AS delivered_date,
       CASE WHEN ls.status = 'delivered'
            THEN p.cod_amount ELSE 0 END                             AS cod_due,
       CASE WHEN ls.status = 'delivered'
             AND date(ls.scanned_at) <= p.promised_date
            THEN 1 ELSE 0 END                                        AS on_time
FROM clean_parcels p
LEFT JOIN last_scan ls
       ON ls.parcel_id = p.parcel_id AND ls.rn = 1;
""")
conn.commit()

print("rows:", conn.execute("SELECT COUNT(*) FROM parcel_final").fetchone()[0])
print("delivered before booked:", conn.execute(
    "SELECT COUNT(*) FROM parcel_final WHERE delivered_date < booked_date").fetchone()[0])
for row in conn.execute("""SELECT final_status, COUNT(*), SUM(cod_due)
                           FROM parcel_final GROUP BY final_status"""):
    print(row)
conn.close()
