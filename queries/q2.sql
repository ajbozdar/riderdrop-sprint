SELECT zone,
       COUNT(*)                                   AS delivered_parcels,
       SUM(on_time)                               AS on_time_parcels,
       ROUND(100.0 * SUM(on_time) / COUNT(*), 1)  AS on_time_pct
FROM parcel_final
WHERE final_status = 'delivered'
GROUP BY zone
ORDER BY zone;
