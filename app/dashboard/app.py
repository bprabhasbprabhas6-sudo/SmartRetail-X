import streamlit as st

st.set_page_config(
    page_title="SmartRetail-X",
    page_icon="🛒",
    layout="wide"
)


st.title("🛒 SmartRetail-X")

st.subheader(
    "Real-Time Retail Intelligence, Demand Forecasting "
    "& Inventory Optimization Platform"
)

st.markdown(
    """
    ## Welcome to SmartRetail-X

    SmartRetail-X is an end-to-end retail analytics platform
    designed to transform transaction data into actionable
    business intelligence.

    ### Available Modules

    Use the sidebar to explore:

    - 📈 **Demand Forecasting**
    - 📦 **Inventory Optimization**
    - 👥 **Customer Segmentation**
    - 🛍️ **Product Recommendations**
    - 🚨 **Sales Anomaly Detection**
    - 🔍 **Explainable AI**

    ### Technology Stack

    **Python · Pandas · Scikit-learn · XGBoost · SHAP ·
    PostgreSQL · FastAPI · Streamlit · Plotly**
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Platform", "SmartRetail-X")

with col2:
    st.metric("ML Modules", "5+")

with col3:
    st.metric("Explainability", "SHAP")

st.info(
    "Select a module from the sidebar to explore the corresponding "
    "analytics and machine-learning capabilities."
)

st.caption(
    "SmartRetail-X | Retail Intelligence Platform"
)