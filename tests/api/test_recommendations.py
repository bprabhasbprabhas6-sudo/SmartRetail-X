from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import recommendations

client = TestClient(app)


def test_product_recommendations(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "product_recommendations.csv"
    )

    monkeypatch.setattr(
        recommendations,
        "RECOMMENDATION_FILE",
        fixture_path,
    )

    response = client.post(
        "/api/v1/recommendations/",
        json={
            "product_id": "23131",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "23131"
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5
    assert data["status"] == "success"

    assert data["recommendations"][0]["product_id"] == "10001"
    assert data["recommendations"][0]["recommendation_rank"] == 1