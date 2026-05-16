# Architecture

```text
public source registry + manual quotes
        ↓
seed tables / processed observations
        ↓
normalization + validation + confidence scoring
        ↓
feedstock passport + process/risk/cost models
        ↓
Streamlit dashboard + CLI tools + future ML dataset
```

The repository deliberately keeps public, quote-only, marketplace, and manual observations separate. The dashboard displays all records, but price charts only use normalized numeric prices.
