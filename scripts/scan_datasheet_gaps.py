from __future__ import annotations

import csv
from pathlib import Path

from am_powder_intel.datasheet_gap import missing_datasheet_fields, gap_score

IN = Path('data/seed/am_feedstocks_seed.csv')
OUT = Path('data/processed/datasheet_gaps.csv')
OUT.parent.mkdir(parents=True, exist_ok=True)
rows = []
for row in csv.DictReader(IN.open(newline='', encoding='utf-8')):
    missing = missing_datasheet_fields(row)
    rows.append({
        'record_id': row['record_id'],
        'product_name': row['product_name'],
        'feedstock_class': row['feedstock_class'],
        'material_family': row['material_family'],
        'gap_score': gap_score(row),
        'missing_datasheet_fields': ';'.join(missing),
    })
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f'wrote {OUT}')
