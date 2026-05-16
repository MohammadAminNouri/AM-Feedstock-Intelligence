from __future__ import annotations

import argparse
import csv
from pathlib import Path

from am_powder_intel.recommender import rank_feedstocks

parser = argparse.ArgumentParser()
parser.add_argument('--process', help='LPBF, SLS, FDM, MJF, etc.')
parser.add_argument('--material-group', help='316L, PA12, PLA, etc.')
parser.add_argument('--public-price-only', action='store_true')
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()

path = Path('data/seed/am_feedstocks_seed.csv')
records = list(csv.DictReader(path.open(newline='', encoding='utf-8')) )
ranked = rank_feedstocks(records, process=args.process, material_group=args.material_group, require_public_price=args.public_price_only)
for r in ranked[:args.limit]:
    price = r.get('normalized_price_per_kg') or r.get('normalized_price_per_l') or r.get('package_price') or 'quote'
    print(f"{r['ranking_score']:>3} | {r['record_id']} | {r['product_name']} | {r['supplier']} | {price} {r.get('currency','')}")
