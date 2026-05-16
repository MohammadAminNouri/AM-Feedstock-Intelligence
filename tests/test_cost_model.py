from am_powder_intel.cost_model import PowderCostInputs, material_cost_per_part


def test_material_cost_per_part_positive():
    cost = material_cost_per_part(PowderCostInputs(powder_price_per_kg=100, part_mass_g=50))
    assert cost > 0
