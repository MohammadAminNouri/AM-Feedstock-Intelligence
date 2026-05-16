from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FeedstockRecord:
    record_id: str
    feedstock_class: str
    material_family: str
    material_group: str
    grade_or_alloy: str
    product_name: str
    supplier: str
    processes: str
    price_type: str
    confidence: str
    package_quantity: Optional[float] = None
    package_unit: Optional[str] = None
    package_price: Optional[float] = None
    currency: Optional[str] = None
    normalized_price_per_kg: Optional[float] = None
    normalized_price_per_l: Optional[float] = None

    @property
    def process_set(self) -> set[str]:
        return {p.strip().upper() for p in self.processes.split(';') if p.strip()}

    @property
    def has_public_price(self) -> bool:
        return self.price_type == 'public_list' and (self.normalized_price_per_kg is not None or self.normalized_price_per_l is not None or self.package_price is not None)
