from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

SEGMENT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_segments.csv"
)


st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide",
)


st.title("👥 SmartRetail-X Customer Segmentation")
st.caption("RFM-based customer intelligence")


# --------------------------------------------------
# Load data
# --------------------------------------------------

if not SEGMENT_PATH.exists():

    st.error(
        "Customer segmentation file not found. "
        "Run customer_segmentation.py first."
    )

    st.stop()


rfm = pd.read_csv(SEGMENT_PATH)


# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_customers = len(rfm)

total_revenue = rfm["monetary"].sum()

average_revenue = rfm["monetary"].mean()

champions = (
    rfm["segment"] == "Champions"
).sum()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{total_customers:,}",
)

col2.metric(
    "Customer Revenue",
    f"₹{total_revenue:,.0f}",
)

col3.metric(
    "Avg Customer Revenue",
    f"₹{average_revenue:,.2f}",
)

col4.metric(
    "Champions",
    f"{champions:,}",
)


st.divider()


# --------------------------------------------------
# Segment distribution
# --------------------------------------------------

st.subheader("📊 Customer Segment Distribution")


segment_counts = (
    rfm["segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "segment",
    "customers",
]


fig_segments = px.bar(
    segment_counts,
    x="segment",
    y="customers",
    title="Customers by Segment",
)


fig_segments.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Number of Customers",
)


st.plotly_chart(
    fig_segments,
    use_container_width=True,
)


# --------------------------------------------------
# Revenue by segment
# --------------------------------------------------

st.subheader("💰 Revenue by Customer Segment")


segment_revenue = (
    rfm
    .groupby("segment", as_index=False)
    .agg(
        revenue=("monetary", "sum"),
        customers=("customer_key", "count"),
    )
    .sort_values(
        "revenue",
        ascending=False,
    )
)


fig_revenue = px.bar(
    segment_revenue,
    x="segment",
    y="revenue",
    title="Revenue Contribution by Segment",
)


fig_revenue.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Revenue",
)


st.plotly_chart(
    fig_revenue,
    use_container_width=True,
)


# --------------------------------------------------
# RFM relationship
# --------------------------------------------------

st.subheader("🔎 Customer Value Distribution")


fig_scatter = px.scatter(
    rfm,
    x="frequency",
    y="monetary",
    size="recency",
    color="segment",
    hover_data=[
        "customer_key",
        "recency",
        "frequency",
        "monetary",
    ],
    title="Frequency vs Monetary Value",
)


fig_scatter.update_layout(
    xaxis_title="Purchase Frequency",
    yaxis_title="Monetary Value",
)


st.plotly_chart(
    fig_scatter,
    use_container_width=True,
)


# --------------------------------------------------
# Segment filter
# --------------------------------------------------

st.subheader("🔍 Customer Details")


segment_options = [
    "ALL",
    *sorted(
        rfm["segment"]
        .dropna()
        .unique()
        .tolist()
    ),
]


selected_segment = st.selectbox(
    "Select customer segment",
    segment_options,
)


filtered = rfm.copy()


if selected_segment != "ALL":

    filtered = filtered[
        filtered["segment"]
        == selected_segment
    ]


st.dataframe(
    filtered[
        [
            "customer_key",
            "last_purchase_date",
            "recency",
            "frequency",
            "monetary",
            "r_score",
            "f_score",
            "m_score",
            "rfm_score",
            "segment",
            "recommended_action",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)


st.success(
    "Customer segmentation dashboard loaded successfully."
)