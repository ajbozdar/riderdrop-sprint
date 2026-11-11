SELECT zone, final_status, COUNT(*) AS parcels
FROM parcel_final
GROUP BY zone, final_status 
ORDER BY zone, final_status;
