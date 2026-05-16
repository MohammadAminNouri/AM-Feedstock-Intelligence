from __future__ import annotations

from datetime import date

TEMPLATE = {
    "material_family": "metal",
    "material_group": "Ti",
    "grade_or_alloy": "Ti-6Al-4V",
    "powder_name": "",
    "supplier": "",
    "manufacturer": "",
    "processes": ["LPBF"],
    "psd_um": "15-53",
    "price_type": "request_quote",
    "source_url": "",
    "source_accessed_date": date.today().isoformat(),
    "confidence": "medium",
}

print(TEMPLATE)
