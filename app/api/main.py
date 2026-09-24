from datetime import UTC, datetime
from time import perf_counter

from fastapi import FastAPI, Request

from app.api.routes.anomalies import router as anomalies_router
from app.api.routes.customer_segment import router as customer_segment_router
from app.api.routes.explainability import router as explainability_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.recommendations import router as recommendations_router
from configs.logging_config import logger

app = FastAPI(
    title="SmartRetail-X API",
    description=(
        "Retail Intelligence, Demand Forecasting, "
        "Inventory Optimization and Explainable AI API"
    ),
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log API requests, response status codes, and response times."""

    start_time = perf_counter()

    logger.info(
        "Request started | method=%s | path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        elapsed_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Request completed | method=%s | path=%s | status=%s | duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )

        return response

    except Exception:
        elapsed_ms = (perf_counter() - start_time) * 1000

        logger.exception(
            "Request failed | method=%s | path=%s | duration_ms=%.2f",
            request.method,
            request.url.path,
            elapsed_ms,
        )

        raise


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
        "timestamp": datetime.now(UTC).isoformat(),
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