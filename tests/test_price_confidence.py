from datetime import date

from am_powder_intel.price_confidence import score_price_confidence, confidence_label


def test_price_confidence_public_source():
    score = score_price_confidence('public_list', '2026-05-17', True, True, True)
    assert score >= 85
    assert confidence_label(score) == 'high'
