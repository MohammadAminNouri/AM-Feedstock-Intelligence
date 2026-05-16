from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from am_powder_intel.passport import completeness_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "seed" / "am_feedstocks_seed.csv"

st.set_page_config(page_title="AM Feedstock Intelligence", layout="wide")
st.title("AM Feedstock Intelligence")
st.caption("Metals + polymers + ceramics: powders, filaments, resins, pellets, wires, suppliers, prices, confidence, and process suitability.")

df = pd.read_csv(DATA).fillna("")
df["passport_completeness"] = df.apply(lambda r: completeness_score(r.to_dict()), axis=1)

with st.sidebar:
    st.header("Filters")
    feedstock = st.multiselect("Feedstock class", sorted(df["feedstock_class"].dropna().unique()))
    family = st.multiselect("Material family", sorted(df["material_family"].dropna().unique()))
    group = st.multiselect("Material group", sorted(df["material_group"].dropna().unique()))
    confidence = st.multiselect("Confidence", sorted(df["confidence"].dropna().unique()))
    process_query = st.text_input("Process contains", placeholder="LPBF, SLS, FDM, MJF...")
    public_only = st.checkbox("Public numeric price only", value=False)

view = df.copy()
if feedstock:
    view = view[view["feedstock_class"].isin(feedstock)]
if family:
    view = view[view["material_family"].isin(family)]
if group:
    view = view[view["material_group"].isin(group)]
if confidence:
    view = view[view["confidence"].isin(confidence)]
if process_query:
    view = view[view["processes"].str.contains(process_query, case=False, na=False)]
if public_only:
    view = view[(view["price_type"] == "public_list") & ((view["normalized_price_per_kg"] != "") | (view["normalized_price_per_l"] != "") | (view["package_price"] != ""))]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Records", len(view))
c2.metric("Classes", view["feedstock_class"].nunique())
c3.metric("Suppliers", view["supplier"].nunique())
c4.metric("Public prices", int((view["price_type"] == "public_list").sum()))
c5.metric("Avg passport", f"{view['passport_completeness'].mean():.0f}%" if len(view) else "0%")

tab_catalog, tab_price, tab_passport, tab_sources = st.tabs(["Catalog", "Prices", "Passports", "Sources"] )

with tab_catalog:
    st.subheader("Feedstock catalog")
    st.dataframe(view, use_container_width=True, height=520)

with tab_price:
    st.subheader("Normalized price observations")
    priced_kg = view[view["normalized_price_per_kg"].astype(str).str.len() > 0].copy()
    if not priced_kg.empty:
        priced_kg["normalized_price_per_kg"] = pd.to_numeric(priced_kg["normalized_price_per_kg"], errors="coerce")
        fig = px.bar(
            priced_kg.sort_values("normalized_price_per_kg"),
            x="product_name",
            y="normalized_price_per_kg",
            color="feedstock_class",
            hover_data=["supplier", "material_group", "currency", "package_quantity", "package_unit", "confidence"],
            labels={"normalized_price_per_kg": "Price / kg"},
        )
        st.plotly_chart(fig, use_container_width=True)
    priced_l = view[view["normalized_price_per_l"].astype(str).str.len() > 0].copy()
    if not priced_l.empty:
        priced_l["normalized_price_per_l"] = pd.to_numeric(priced_l["normalized_price_per_l"], errors="coerce")
        st.write("Liquid/resin price observations")
        st.dataframe(priced_l[["record_id", "product_name", "supplier", "currency", "normalized_price_per_l", "confidence", "source_url"]], use_container_width=True)

with tab_passport:
    st.subheader("Completeness and missing data")
    cols = ["record_id", "feedstock_class", "product_name", "supplier", "passport_completeness", "price_type", "confidence", "handling_risks", "refresh_or_reuse_note"]
    st.dataframe(view[cols].sort_values("passport_completeness"), use_container_width=True, height=500)

with tab_sources:
    st.subheader("Traceable source links")
    for _, row in view.iterrows():
        url = str(row.get("source_url", ""))
        if url:
            st.markdown(f"- **{row['product_name']}** — {row['supplier']} — {row['price_type']} — [source]({url})")
        else:
            st.markdown(f"- **{row['product_name']}** — {row['supplier']} — {row['price_type']} — no source yet")
