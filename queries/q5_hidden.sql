SELECT COUNT(*)         AS parcels,
       SUM(cod_amount)  AS rupees_hidden_from_q5
FROM parcel_final pf
WHERE pf.final_status <> 'delivered'
  AND pf.cod_amount > 0
  AND EXISTS (SELECT 1 FROM clean_scans s
              WHERE s.parcel_id = pf.parcel_id AND s.status = 'delivered')
  AND NOT EXISTS (SELECT 1 FROM clean_remittances r
                  WHERE r.parcel_id = pf.parcel_id);
