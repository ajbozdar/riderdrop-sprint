SELECT pf.final_status,
       COUNT(DISTINCT pf.parcel_id) AS parcels,
       SUM(r.amount)                AS rupees_remitted
FROM parcel_final pf
INNER JOIN clean_remittances r ON r.parcel_id = pf.parcel_id
WHERE pf.final_status <> 'delivered'
GROUP BY pf.final_status;
