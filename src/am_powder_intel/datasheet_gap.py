from __future__ import annotations

DEFAULT_REQUIREMENTS = {
    ('powder', 'metal'): ['chemistry', 'PSD', 'morphology', 'apparent_density', 'tap_density', 'flowability', 'oxygen_nitrogen_hydrogen', 'production_route', 'SDS_url'],
    ('powder', 'polymer'): ['PSD', 'bulk_density', 'melting_point', 'crystallization_window', 'refresh_ratio', 'moisture', 'SDS_url'],
    ('filament', 'polymer'): ['diameter', 'tolerance', 'net_weight', 'density', 'drying_temperature', 'nozzle_temperature', 'bed_temperature', 'SDS_url'],
    ('resin', 'photopolymer'): ['bottle_volume', 'viscosity', 'wavelength', 'printer_compatibility', 'post_cure', 'shelf_life', 'SDS_url'],
    ('pellet', 'polymer'): ['pellet_size', 'MFI_or_MVR', 'drying_condition', 'density', 'recycled_content', 'SDS_url'],
}

FIELD_ALIASES = {
    'PSD': ['psd_um', 'particle_size', 'particle_size_distribution'],
    'diameter': ['diameter_mm', 'filament_diameter'],
    'net_weight': ['package_quantity'],
    'bottle_volume': ['package_quantity'],
    'density': ['density_g_cm3'],
    'production_route': ['production_route'],
}


def _present(value) -> bool:
    return value is not None and str(value).strip().lower() not in {'', 'nan', 'none', 'unknown'}


def missing_datasheet_fields(record: dict, requirements: list[str] | None = None) -> list[str]:
    key = (str(record.get('feedstock_class', '')).lower(), str(record.get('material_family', '')).lower())
    reqs = requirements or DEFAULT_REQUIREMENTS.get(key, [])
    missing = []
    for req in reqs:
        candidate_fields = FIELD_ALIASES.get(req, [req])
        if not any(_present(record.get(f)) for f in candidate_fields):
            missing.append(req)
    return missing


def gap_score(record: dict, requirements: list[str] | None = None) -> int:
    key = (str(record.get('feedstock_class', '')).lower(), str(record.get('material_family', '')).lower())
    reqs = requirements or DEFAULT_REQUIREMENTS.get(key, [])
    if not reqs:
        return 0
    missing = missing_datasheet_fields(record, reqs)
    return round(100 * (1 - len(missing) / len(reqs)))
