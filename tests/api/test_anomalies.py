from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_product_anomalies():
    response = client.post(
        "/api/v1/anomalies/product",
        json={
            "product_id": "37410"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "37410"
    assert data["status"] == "success"

    assert "anomaly_count" in data
    assert "anomalies" in data

    assert data["anomaly_count"] == len(data["anomalies"])

    for anomaly in data["anomalies"]:
        assert "date" in anomaly
        assert "product_id" in anomaly
        assert "product_name" in anomaly
        assert "demand" in anomaly
        assert "revenue" in anomaly
        assert "rolling_mean" in anomaly
        assert "rolling_std" in anomaly
        assert "anomaly_score" in anomaly
        assert "anomaly_type" in anomaly
        assert "absolute_deviation" in anomaly

        assert anomaly["demand"] >= 0
        assert anomaly["rolling_std"] >= 0
        assert anomaly["anomaly_type"] in [
            "DEMAND_SPIKE",
            "DEMAND_DROP",
            "NORMAL"
        ]