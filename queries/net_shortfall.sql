SELECT SUM(pf.cod_due - COALESCE(r.paid, 0)) AS net_shortfall
FROM parcel_final pf
LEFT JOIN (SELECT parcel_id, SUM(amount) AS paid
           FROM clean_remittances GROUP BY parcel_id) r
       ON r.parcel_id = pf.parcel_id
WHERE pf.final_status = 'delivered';
