from __future__ import annotations

import csv
from pathlib import Path
import sys

from am_powder_intel.passport import make_passport_summary


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('data/seed/am_feedstocks_seed.csv')
    rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')) )
    errors = []
    for row in rows:
        summary = make_passport_summary(row)
        if not row.get('record_id'):
            errors.append('missing record_id')
        if row.get('price_type') == 'public_list' and not row.get('source_url'):
            errors.append(f"{row.get('record_id')}: public price without source_url")
        if row.get('feedstock_class') == 'powder' and not row.get('psd_um'):
            print(f"WARN {row.get('record_id')}: powder without PSD")
        if summary.completeness < 55:
            print(f"WARN {row.get('record_id')}: low passport completeness {summary.completeness}%")
    if errors:
        for e in errors:
            print('ERROR', e)
        return 1
    print(f'validated {len(rows)} feedstock rows')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
