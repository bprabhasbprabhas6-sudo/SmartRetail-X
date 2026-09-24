from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import (
    anomalies,
    customer_segment,
    explainability,
    forecast,
    inventory,
    recommendations,
)

client = TestClient(app)


def test_smartretail_api_workflow(monkeypatch):
    fixture_dir = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
    )

    monkeypatch.setattr(
        forecast,
        "DATA_PATH",
        fixture_dir / "forecasting_features.parquet",
    )

    monkeypatch.setattr(
        inventory,
        "INVENTORY_FILE",
        fixture_dir / "inventory_recommendations.csv",
    )

    monkeypatch.setattr(
        recommendations,
        "RECOMMENDATION_FILE",
        fixture_dir / "product_recommendations.csv",
    )

    monkeypatch.setattr(
        customer_segment,
        "SEGMENT_FILE",
        fixture_dir / "customer_segments.csv",
    )

    monkeypatch.setattr(
        anomalies,
        "ANOMALY_FILE",
        fixture_dir / "sales_anomalies.csv",
    )

    monkeypatch.setattr(
        explainability,
        "SHAP_FILE",
        fixture_dir / "shap_feature_importance.csv",
    )

    # 1. Check API health
    health_response = client.get("/health")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "healthy"

    # 2. Request demand forecast
    forecast_response = client.post(
        "/api/v1/forecast",
        json={
            "product_id": "85123A"
        },
    )

    assert forecast_response.status_code == 200

    forecast_data = forecast_response.json()

    assert forecast_data["product_id"] == "85123A"
    assert forecast_data["predicted_demand"] >= 0

    # 3. Use forecast-related information for inventory planning
    inventory_response = client.post(
        "/api/v1/inventory/recommendation",
        json={
            "product_id": "85123A"
        },
    )

    assert inventory_response.status_code == 200

    inventory_data = inventory_response.json()

    assert inventory_data["product_id"] == "85123A"
    assert inventory_data["reorder_point"] >= 0
    assert inventory_data["recommended_order_quantity"] >= 0

    # 4. Get product recommendations
    recommendation_response = client.post(
        "/api/v1/recommendations/",
        json={
            "product_id": "23131",
            "limit": 5,
        },
    )

    assert recommendation_response.status_code == 200

    recommendation_data = recommendation_response.json()

    assert recommendation_data["product_id"] == "23131"
    assert recommendation_data["status"] == "success"
    assert recommendation_data["count"] <= 5

    # 5. Get customer segmentation
    customer_response = client.post(
        "/api/v1/customer/segment",
        json={
            "customer_key": 1,
        },
    )

    assert customer_response.status_code == 200

    customer_data = customer_response.json()

    assert customer_data["customer_key"] == 1
    assert customer_data["segment"]

    # 6. Check anomaly detection
    anomaly_response = client.post(
        "/api/v1/anomalies/product",
        json={
            "product_id": "37410",
        },
    )

    assert anomaly_response.status_code == 200

    anomaly_data = anomaly_response.json()

    assert anomaly_data["product_id"] == "37410"
    assert anomaly_data["anomaly_count"] >= 0

    # 7. Check explainability
    shap_response = client.get(
        "/api/v1/explainability/feature-importance"
    )

    assert shap_response.status_code == 200

    shap_data = shap_response.json()

    assert shap_data["status"] == "success"
    assert shap_data["feature_count"] > 0