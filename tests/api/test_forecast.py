from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import forecast

client = TestClient(app)


def test_forecast_api(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "forecasting_features.parquet"
    )

    monkeypatch.setattr(
        forecast,
        "DATA_PATH",
        fixture_path,
    )

    response = client.post(
        "/api/v1/forecast",
        json={
            "product_id": "85123A"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "85123A"
    assert "predicted_demand" in data
    assert data["predicted_demand"] >= 0
    assert data["model"] == "xgboost_demand_forecast_log"
    assert data["status"] == "success"
