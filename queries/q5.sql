SELECT COUNT(*)     AS parcels_unremitted,
       SUM(cod_due) AS rupees_at_risk
FROM parcel_final pf
WHERE pf.final_status = 'delivered'
  AND pf.cod_due > 0
  AND NOT EXISTS (SELECT 1 FROM clean_remittances r
                  WHERE r.parcel_id = pf.parcel_id);
