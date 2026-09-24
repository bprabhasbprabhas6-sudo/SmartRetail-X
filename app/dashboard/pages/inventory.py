from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

INVENTORY_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_recommendations.csv"
)


st.set_page_config(
    page_title="SmartRetail-X Inventory",
    page_icon="📦",
    layout="wide",
)


st.title("📦 SmartRetail-X Inventory Optimization")
st.caption("Demand-driven inventory and reorder recommendations")


# --------------------------------------------------
# Load data
# --------------------------------------------------

if not INVENTORY_PATH.exists():

    st.error(
        "Inventory recommendations not found. "
        "Run inventory_optimizer.py first."
    )

    st.stop()


inventory = pd.read_csv(INVENTORY_PATH)


# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_products = len(inventory)

total_recommended = inventory[
    "recommended_order_quantity"
].sum()

total_safety_stock = inventory[
    "safety_stock"
].sum()

high_priority = (
    inventory["inventory_priority"] == "HIGH"
).sum()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Products",
    f"{total_products:,}",
)

col2.metric(
    "Recommended Units",
    f"{total_recommended:,.0f}",
)

col3.metric(
    "Safety Stock",
    f"{total_safety_stock:,.0f}",
)

col4.metric(
    "High Priority",
    f"{high_priority:,}",
)


st.divider()


# --------------------------------------------------
# Priority distribution
# --------------------------------------------------

st.subheader("🚦 Inventory Priority Distribution")


priority_counts = (
    inventory["inventory_priority"]
    .value_counts()
    .reset_index()
)

priority_counts.columns = [
    "priority",
    "products",
]


fig_priority = px.bar(
    priority_counts,
    x="priority",
    y="products",
    title="Products by Inventory Priority",
)


st.plotly_chart(
    fig_priority,
    use_container_width=True,
)


# --------------------------------------------------
# Top reorder recommendations
# --------------------------------------------------

st.subheader("🔝 Top Reorder Recommendations")


top_reorders = inventory.head(15).copy()


fig_reorder = px.bar(
    top_reorders,
    x="recommended_order_quantity",
    y="product_name",
    orientation="h",
    title="Products Requiring the Largest Recommended Orders",
)


fig_reorder.update_layout(
    xaxis_title="Recommended Order Quantity",
    yaxis_title="Product",
)


st.plotly_chart(
    fig_reorder,
    use_container_width=True,
)


# --------------------------------------------------
# Product filter
# --------------------------------------------------

st.subheader("🔍 Product Inventory Analysis")


priority_options = [
    "ALL",
    *sorted(
        inventory["inventory_priority"]
        .dropna()
        .unique()
        .tolist()
    ),
]


selected_priority = st.selectbox(
    "Filter by priority",
    priority_options,
)


filtered = inventory.copy()


if selected_priority != "ALL":

    filtered = filtered[
        filtered["inventory_priority"]
        == selected_priority
    ]


st.dataframe(
    filtered[
        [
            "product_id",
            "product_name",
            "forecast_total_demand",
            "average_daily_demand",
            "safety_stock",
            "reorder_point",
            "recommended_order_quantity",
            "inventory_priority",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Inventory scatter analysis
# --------------------------------------------------

st.subheader("📊 Demand vs Reorder Quantity")


fig_scatter = px.scatter(
    inventory,
    x="average_daily_demand",
    y="recommended_order_quantity",
    size="safety_stock",
    hover_name="product_name",
    title="Average Daily Demand vs Recommended Order Quantity",
)


fig_scatter.update_layout(
    xaxis_title="Average Daily Demand",
    yaxis_title="Recommended Order Quantity",
)


st.plotly_chart(
    fig_scatter,
    use_container_width=True,
)


st.success(
    "Inventory optimization dashboard loaded successfully."
)