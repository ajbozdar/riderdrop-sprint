WITH remitted AS (
    SELECT parcel_id, SUM(amount) AS paid
    FROM clean_remittances
    GROUP BY parcel_id
)
SELECT pf.rider_id,
       SUM(pf.cod_due - COALESCE(r.paid, 0)) AS total_shortfall
FROM parcel_final pf
LEFT JOIN remitted r ON r.parcel_id = pf.parcel_id
WHERE pf.final_status = 'delivered'
GROUP BY pf.rider_id
ORDER BY total_shortfall DESC
LIMIT 5;
