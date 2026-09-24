from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

RECOMMENDATION_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "product_recommendations.csv"
)


st.set_page_config(
    page_title="Product Recommendations",
    page_icon="🛍️",
    layout="wide",
)


st.title("🛍️ SmartRetail-X Recommendation Engine")
st.caption("Product recommendations based on customer co-purchase behavior")


# --------------------------------------------------
# Load recommendations
# --------------------------------------------------

if not RECOMMENDATION_PATH.exists():

    st.error(
        "Recommendation file not found. "
        "Run recommendation_engine.py first."
    )

    st.stop()


recommendations = pd.read_csv(
    RECOMMENDATION_PATH
)


if recommendations.empty:

    st.warning(
        "No recommendation relationships were generated."
    )

    st.stop()


# --------------------------------------------------
# KPIs
# --------------------------------------------------

products = (
    recommendations["product_key_x"]
    .nunique()
)

pairs = len(recommendations)

avg_similarity = (
    recommendations["similarity"]
    .mean()
)

max_similarity = (
    recommendations["similarity"]
    .max()
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Products",
    f"{products:,}",
)

col2.metric(
    "Recommendation Pairs",
    f"{pairs:,}",
)

col3.metric(
    "Avg Similarity",
    f"{avg_similarity:.3f}",
)

col4.metric(
    "Max Similarity",
    f"{max_similarity:.3f}",
)


st.divider()


# --------------------------------------------------
# Top recommendation relationships
# --------------------------------------------------

st.subheader("🔝 Strongest Product Relationships")


top_relationships = (
    recommendations
    .sort_values(
        [
            "similarity",
            "co_purchase_count",
        ],
        ascending=False,
    )
    .head(15)
    .copy()
)


top_relationships["relationship"] = (
    top_relationships["product_x_name"]
    + " → "
    + top_relationships["product_y_name"]
)


fig = px.bar(
    top_relationships,
    x="similarity",
    y="relationship",
    orientation="h",
    title="Top Product Recommendation Relationships",
)


fig.update_layout(
    xaxis_title="Similarity",
    yaxis_title="Product Relationship",
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# Product selector
# --------------------------------------------------

st.subheader("🔍 Find Product Recommendations")


product_list = (
    recommendations[
        [
            "product_key_x",
            "product_x_name",
        ]
    ]
    .drop_duplicates()
    .sort_values("product_x_name")
)


selected_product: int = st.selectbox(
    "Select a product",
    product_list["product_key_x"],
    format_func=lambda x: product_list.loc[
        product_list["product_key_x"] == x,
        "product_x_name",
    ].iloc[0],
)


selected = recommendations[
    recommendations["product_key_x"]
    == selected_product
].copy()


selected = selected.sort_values(
    [
        "similarity",
        "co_purchase_count",
    ],
    ascending=False,
)


st.write(
    f"### Recommended products for "
    f"**{selected['product_x_name'].iloc[0]}**"
)


# --------------------------------------------------
# Recommendation table
# --------------------------------------------------

display_columns = [
    "product_y_id",
    "product_y_name",
    "co_purchase_count",
    "similarity",
    "recommendation_rank",
]


st.dataframe(
    selected[display_columns],
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Recommendation chart
# --------------------------------------------------

chart_data = selected.head(10)


fig_recommendations = px.bar(
    chart_data,
    x="similarity",
    y="product_y_name",
    orientation="h",
    title="Recommended Products",
)


fig_recommendations.update_layout(
    xaxis_title="Similarity",
    yaxis_title="Recommended Product",
)


st.plotly_chart(
    fig_recommendations,
    use_container_width=True,
)


st.success(
    "Recommendation dashboard loaded successfully."
)