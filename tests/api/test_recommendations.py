from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_product_recommendations():
    response = client.post(
        "/api/v1/recommendations/",
        json={
            "product_id": "23131",
            "limit": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "23131"
    assert data["status"] == "success"

    assert "recommendations" in data
    assert "count" in data

    assert data["count"] <= 5

    for recommendation in data["recommendations"]:
        assert "product_id" in recommendation
        assert "product_name" in recommendation
        assert "similarity" in recommendation
        assert "co_purchase_count" in recommendation
        assert "recommendation_rank" in recommendation

        assert recommendation["similarity"] >= 0
        assert recommendation["co_purchase_count"] >= 0
        assert recommendation["recommendation_rank"] >= 1