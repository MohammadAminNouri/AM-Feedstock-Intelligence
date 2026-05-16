from am_powder_intel.risk_model import filament_handling_risk, powder_reuse_risk


def test_nylon_cf_filament_risk():
    risk = filament_handling_risk('PA12-CF', dried=False)
    assert risk['label'] in {'medium', 'high'}


def test_ti_reuse_risk():
    risk = powder_reuse_risk('Ti-6Al-4V', 'LPBF', reuse_cycles=6)
    assert risk['score'] >= 60
