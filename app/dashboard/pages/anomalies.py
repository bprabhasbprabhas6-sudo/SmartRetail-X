from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

ANOMALY_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_anomalies.csv"
)


st.set_page_config(
    page_title="Sales Anomaly Detection",
    page_icon="🚨",
    layout="wide",
)


st.title("🚨 SmartRetail-X Anomaly Detection")
st.caption("Detection of unusual product-demand behavior")


# --------------------------------------------------
# Load data
# --------------------------------------------------

if not ANOMALY_PATH.exists():

    st.error(
        "Anomaly file not found. "
        "Run detect_sales_anomalies.py first."
    )

    st.stop()


anomalies = pd.read_csv(ANOMALY_PATH)

anomalies["date"] = pd.to_datetime(
    anomalies["date"]
)


# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_anomalies = len(anomalies)

spikes = (
    anomalies["anomaly_type"]
    == "DEMAND_SPIKE"
).sum()

drops = (
    anomalies["anomaly_type"]
    == "DEMAND_DROP"
).sum()

products_affected = (
    anomalies["product_id"]
    .nunique()
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Anomalies",
    f"{total_anomalies:,}",
)

col2.metric(
    "Demand Spikes",
    f"{spikes:,}",
)

col3.metric(
    "Demand Drops",
    f"{drops:,}",
)

col4.metric(
    "Products Affected",
    f"{products_affected:,}",
)


st.divider()


# --------------------------------------------------
# Anomaly type distribution
# --------------------------------------------------

st.subheader("📊 Anomaly Distribution")


type_counts = (
    anomalies["anomaly_type"]
    .value_counts()
    .reset_index()
)

type_counts.columns = [
    "anomaly_type",
    "count",
]


fig_types = px.bar(
    type_counts,
    x="anomaly_type",
    y="count",
    title="Demand Spikes vs Demand Drops",
)


fig_types.update_layout(
    xaxis_title="Anomaly Type",
    yaxis_title="Number of Anomalies",
)


st.plotly_chart(
    fig_types,
    use_container_width=True,
)


# --------------------------------------------------
# Anomalies over time
# --------------------------------------------------

st.subheader("📅 Anomalies Over Time")


daily_anomalies = (
    anomalies
    .groupby(
        "date",
        as_index=False,
    )
    .size()
)

daily_anomalies.columns = [
    "date",
    "anomaly_count",
]


fig_time = px.line(
    daily_anomalies,
    x="date",
    y="anomaly_count",
    markers=True,
    title="Daily Anomaly Count",
)


fig_time.update_layout(
    xaxis_title="Date",
    yaxis_title="Anomalies",
)


st.plotly_chart(
    fig_time,
    use_container_width=True,
)


# --------------------------------------------------
# Top affected products
# --------------------------------------------------

st.subheader("🔝 Most Affected Products")


top_products = (
    anomalies
    .groupby(
        [
            "product_id",
            "product_name",
        ],
        as_index=False,
    )
    .size()
    .sort_values(
        "size",
        ascending=False,
    )
    .head(15)
)


top_products = top_products.rename(
    columns={
        "size": "anomaly_count"
    }
)


fig_products = px.bar(
    top_products,
    x="anomaly_count",
    y="product_name",
    orientation="h",
    title="Products with Most Anomalies",
)


fig_products.update_layout(
    xaxis_title="Anomaly Count",
    yaxis_title="Product",
)


st.plotly_chart(
    fig_products,
    use_container_width=True,
)


# --------------------------------------------------
# Anomaly score distribution
# --------------------------------------------------

st.subheader("📈 Anomaly Score Distribution")


fig_score = px.histogram(
    anomalies,
    x="anomaly_score",
    nbins=40,
    title="Distribution of Anomaly Scores",
)


fig_score.update_layout(
    xaxis_title="Anomaly Score",
    yaxis_title="Frequency",
)


st.plotly_chart(
    fig_score,
    use_container_width=True,
)


# --------------------------------------------------
# Filter
# --------------------------------------------------

st.subheader("🔍 Anomaly Details")


filter_options = [
    "ALL",
    "DEMAND_SPIKE",
    "DEMAND_DROP",
]


selected_type = st.selectbox(
    "Filter by anomaly type",
    filter_options,
)


filtered = anomalies.copy()


if selected_type != "ALL":

    filtered = filtered[
        filtered["anomaly_type"]
        == selected_type
    ]


st.dataframe(
    filtered[
        [
            "date",
            "product_id",
            "product_name",
            "demand",
            "rolling_mean",
            "rolling_std",
            "anomaly_score",
            "anomaly_type",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)


st.success(
    "Anomaly detection dashboard loaded successfully."
)