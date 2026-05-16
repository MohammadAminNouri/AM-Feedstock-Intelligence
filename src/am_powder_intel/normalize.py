from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


ALLOY_ALIASES = {
    "ti64": "Ti-6Al-4V",
    "ti-6al-4v": "Ti-6Al-4V",
    "ti6al4v": "Ti-6Al-4V",
    "in718": "Inconel 718",
    "alloy 718": "Inconel 718",
    "in625": "Inconel 625",
    "alloy 625": "Inconel 625",
    "ss316l": "316L",
    "316 l": "316L",
    "alsi10mg": "AlSi10Mg",
    "al-si10-mg": "AlSi10Mg",
    "pla": "PLA",
    "petg": "PETG",
    "pa12": "PA12",
    "pa 12": "PA12",
    "pa11": "PA11",
    "peek": "PEEK",
    "pekk": "PEKK",
    "pps": "PPS",
    "asa": "ASA",
    "abs": "ABS",
}


@dataclass(frozen=True)
class PriceObservation:
    total_price: Optional[float]
    quantity_kg: Optional[float]
    currency: Optional[str]

    @property
    def unit_price_per_kg(self) -> Optional[float]:
        if self.total_price is None or not self.quantity_kg:
            return None
        return round(self.total_price / self.quantity_kg, 4)


def canonical_alloy(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip().lower())
    return ALLOY_ALIASES.get(key, name.strip())


def parse_psd_um(text: str) -> Optional[str]:
    """Extract a particle-size range like 15-53 from text."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*(?:µm|um|micron)", text, re.I)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2)}"


def normalize_currency(value: str | None) -> Optional[str]:
    if not value:
        return None
    value = value.strip().upper()
    symbols = {"$": "USD", "€": "EUR", "£": "GBP"}
    return symbols.get(value, value)
