WITH remitted AS (
    SELECT parcel_id, SUM(amount) AS paid
    FROM clean_remittances
    GROUP BY parcel_id
)
SELECT pf.rider_id,
       SUM(CASE WHEN r.paid IS NULL THEN pf.cod_due ELSE 0 END)        AS never_remitted,
       SUM(CASE WHEN r.paid IS NOT NULL
                THEN pf.cod_due - r.paid ELSE 0 END)                   AS underpaid
FROM parcel_final pf
LEFT JOIN remitted r ON r.parcel_id = pf.parcel_id
WHERE pf.final_status = 'delivered'
GROUP BY pf.rider_id
ORDER BY underpaid DESC
LIMIT 8;
