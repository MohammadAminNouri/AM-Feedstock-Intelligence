from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

CORE_FIELDS = [
    'record_id', 'feedstock_class', 'material_family', 'material_group', 'grade_or_alloy',
    'product_name', 'supplier', 'manufacturer', 'supplier_type', 'processes',
    'price_type', 'source_url', 'source_accessed_date', 'confidence'
]

POWDER_FIELDS = ['psd_um', 'particle_shape', 'production_route', 'density_g_cm3', 'refresh_or_reuse_note']
FILAMENT_FIELDS = ['diameter_mm', 'production_route', 'density_g_cm3', 'handling_risks']
RESIN_FIELDS = ['package_quantity', 'package_unit', 'normalized_price_per_l', 'handling_risks']
PRICE_FIELDS = ['currency', 'package_price', 'package_quantity', 'package_unit']


def _present(value: Any) -> bool:
    return value is not None and str(value).strip().lower() not in {'', 'nan', 'none', 'unknown'}


def required_fields_for(feedstock_class: str) -> list[str]:
    cls = feedstock_class.lower().strip()
    fields = list(CORE_FIELDS)
    if cls == 'powder':
        fields += POWDER_FIELDS
    elif cls == 'filament':
        fields += FILAMENT_FIELDS
    elif cls == 'resin':
        fields += RESIN_FIELDS
    elif cls in {'pellet', 'wire', 'ceramic_slurry'}:
        fields += ['form_factor', 'production_route', 'handling_risks']
    fields += PRICE_FIELDS
    return list(dict.fromkeys(fields))


def completeness_score(record: Mapping[str, Any]) -> int:
    fields = required_fields_for(str(record.get('feedstock_class', '')))
    if not fields:
        return 0
    present = sum(1 for f in fields if _present(record.get(f)))
    return round(100 * present / len(fields))


@dataclass(frozen=True)
class PassportSummary:
    record_id: str
    completeness: int
    missing_fields: list[str]
    warning_count: int


def make_passport_summary(record: Mapping[str, Any]) -> PassportSummary:
    fields = required_fields_for(str(record.get('feedstock_class', '')))
    missing = [f for f in fields if not _present(record.get(f))]
    warnings = []
    if record.get('price_type') == 'public_list' and not (_present(record.get('normalized_price_per_kg')) or _present(record.get('normalized_price_per_l')) or _present(record.get('package_price'))):
        warnings.append('public_list price without numeric package/normalized price')
    if record.get('feedstock_class') == 'powder' and not _present(record.get('psd_um')):
        warnings.append('powder without PSD')
    if record.get('feedstock_class') == 'filament' and not _present(record.get('diameter_mm')):
        warnings.append('filament without diameter')
    return PassportSummary(str(record.get('record_id', '')), completeness_score(record), missing, len(warnings))
