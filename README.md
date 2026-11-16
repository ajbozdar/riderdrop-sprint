# RiderDrop sprint: where did the cash go?

A pipeline that loads three messy courier exports, cleans them, and tells Finance
how much cash is missing and who is holding it. Findings are in `findings.md`.

**Stack:** Python 3 (pandas, sqlite3) and SQLite. This differs from the brief
(SQL Server): SQLite has no schemas, so `raw.parcels` became `raw_parcels`, and
`clean.parcels` became `clean_parcels`. Primary keys are declared in `CREATE TABLE`,
because SQLite cannot add them afterwards.

## How to run

```bash
pip install pandas          # or: sudo apt install python3-pandas
python3 make_data.py        # generates data/*.csv (seeded, so identical every time)
python3 run_all.py          # runs every stage in order; stops at the first failure
python3 run_all.py --from 4 # resume at a later step
```

The database file is `riderdrop.db`, created automatically. No connection string
is needed. Every stage is idempotent: running it twice gives the same result.

## Files

| File | Job |
|---|---|
| `stage_01_pipeline.py` | Load the 3 CSVs into `raw_*` as text, check row counts |
| `stage_02_clean_parcels.py` | Parse dates, normalise zones and rider IDs |
| `stage_03_dedupe_parcels.py` | Build `clean_parcels` (primary key) and `merge_log` |
| `stage_04_clean_scans.py` | Build `rejected_scans` and `clean_scans` |
| `stage_05_clean_remittances.py` | Convert `amount` to a number |
| `stage_06_parcel_final.py` | One row per parcel: final status, `cod_due`, `on_time` |
| `stage_07_quality_checks.py` | Three checks, recorded in `dq_results` |
| `run_queries.py` | Run every `queries/*.sql`, save CSVs in `results/` |
| `queries/` | `q1` to `q5`, plus `q3b`, `q5_hidden`, `net_shortfall` |
| `results/` | One CSV per query |

## Cleaning decisions (one line each)

1. **Raw load:** every column is stored as text (`dtype=str`), so nothing is guessed; tables are replaced on each run.
2. **Duplicate parcels (rule 1):** 40 repeated `parcel_id` rows; `ROW_NUMBER()` keeps the latest `updated_at`, and the dropped rows are logged in `merge_log`.
3. **Dates:** three explicit formats are tried in turn (`%Y-%m-%d`, `%d/%m/%Y`, `%d-%b-%Y`); `pd.to_datetime(..., format="mixed")` is never used, because it misreads `11/09/2026`. An unparseable date becomes `NULL` and is counted.
4. **Zones and rider IDs:** trimmed and title-cased (zones) or upper-cased (riders), giving exactly 4 zones.
5. **Scans:** 30 scans for unknown parcels go to `rejected_scans` with a reason; 366 echo scans (same parcel and status within 120 seconds, rule 2) are removed with `LAG()`.
6. **Money:** non-digit characters are removed with a regex (`Rs`, commas, spaces) and the result becomes a number; all 734 rows are kept.

## Business rules as implemented

- Final status = status of the **latest** scan (rule 3).
- `cod_due` = `cod_amount` only if the final status is `delivered` (rule 4).
- On time = delivered on or before `promised_date` (rule 5).
- Shortfall = `cod_due` minus total remitted per parcel (rule 6); negative values are kept.

## Data quality

`stage_07_quality_checks.py` writes three checks to `dq_results`:
unique non-null `parcel_id`; `3870 raw scans = 3474 clean + 30 rejected + 366 echoes`
(echoes counted independently, so the check can fail); no delivery before booking.
These prove that no row vanished. They do not prove that the 2-minute rule removed the
right rows; that was tested separately (no surviving echoes, no parcel lost).

## Results at a glance

| Figure | Rupees | Query |
|---|---|---|
| Net shortfall, delivered parcels | 834,140 | `net_shortfall.sql` |
| Never remitted (97 parcels) | 727,690 | `q5.sql` |
| Underpaid by four riders | 106,450 | `q3b.sql` |
| Never remitted, contradictory scans (3 parcels) | 21,260 | `q5_hidden.sql` |
| Remitted for not-delivered parcels (41 parcels) | 265,630 | `q4.sql` |

## Known limitations and open points

- **Rule 3 can mislabel parcels.** 23 parcels have a `delivered` scan followed by a later `in_transit` scan. The pipeline obeys rule 3, so they count as not delivered. The business owner should decide whether "latest scan wins" is the right definition; both figures are reported.
- **Unexplained gap with the instructor reference figures.** The reference net shortfall is Rs 657,130; this pipeline gives Rs 834,140. For q5, the parcel count matches (97 + 3 = 100) but the rupees differ (748,950 against 759,440). No cause has been tested, and nothing was adjusted to match.
- **Q3 mixes two causes** (never remitted and underpaid), so `q3b` splits them.
- **On-time rate is about 50% in every zone.** The differences between zones (46% to 54%) are probably noise in synthetic data.
- Extra queries (`q3b`, `q5_hidden`, `net_shortfall`) are diagnostics beyond the five required questions.

## How to reproduce?
- Delete `riderdrop.db` and `results/`, then run `python3 run_all.py`
