from am_powder_intel.passport import completeness_score, make_passport_summary


def test_completeness_score_basic():
    row = {
        'record_id': 'X', 'feedstock_class': 'filament', 'material_family': 'polymer',
        'material_group': 'PLA', 'grade_or_alloy': 'PLA', 'product_name': 'PLA',
        'supplier': 'Supplier', 'manufacturer': 'Maker', 'supplier_type': 'material_manufacturer',
        'processes': 'FDM', 'price_type': 'public_list', 'source_url': 'https://example.com',
        'source_accessed_date': '2026-05-17', 'confidence': 'medium', 'diameter_mm': 1.75,
        'production_route': 'extruded filament', 'density_g_cm3': 1.24, 'handling_risks': 'dry',
        'currency': 'USD', 'package_price': 30, 'package_quantity': 1, 'package_unit': 'kg'
    }
    assert completeness_score(row) > 80
    assert make_passport_summary(row).warning_count == 0
