from __future__ import annotations

from dataclasses import dataclass


PROCESS_RULES = {
    "LPBF": {
        "preferred_psd": (15, 53),
        "morphology": {"spherical", "near-spherical"},
        "notes": "Needs good flowability, low satellites, controlled oxygen/moisture."
    },
    "EBM": {
        "preferred_psd": (45, 106),
        "morphology": {"spherical", "near-spherical"},
        "notes": "Coarser conductive powders; titanium and CoCr common."
    },
    "DED": {
        "preferred_psd": (45, 150),
        "morphology": {"spherical", "near-spherical"},
        "notes": "Nozzle flow matters; broader PSD acceptable than LPBF."
    },
    "Binder Jetting": {
        "preferred_psd": (5, 45),
        "morphology": {"spherical", "irregular", "near-spherical"},
        "notes": "Packing density and sinterability dominate."
    },
    "SLS": {
        "preferred_psd": (40, 120),
        "morphology": {"near-spherical", "irregular"},
        "notes": "Polymer powder needs thermal window and recyclability."
    },
    "MJF": {
        "preferred_psd": (40, 100),
        "morphology": {"near-spherical", "irregular"},
        "notes": "Polymer powder needs flow, heat absorption, and aging control."
    },
}


@dataclass(frozen=True)
class PowderDescriptor:
    psd_min_um: float | None
    psd_max_um: float | None
    morphology: str | None
    material_family: str


def score_process_suitability(powder: PowderDescriptor, process: str) -> dict:
    rule = PROCESS_RULES.get(process)
    if rule is None:
        return {"score": 0, "label": "unknown", "reason": "No rule for this process."}

    score = 50
    reasons = []

    if powder.psd_min_um is not None and powder.psd_max_um is not None:
        low, high = rule["preferred_psd"]
        overlap = max(0, min(powder.psd_max_um, high) - max(powder.psd_min_um, low))
        width = max(1, powder.psd_max_um - powder.psd_min_um)
        ratio = overlap / width
        score += int(35 * ratio)
        reasons.append(f"PSD overlap with preferred {low}-{high} µm: {ratio:.0%}.")
    else:
        reasons.append("PSD missing; score capped by uncertainty.")
        score -= 10

    if powder.morphology:
        if powder.morphology.lower() in rule["morphology"]:
            score += 15
            reasons.append("Morphology is compatible.")
        else:
            score -= 15
            reasons.append("Morphology may reduce flow/packing.")
    else:
        reasons.append("Morphology missing.")
        score -= 5

    score = max(0, min(score, 100))
    label = "strong" if score >= 80 else "possible" if score >= 55 else "weak"
    return {"score": score, "label": label, "reason": " ".join(reasons), "process_note": rule["notes"]}
