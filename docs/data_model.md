# Data model

The main table is `data/seed/am_feedstocks_seed.csv`. It is broad enough for powders, filaments, resins, pellets, wires, and ceramic slurries.

Key design principle: store a **product/observation**, not just a material. `PA12` is not enough. `HP 3D High Reusability PA12 13 kg MJF powder` and `EOS PA2200 SLS powder` are different industrial products.

## Tables

- `am_feedstocks_seed.csv`: main catalog
- `price_observations_seed.csv`: price observations in long format
- `process_requirements.csv`: typical process/feedstock requirements
- `supplier_taxonomy.csv`: supplier classification
- `trend_segments.csv`: market/technical trend watchlist

## Important columns

- `feedstock_class`: powder, filament, resin, pellet, wire, ceramic_slurry
- `material_family`: metal, polymer, polymer_composite, photopolymer, ceramic
- `material_group`: Fe, Ni, PA12, PLA, ASA, PA-CF, etc.
- `price_type`: public_list, request_quote, distributor_estimate, marketplace, manual_quote
- `confidence`: high, medium, low
- `normalized_price_per_kg` and `normalized_price_per_l`: only filled when package unit is clear
