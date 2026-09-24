from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import customer_segment

client = TestClient(app)


def test_customer_segment(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "customer_segments.csv"
    )

    monkeypatch.setattr(
        customer_segment,
        "SEGMENT_FILE",
        fixture_path,
    )

    response = client.post(
        "/api/v1/customer/segment",
        json={
            "customer_key": 1
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_key"] == 1
    assert data["segment"] == "Champions"
    assert "recommended_action" in data
    assert data["status"] == "success"