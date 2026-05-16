from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class TrendSignal:
    name: str
    value: float
    weight: float
    direction: str  # positive, negative, risk


def score_trend(signals: list[TrendSignal]) -> float:
    """Weighted score from -100 to +100.

    Examples of signals:
    - supplier_count_growth
    - price_decrease_12m
    - patent_or_paper_growth
    - strategic_end_use_adoption
    - critical_raw_material_risk
    - qualification_barrier
    """
    if not signals:
        return 0.0
    weighted = []
    for s in signals:
        sign = -1 if s.direction in {"negative", "risk"} else 1
        weighted.append(sign * s.value * s.weight)
    total_weight = sum(abs(s.weight) for s in signals) or 1
    return round(max(-100, min(100, sum(weighted) / total_weight)), 2)


def classify_trend(score: float) -> str:
    if score >= 45:
        return "hot"
    if score >= 15:
        return "growing"
    if score <= -35:
        return "declining/risky"
    return "stable/watch"
