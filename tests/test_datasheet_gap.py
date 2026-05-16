from am_powder_intel.datasheet_gap import gap_score, missing_datasheet_fields


def test_gap_detector_powder_missing_sds():
    row = {'feedstock_class': 'powder', 'material_family': 'metal', 'psd_um': '15-53', 'particle_shape': 'spherical', 'production_route': 'VIGA'}
    missing = missing_datasheet_fields(row)
    assert 'SDS_url' in missing
    assert gap_score(row) < 100
