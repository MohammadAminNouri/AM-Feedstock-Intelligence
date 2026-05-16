from am_powder_intel.normalize import canonical_alloy, parse_psd_um


def test_canonical_alloy():
    assert canonical_alloy("ti64") == "Ti-6Al-4V"


def test_parse_psd():
    assert parse_psd_um("15–53 µm") == "15-53"
