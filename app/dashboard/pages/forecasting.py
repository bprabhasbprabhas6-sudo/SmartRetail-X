from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "forecast_7_days.csv"
)


st.set_page_config(
    page_title="SmartRetail-X Forecasting",
    page_icon="📈",
    layout="wide",
)


st.title("📈 SmartRetail-X Demand Forecasting")
st.caption("7-Day Product Demand Forecast")


# --------------------------------------------------
# Load forecast
# --------------------------------------------------

if not FORECAST_PATH.exists():

    st.error(
        "Forecast file not found. "
        "Run generate_7day_forecast.py first."
    )

    st.stop()


forecast = pd.read_csv(FORECAST_PATH)

forecast["date"] = pd.to_datetime(forecast["date"])

forecast["predicted_demand"] = pd.to_numeric(
    forecast["predicted_demand"],
    errors="coerce",
).fillna(0)


# --------------------------------------------------
# KPI section
# --------------------------------------------------

total_demand = forecast["predicted_demand"].sum()

forecast_days = forecast["date"].nunique()

products = forecast["product_id"].nunique()

average_daily_demand = (
    total_demand / forecast_days
    if forecast_days > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Forecast Horizon",
    f"{forecast_days} Days",
)

col2.metric(
    "Products",
    f"{products:,}",
)

col3.metric(
    "Predicted Units",
    f"{total_demand:,.0f}",
)

col4.metric(
    "Avg Daily Demand",
    f"{average_daily_demand:,.0f}",
)


st.divider()


# --------------------------------------------------
# Daily forecast
# --------------------------------------------------

st.subheader("📅 Daily Predicted Demand")


daily = (
    forecast
    .groupby("date", as_index=False)["predicted_demand"]
    .sum()
)


fig_daily = px.line(
    daily,
    x="date",
    y="predicted_demand",
    markers=True,
    title="Total Predicted Demand by Day",
)


fig_daily.update_layout(
    xaxis_title="Date",
    yaxis_title="Predicted Units",
)


st.plotly_chart(
    fig_daily,
    use_container_width=True,
)


# --------------------------------------------------
# Product ranking
# --------------------------------------------------

st.subheader("🔝 Top Products by Forecasted Demand")


product_summary = (
    forecast
    .groupby(
        ["product_id", "product_name"],
        as_index=False,
    )["predicted_demand"]
    .sum()
    .to_frame()
)

top_products = product_summary.head(10)


fig_products = px.bar(
    top_products,
    x="predicted_demand",
    y="product_name",
    orientation="h",
    title="Top 10 Products",
)


fig_products.update_layout(
    xaxis_title="Predicted Units",
    yaxis_title="Product",
)


st.plotly_chart(
    fig_products,
    use_container_width=True,
)


# --------------------------------------------------
# Product selector
# --------------------------------------------------

st.subheader("🔍 Product-Level Forecast")


product_options = (
    forecast[
        ["product_id", "product_name"]
    ]
    .drop_duplicates()
    .sort_values("product_name")
)


selected_product: str = st.selectbox(
    "Select a product",
    product_options["product_id"],
    format_func=lambda x: product_options.loc[
        product_options["product_id"] == x,
        "product_name",
    ].iloc[0],
)


selected_data = forecast[
    forecast["product_id"] == selected_product
].copy()


fig_product = px.line(
    selected_data,
    x="date",
    y="predicted_demand",
    markers=True,
    title="7-Day Product Demand Forecast",
)


fig_product.update_layout(
    xaxis_title="Date",
    yaxis_title="Predicted Units",
)


st.plotly_chart(
    fig_product,
    use_container_width=True,
)


# --------------------------------------------------
# Forecast table
# --------------------------------------------------

st.subheader("📋 Forecast Details")

display_data = forecast.copy()

display_data["date"] = display_data[
    "date"
].dt.strftime("%Y-%m-%d")


st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
)


st.success(
    "7-day demand forecasting dashboard loaded successfully."
)