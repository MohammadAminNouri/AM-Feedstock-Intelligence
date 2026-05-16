# ML roadmap

Do not start with fake ML. Build clean data first, then model useful targets.

## Phase 1: Rule-based intelligence

- process suitability score
- passport completeness score
- price confidence score
- powder reuse risk
- filament drying/abrasion risk

## Phase 2: ML-ready dataset

Potential features:

- material family
- feedstock class
- PSD or filament diameter
- production route
- supplier type
- region
- price type
- process compatibility
- confidence
- source age

Potential targets:

- price band: low / medium / high
- likely process compatibility
- quote-only probability
- missing datasheet field prediction
- supplier category prediction

## Phase 3: Models

- baseline: logistic regression / random forest
- interpretable model: explain why a powder fits LPBF or why a filament is high-risk
- active learning: ask user which missing field should be collected next

## Phase 4: Niche research angle

Build a **feedstock intelligence graph**: supplier -> product -> material -> process -> price observation -> risk -> standard/datasheet. This is more original than a normal CSV dataset.
