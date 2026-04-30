#!/usr/bin/env python3
"""
generate_charts.py
Reads data/cohort.csv and outputs 4 Plotly charts to assets/charts/
Run from the root of your n18 repo:  python scripts/generate_charts.py
"""

import pandas as pd
import plotly.express as px
import os

# ── Config ────────────────────────────────────────────────────────────────────
CSV_PATH   = "data/cohort.csv"
OUTPUT_DIR = "assets/charts"
TEAL       = "#01696f"
COLORS     = ["#01696f","#4f98a3","#0c4e54","#cedcd8","#a3c4c7","#1a626b","#7ab5ba","#0f3638"]

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_chart(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.write_html(path, full_html=False, include_plotlyjs=False)
    print(f"  saved: {path}")

LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_family="sans-serif",
    margin=dict(l=10, r=10, t=40, b=10),
    title_font_size=14,
)

# ── Chart 1: Topic Areas ──────────────────────────────────────────────────────
topic_counts = (
    df["topic_area"]
    .str.split(" / ")
    .explode()
    .str.strip()
    .value_counts()
    .reset_index()
)
topic_counts.columns = ["topic", "count"]

fig1 = px.bar(
    topic_counts, x="count", y="topic", orientation="h",
    title="Topic Areas", color_discrete_sequence=[TEAL],
    labels={"count": "Projects", "topic": ""},
)
fig1.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"})
fig1.update_traces(marker_line_width=0)
save_chart(fig1, "topic_areas.html")

# ── Chart 2: Analysis Methods ─────────────────────────────────────────────────
def simplify_method(m):
    m = str(m).lower()
    if "mediat"      in m: return "Mediation Analysis"
    if "logistic"    in m: return "Logistic Regression"
    if "regression"  in m: return "Linear / Multiple Regression"
    if "coloc"       in m: return "Colocalisation (COLOC)"
    if "thematic"    in m: return "Thematic Analysis"
    if "ica"         in m: return "Group ICA"
    if "ancova"      in m or "mixed" in m: return "ANCOVA / Mixed Models"
    if "correlation" in m: return "Correlation"
    if "chi"         in m: return "Chi-Square / Descriptive"
    return "Other"

method_counts = (
    df["analysis"].apply(simplify_method)
    .value_counts().reset_index()
)
method_counts.columns = ["method", "count"]

fig2 = px.bar(
    method_counts, x="count", y="method", orientation="h",
    title="Analysis Methods", color_discrete_sequence=[TEAL],
    labels={"count": "Projects", "method": ""},
)
fig2.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"})
fig2.update_traces(marker_line_width=0)
save_chart(fig2, "methods.html")

# ── Chart 3: Supervisors ──────────────────────────────────────────────────────
sup_counts = (
    df["supervisor"]
    .str.split(";")
    .explode()
    .str.strip()
    .str.replace(r"^(Prof\.|Dr\.|Prof)\s+", "", regex=True)
    .value_counts()
    .reset_index()
)
sup_counts.columns = ["supervisor", "count"]

fig3 = px.bar(
    sup_counts, x="count", y="supervisor", orientation="h",
    title="Supervisors", color_discrete_sequence=[TEAL],
    labels={"count": "Projects", "supervisor": ""},
)
fig3.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"})
fig3.update_traces(marker_line_width=0)
save_chart(fig3, "supervisors.html")

# ── Chart 4: Primary vs Secondary ────────────────────────────────────────────
data_counts = df["data_type"].value_counts().reset_index()
data_counts.columns = ["type", "count"]

fig4 = px.pie(
    data_counts, names="type", values="count",
    title="Data Type", color_discrete_sequence=COLORS, hole=0.45,
)
fig4.update_layout(
    **LAYOUT,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2),
)
fig4.update_traces(textposition="inside", textinfo="percent+label")
save_chart(fig4, "data_type.html")

print("\nDone. All 4 charts saved to", OUTPUT_DIR)
