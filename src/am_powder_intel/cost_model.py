from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PowderCostInputs:
    powder_price_per_kg: float
    part_mass_g: float
    support_mass_g: float = 0.0
    powder_bed_loaded_kg: float = 0.0
    refresh_ratio: float = 0.2
    sieving_loss_fraction: float = 0.02
    failed_build_fraction: float = 0.03
    buy_to_fly_multiplier: float = 1.0


def material_cost_per_part(x: PowderCostInputs) -> float:
    """Estimate direct powder cost consumed per printed part.

    This is intentionally simple and transparent. It does not include machine time,
    labor, gas, QA, heat treatment, HIP, machining, or certification.
    """
    printed_mass_kg = (x.part_mass_g + x.support_mass_g) / 1000.0
    consumed_kg = printed_mass_kg * x.buy_to_fly_multiplier
    refresh_penalty_kg = consumed_kg * x.refresh_ratio
    sieving_loss_kg = max(x.powder_bed_loaded_kg, consumed_kg) * x.sieving_loss_fraction
    failure_penalty_kg = consumed_kg * x.failed_build_fraction
    total_effective_kg = consumed_kg + refresh_penalty_kg + sieving_loss_kg + failure_penalty_kg
    return round(total_effective_kg * x.powder_price_per_kg, 2)


def powder_inventory_cost(price_per_kg: float, machine_charge_kg: float, safety_stock_kg: float = 0.0) -> float:
    return round(price_per_kg * (machine_charge_kg + safety_stock_kg), 2)


@dataclass(frozen=True)
class FilamentCostInputs:
    filament_price_per_kg: float
    part_mass_g: float
    purge_mass_g: float = 0.0
    failed_print_fraction: float = 0.05


def filament_material_cost_per_part(x: FilamentCostInputs) -> float:
    consumed_kg = (x.part_mass_g + x.purge_mass_g) / 1000.0
    total_kg = consumed_kg * (1 + x.failed_print_fraction)
    return round(total_kg * x.filament_price_per_kg, 2)


@dataclass(frozen=True)
class ResinCostInputs:
    resin_price_per_l: float
    part_volume_ml: float
    support_volume_ml: float = 0.0
    vat_loss_fraction: float = 0.03
    failed_print_fraction: float = 0.04


def resin_material_cost_per_part(x: ResinCostInputs) -> float:
    consumed_l = (x.part_volume_ml + x.support_volume_ml) / 1000.0
    total_l = consumed_l * (1 + x.vat_loss_fraction + x.failed_print_fraction)
    return round(total_l * x.resin_price_per_l, 2)


@dataclass(frozen=True)
class PelletCostInputs:
    pellet_price_per_kg: float
    part_mass_g: float
    purge_mass_g: float = 0.0
    grinder_reuse_credit_fraction: float = 0.0
    failed_print_fraction: float = 0.04


def pellet_material_cost_per_part(x: PelletCostInputs) -> float:
    consumed_kg = (x.part_mass_g + x.purge_mass_g) / 1000.0
    total_kg = consumed_kg * (1 + x.failed_print_fraction) * (1 - x.grinder_reuse_credit_fraction)
    return round(total_kg * x.pellet_price_per_kg, 2)
