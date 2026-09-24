from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_customer_segment():
    response = client.post(
        "/api/v1/customer/segment",
        json={
            "customer_key": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_key"] == 1

    assert data["recency"] >= 0
    assert data["frequency"] >= 0
    assert data["monetary"] >= 0

    assert 1 <= data["r_score"] <= 5
    assert 1 <= data["f_score"] <= 5
    assert 1 <= data["m_score"] <= 5

    assert "rfm_score" in data
    assert "segment" in data
    assert "recommended_action" in data

    assert data["status"] == "success"