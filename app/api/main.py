from datetime import datetime, timezone

from fastapi import FastAPI

from app.api.routes.anomalies import router as anomalies_router
from app.api.routes.customer_segment import router as customer_segment_router
from app.api.routes.explainability import router as explainability_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.recommendations import router as recommendations_router

app = FastAPI(
    title="SmartRetail-X API",
    description=(
        "Retail Intelligence, Demand Forecasting, "
        "Inventory Optimization and Explainable AI API"
    ),
    version="1.0.0",
)


# Register API routers
app.include_router(forecast_router)
app.include_router(inventory_router)
app.include_router(customer_segment_router)
app.include_router(recommendations_router)
app.include_router(anomalies_router)
app.include_router(explainability_router)


@app.get("/")
def root():
    return {
        "project": "SmartRetail-X",
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SmartRetail-X API",
    }


@app.get("/api/v1/info")
def project_info():
    return {
        "project": "SmartRetail-X",
        "version": "1.0.0",
        "modules": [
            "Demand Forecasting",
            "Inventory Optimization",
            "Customer Segmentation",
            "Product Recommendations",
            "Anomaly Detection",
            "Explainable AI",
        ],
    }