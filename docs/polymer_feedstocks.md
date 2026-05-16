# Polymer, filament, resin, pellet, and composite coverage

This repository intentionally covers polymers because many AM databases overfocus on metal LPBF and miss the feedstock economics of real labs.

## Polymer powder categories

- **PA12**: dominant SLS/MJF production polymer; track refresh ratio, cake aging, and surface-quality drift.
- **PA11**: bio-based castor-oil narrative, usually tougher than PA12, often higher price.
- **TPU/TPE powders**: flexible SLS/MJF materials; track flow and aging.
- **PP/PE powders**: lower density and chemical resistance, but harder sintering windows.
- **PEEK/PEKK powders**: high temperature and high cost; strict machine capability requirements.
- **CF/GF-filled powders**: stiffness improvement but fiber segregation, dust, and recycling issues.

## Filament categories

- Commodity: PLA, PETG, ABS, ASA, TPU.
- Engineering: PA6, PA12, PC, PP, ASA, PCTG.
- High temperature: PPS, PEI/ULTEM, PEEK, PEKK.
- Filled/composite: CF, GF, Kevlar, ESD, metal-filled, ceramic-filled.
- Support: PVA, BVOH, HIPS, breakaway support.

## Resin categories

- Standard prototyping resins.
- Tough/durable/flexible resins.
- Dental/medical biocompatible resins.
- Castable resins.
- Ceramic-filled resins/slurries.

## Data fields that matter for polymers

| Feedstock | Key fields |
|---|---|
| Polymer powder | PSD, refresh ratio, melting point, crystallization window, cake aging, moisture, bulk density |
| Filament | diameter tolerance, ovality, spool weight, drying conditions, nozzle temp, bed temp, chamber need, abrasiveness |
| Resin | viscosity, wavelength, exposure profile, shelf life, bottle volume, post-cure, safety, biocompatibility class |
| Pellets | pellet size, MFI/MVR, drying, recycled content, screw/nozzle wear, contamination risk |
