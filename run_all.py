import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    ("stage_01_pipeline.py",           "Load raw files"),
    ("stage_02_clean_parcels.py",      "Clean parcels"),
    ("stage_03_dedupe_parcels.py",     "Deduplicate parcels"),
    ("stage_04_clean_scans.py",        "Clean scans"),
    ("stage_05_clean_remittances.py",  "Clean remittances"),
    ("stage_06_parcel_final.py",       "Build parcel_final"),
    ("stage_07_quality_checks.py",     "Data quality checks"),
    ("run_queries.py",                 "Run queries, save CSVs"),
]

def main():
    start_at = 1
    if "--from" in sys.argv:
        start_at = int(sys.argv[sys.argv.index("--from") + 1])

    if not (HERE / "data" / "parcels.csv").exists():
        sys.exit("No data found. Run first:  python3 make_data.py")

    began = time.time()
    for number, (script, title) in enumerate(STEPS, start=1):
        if number < start_at:
            print(f"..  skipping step {number}: {title}")
            continue
        print(f"\n=== STEP {number}: {title} ({script}) ===", flush=True)
        result = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE)
        if result.returncode != 0:
            sys.exit(f"\nSTOPPED: {script} failed. Fix it before continuing.")

    print(f"\nAll steps finished in {time.time() - began:.1f} seconds.")

if __name__ == "__main__":
    main()
    
# sqlite3 -header -column riderdrop.db < queries/q5.sql
