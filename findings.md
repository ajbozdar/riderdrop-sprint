# RiderDrop findings: September cash book

**Headline: Rs 834,140 is short on delivered parcels (`queries/net_shortfall.sql`), made up of Rs 727,690 never remitted (q5) and Rs 106,450 underpaid by four riders (q3b).**

- **Rs 727,690 was never remitted on 97 delivered parcels with no remittance record (`queries/q5.sql`), and a further Rs 21,260 on 3 parcels whose scans say "delivered" and then "in_transit" (`queries/q5_hidden.sql`):** on Monday, Finance should ask Operations for the rider handover logs for these 100 parcel IDs and chase the cash, starting with the 97 clear cases.
- **Four riders (R09, R08, R12, R13) remitted Rs 106,450 less than they owed on parcels they did pay for (`queries/q3b.sql`):** on Monday, Finance should hold individual conversations with these four riders, because their problem (partial payment) differs from riders who simply have unrecorded parcels.
- **Rs 265,630 arrived for 41 parcels whose last scan is not "delivered" (`queries/q4.sql`):** on Monday, Finance should first check the 23 parcels (Rs 140,530) with no earlier delivered scan, because Rs 125,100 on 18 parcels likely reflects scans recorded in the wrong order, not rider errors.

*Caveat:* the delivered status follows Rule 3 (latest scan wins). A parcel scanned "delivered" and then "in_transit" counts as not delivered, so q5 may understate the missing cash. The business owner should confirm whether this rule is correct.
