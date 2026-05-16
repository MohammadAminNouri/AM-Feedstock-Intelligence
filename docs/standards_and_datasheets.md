# Standards and datasheet map

The repository does not copy paid standards. It stores pointers and uses them to structure data collection.

## Important standards / documents

- ASTM F3509: metal powder feedstock test-method guide for PBF, Binder Jetting, and DED.
- ASTM F3049: guide to characterization techniques for metal powders used in powder-based AM.
- ISO/ASTM 52928:2024: metal powder lifecycle management for powder-based AM.
- Supplier SDS/TDS/CoA: always required for procurement-quality records.

## Datasheet gap detector

Use:

```bash
python scripts/scan_datasheet_gaps.py
```

The output tells you which products are missing important fields such as PSD, density, flowability, drying conditions, resin wavelength, or SDS URL. This creates useful GitHub issues and makes the repo more than a static table.
