from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"]

def to_date(text):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None

# Tests: all three lines must print 2026-09-11
print(to_date("2026-09-11"))
print(to_date("11/09/2026"))
print(to_date("11-Sep-2026"))
print(to_date("garbage"))   # must print None
