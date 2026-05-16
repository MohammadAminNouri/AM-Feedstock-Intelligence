from __future__ import annotations

from datetime import date, datetime
from typing import Optional

BASE = {
    'public_list': 70,
    'manual_quote': 85,
    'request_quote': 45,
    'distributor_estimate': 35,
    'marketplace': 25,
    'unknown': 10,
}


def age_days(accessed_date: str | None, today: date | None = None) -> Optional[int]:
    if not accessed_date:
        return None
    today = today or date.today()
    try:
        d = datetime.fromisoformat(str(accessed_date)).date()
    except ValueError:
        return None
    return (today - d).days


def score_price_confidence(price_type: str, accessed_date: str | None = None, has_quantity: bool = False, has_source: bool = False, manufacturer_known: bool = False) -> int:
    score = BASE.get((price_type or 'unknown').strip(), 10)
    if has_quantity:
        score += 10
    if has_source:
        score += 10
    if manufacturer_known:
        score += 5
    days = age_days(accessed_date)
    if days is not None:
        if days <= 30:
            score += 5
        elif days > 365:
            score -= 20
        elif days > 180:
            score -= 10
    return max(0, min(100, score))


def confidence_label(score: int) -> str:
    if score >= 75:
        return 'high'
    if score >= 45:
        return 'medium'
    return 'low'
