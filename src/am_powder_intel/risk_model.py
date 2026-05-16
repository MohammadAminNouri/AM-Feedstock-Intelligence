from __future__ import annotations

HYGROSCOPIC_POLYMERS = {'PA', 'PA12', 'PA11', 'PA6', 'PA612', 'NYLON', 'PC', 'PVA', 'TPU', 'PEEK', 'PEKK'}
OXYGEN_SENSITIVE_METALS = {'TI', 'TITANIUM', 'TI-6AL-4V', 'AL', 'ALSI10MG', 'MG'}
ABRASIVE_KEYWORDS = {'CF', 'CARBON', 'GF', 'GLASS', 'KEVLAR', 'CERAMIC', 'METAL-FILLED'}


def powder_reuse_risk(material_group: str, process: str, reuse_cycles: int = 0, oxygen_ppm_delta: float | None = None, moisture_flag: bool = False) -> dict:
    group = material_group.upper()
    score = 20
    reasons = []
    if any(k in group for k in OXYGEN_SENSITIVE_METALS):
        score += 25
        reasons.append('oxygen-sensitive material family')
    if process.upper() in {'LPBF', 'EBM'}:
        score += 15
        reasons.append('powder-bed reuse changes PSD/fines/spatter exposure')
    if reuse_cycles >= 5:
        score += 20
        reasons.append('many reuse cycles')
    if oxygen_ppm_delta is not None and oxygen_ppm_delta > 300:
        score += 20
        reasons.append('large oxygen pickup')
    if moisture_flag:
        score += 10
        reasons.append('moisture concern')
    score = min(100, score)
    return {'score': score, 'label': 'high' if score >= 70 else 'medium' if score >= 40 else 'low', 'reasons': reasons}


def filament_handling_risk(material_group: str, dried: bool = False, abrasive: bool | None = None) -> dict:
    text = material_group.upper()
    score = 15
    reasons = []
    if any(k in text for k in HYGROSCOPIC_POLYMERS):
        score += 35
        reasons.append('hygroscopic polymer: drying controls print quality')
        if not dried:
            score += 20
            reasons.append('not confirmed dried')
    abrasive_detected = abrasive if abrasive is not None else any(k in text for k in ABRASIVE_KEYWORDS)
    if abrasive_detected:
        score += 20
        reasons.append('abrasive filler: hardened nozzle recommended')
    score = min(100, score)
    return {'score': score, 'label': 'high' if score >= 70 else 'medium' if score >= 40 else 'low', 'reasons': reasons}


def resin_handling_risk(skin_contact_controls: bool = False, months_since_open: float | None = None) -> dict:
    score = 45
    reasons = ['uncured photopolymer resin can be a skin/eye irritant or sensitizer']
    if not skin_contact_controls:
        score += 25
        reasons.append('PPE/handling controls not confirmed')
    if months_since_open is not None and months_since_open > 6:
        score += 15
        reasons.append('open resin age may affect print consistency')
    score = min(100, score)
    return {'score': score, 'label': 'high' if score >= 70 else 'medium' if score >= 40 else 'low', 'reasons': reasons}
