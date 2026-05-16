from __future__ import annotations

import argparse
import csv
import re
from datetime import date
from pathlib import Path
from typing import Any

import requests
import yaml
from bs4 import BeautifulSoup

PRICE_RE = re.compile(r"([$€£])\s?([0-9][0-9,]*(?:\.\d+)?)")


def load_sources(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)["sources"]


def extract_public_price_text(html: str) -> list[tuple[str, float]]:
    """Very conservative public price extractor.

    It does not try to bypass dynamic pages, hidden APIs, login walls, or quote forms.
    It simply scans visible text for currency-looking values.
    """
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = " ".join(soup.get_text(" ").split())
    out = []
    for symbol, raw in PRICE_RE.findall(text):
        try:
            out.append((symbol, float(raw.replace(",", ""))))
        except ValueError:
            continue
    return out


def fetch_source(source: dict[str, Any]) -> dict[str, Any]:
    headers = {"User-Agent": "AM-Powder-Intelligence/0.1 educational research"}
    response = requests.get(source["url"], headers=headers, timeout=20)
    response.raise_for_status()
    prices = extract_public_price_text(response.text)
    return {
        "source_id": source["id"],
        "name": source["name"],
        "url": source["url"],
        "type": source["type"],
        "expected_material": source.get("expected_material"),
        "accessed_date": date.today().isoformat(),
        "raw_price_candidates": ";".join([f"{s}{v}" for s, v in prices[:20]]),
        "candidate_count": len(prices),
        "status": "ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="data/seed/public_sources.yml")
    parser.add_argument("--out", default="data/processed/latest_price_candidates.csv")
    args = parser.parse_args()

    sources = load_sources(Path(args.sources))
    rows = []
    for source in sources:
        try:
            rows.append(fetch_source(source))
        except Exception as exc:  # noqa: BLE001 - logged for pipeline robustness
            rows.append({
                "source_id": source["id"],
                "name": source["name"],
                "url": source["url"],
                "type": source["type"],
                "expected_material": source.get("expected_material"),
                "accessed_date": date.today().isoformat(),
                "raw_price_candidates": "",
                "candidate_count": 0,
                "status": f"error: {exc}",
            })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
