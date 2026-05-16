# AM Feedstock Intelligence

**AM Feedstock Intelligence** is an open-source database and analytics toolkit for additive-manufacturing feedstocks: **metal powders, polymer powders, FDM/FFF filaments, SLA/DLP resins, pellets/granules, wires, ceramic slurries, composites, suppliers, real public prices, quote status, process suitability, reuse risk, and trend signals.**

The repository is designed for materials engineers, AM labs, procurement teams, students, researchers, and people who want a serious GitHub project that is useful beyond a generic material list.

## Why this repository is different

Most AM material lists stop at:

```text
Material -> process -> rough properties
```

This repository tracks the industrial reality:

```text
Main material family
  -> alloy / polymer / ceramic grade
    -> feedstock form: powder / filament / resin / pellet / wire / slurry
      -> supplier vs true manufacturer
        -> PSD or diameter / morphology / production route
          -> process suitability and qualification barrier
            -> price observation / MOQ / quote-only status / confidence
              -> reuse risk / safety / sustainability / trend signal
```

## What is covered

| Area | Examples | Processes |
|---|---|---|
| Metal powders | 316L, AlSi10Mg, Ti-6Al-4V, IN718, IN625, maraging steel | LPBF, EBM, DED, Binder Jetting |
| Polymer powders | PA12, PA11, PA12-CF, PA11-CF | SLS, MJF |
| Filaments | PLA, ASA, PA-CF, PPS-CF, PA12-CF | FFF/FDM |
| Resins | Formlabs-type photopolymer resins | SLA, DLP, MSLA |
| Pellets/granules | PLA pellets, recycled pellets, large-format feedstock | FGF / pellet extrusion |
| Wires | welding wire candidates | WAAM / wire DED |
| Ceramic slurries | alumina/zirconia slurry candidates | LCM / ceramic DLP |

## Core features

- Broad **AM feedstock catalog**, not only metal powders.
- Traceable price observations with `price_type`, source URL, date, package size, and confidence.
- **Powder / filament / resin passport completeness scoring**.
- Process requirement matrix for LPBF, EBM, DED, Binder Jetting, SLS, MJF, FDM, FGF, SLA/DLP, WAAM, and ceramic DLP.
- Cost models for powder, filament, resin, and pellet printing.
- Reuse and handling risk models for metal powder, polymer powder, filament, and resin.
- Supplier taxonomy separating atomizers, machine OEMs, material manufacturers, resellers, marketplaces, and commodity suppliers.
- Streamlit dashboard for filtering by material family, process, supplier, public price, confidence, and passport completeness.
- Scripts for validation, manual quote logging, ranking feedstocks, and exporting passport completeness.
- GitHub Actions pipeline for conservative public source checks.
- Datasheet gap detector and standards map for AM feedstock qualification.

## Repository map

```text
data/seed/
  am_feedstocks_seed.csv          Main broad feedstock catalog
  am_powders_seed.csv             Legacy powder-focused seed file
  price_observations_seed.csv     Long-form price observations
  process_requirements.csv        Process/feedstock compatibility rules
  supplier_taxonomy.csv           Supplier classification
  trend_segments.csv              Market/technical trend watchlist
  standards_map.csv                Standards and datasheet references
  datasheet_requirements.csv       Required fields by feedstock class
schemas/
  feedstock_record.schema.json    General AM feedstock schema
  powder_record.schema.json       Legacy powder schema
src/am_powder_intel/
  cost_model.py                   Powder/filament/resin/pellet cost models
  suitability.py                  Process suitability rules
  passport.py                     Completeness scoring
  risk_model.py                   Reuse/handling risk models
  price_confidence.py             Price-source confidence scoring
  recommender.py                  Simple process/material ranking
  supplier_taxonomy.py            Supplier/material families
dashboards/
  streamlit_app.py                Interactive catalog dashboard
scripts/
  validate_feedstocks.py          Data QA
  export_material_passports.py    Completeness report
  rank_feedstocks.py              CLI ranking
  add_manual_quote.py             Private/manual quote logger
  scan_datasheet_gaps.py           Missing datasheet-field scanner
docs/
  *.md                            Architecture, source policy, polymer coverage, ML roadmap
```

## Install

```bash
git clone https://github.com/YOUR_USERNAME/am-feedstock-intelligence.git
cd am-feedstock-intelligence
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev,dashboard]
```

## Run dashboard

```bash
streamlit run dashboards/streamlit_app.py
```

## Validate data

```bash
python scripts/validate_feedstocks.py
python scripts/export_material_passports.py
python scripts/scan_datasheet_gaps.py
```

## Rank feedstocks

```bash
python scripts/rank_feedstocks.py --process LPBF --material-group 316L --public-price-only
python scripts/rank_feedstocks.py --process FDM --material-group PA --public-price-only
python scripts/rank_feedstocks.py --process SLS --material-group PA12
```

## Add a private quote observation

Do not publish confidential quote PDFs. Log only the minimum derived observation needed for internal comparison:

```bash
python scripts/add_manual_quote.py \
  --record-id MET-TI-TI64-G23-AP-001 \
  --supplier "Supplier name" \
  --currency EUR \
  --package-price 1300 \
  --quantity 10 \
  --unit kg
```

## Data rule

Every price observation must include:

- source URL or manual quote note
- access/observation date
- package quantity and package unit when known
- `price_type`: `public_list`, `request_quote`, `distributor_estimate`, `marketplace`, or `manual_quote`
- confidence label: `high`, `medium`, or `low`

Never fake a market average. Public ecommerce prices, quote-only OEM pages, marketplace signals, and private supplier quotes are different evidence types. The project keeps them separate.

## First serious GitHub issues to open

1. Add 50 more verified metal powder products with PSD and atomization route.
2. Add 50 polymer feedstocks split into PA12 powder, PA11 powder, PLA/PETG/ASA filament, PA-CF, PC, PPS, PEEK, PEKK, TPU, and resins.
3. Add datasheet completeness detector.
4. Add supplier/manufacturer origin verification.
5. Add region-aware price normalization and currency conversion.
6. Add ML model for process-suitability and price-band prediction after enough clean records exist.

## License

MIT.
