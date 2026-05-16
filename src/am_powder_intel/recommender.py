from __future__ import annotations

from typing import Iterable, Mapping, Any


def _tokens(text: str) -> set[str]:
    return {t.strip().upper() for t in str(text).replace(',', ';').split(';') if t.strip()}


def rank_feedstocks(records: Iterable[Mapping[str, Any]], process: str | None = None, material_group: str | None = None, require_public_price: bool = False) -> list[dict[str, Any]]:
    ranked = []
    for r in records:
        score = 0
        if process and process.upper() in _tokens(str(r.get('processes', ''))):
            score += 40
        elif process:
            continue
        if material_group and material_group.lower() in str(r.get('material_group', '')).lower():
            score += 25
        elif material_group:
            continue
        if r.get('price_type') == 'public_list':
            score += 15
        elif require_public_price:
            continue
        if str(r.get('confidence', '')).lower() == 'high':
            score += 15
        elif str(r.get('confidence', '')).lower() == 'medium':
            score += 8
        if str(r.get('normalized_price_per_kg', '')).strip():
            score += 5
        out = dict(r)
        out['ranking_score'] = score
        ranked.append(out)
    return sorted(ranked, key=lambda x: x['ranking_score'], reverse=True)
