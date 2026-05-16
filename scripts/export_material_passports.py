from __future__ import annotations

import csv
from pathlib import Path

from am_powder_intel.passport import make_passport_summary

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / 'data' / 'seed' / 'am_feedstocks_seed.csv'
OUT = ROOT / 'data' / 'processed' / 'passport_completeness.csv'

rows = []
for row in csv.DictReader(IN.open(newline='', encoding='utf-8')):
    s = make_passport_summary(row)
    rows.append({
        'record_id': s.record_id,
        'completeness': s.completeness,
        'warning_count': s.warning_count,
        'missing_fields': ';'.join(s.missing_fields),
    })
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f'wrote {OUT}')
