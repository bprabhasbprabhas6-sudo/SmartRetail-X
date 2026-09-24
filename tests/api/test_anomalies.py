from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import anomalies

client = TestClient(app)


def test_product_anomalies(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "sales_anomalies.csv"
    )

    monkeypatch.setattr(
        anomalies,
        "ANOMALY_FILE",
        fixture_path,
    )

    response = client.post(
        "/api/v1/anomalies/product",
        json={
            "product_id": "37410"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "37410"
    assert data["anomaly_count"] > 0
    assert "anomalies" in data
    assert data["status"] == "success"