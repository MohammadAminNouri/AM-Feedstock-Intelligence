from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

parser = argparse.ArgumentParser(description='Append a private/manual quote observation without leaking sensitive supplier docs.')
parser.add_argument('--record-id', required=True)
parser.add_argument('--supplier', required=True)
parser.add_argument('--currency', required=True)
parser.add_argument('--package-price', type=float, required=True)
parser.add_argument('--quantity', type=float, required=True)
parser.add_argument('--unit', default='kg')
parser.add_argument('--notes', default='manual quote; do not publish confidential document')
args = parser.parse_args()

out = Path('data/processed/manual_quote_log.csv')
out.parent.mkdir(parents=True, exist_ok=True)
exists = out.exists()
unit_price = args.package_price / args.quantity if args.unit == 'kg' else ''
row = {
    'observation_id': f"MANUAL-{args.record_id}-{date.today().isoformat()}",
    'record_id': args.record_id,
    'observed_date': date.today().isoformat(),
    'supplier': args.supplier,
    'currency': args.currency,
    'package_price': args.package_price,
    'package_quantity': args.quantity,
    'package_unit': args.unit,
    'normalized_price_per_kg': round(unit_price, 4) if unit_price != '' else '',
    'price_type': 'manual_quote',
    'confidence': 'high',
    'notes': args.notes,
}
with out.open('a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=row.keys())
    if not exists:
        w.writeheader()
    w.writerow(row)
print(f'added quote observation to {out}')
