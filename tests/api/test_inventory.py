from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_inventory_recommendation():
    response = client.post(
        "/api/v1/inventory/recommendation",
        json={
            "product_id": "85123A"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "85123A"
    assert data["average_daily_demand"] >= 0
    assert data["demand_std"] >= 0
    assert data["safety_stock"] >= 0
    assert data["reorder_point"] >= 0
    assert data["target_inventory"] >= 0
    assert data["recommended_order_quantity"] >= 0
    assert data["inventory_priority"] in [
        "HIGH",
        "MEDIUM",
        "LOW",
        "VERY LOW"
    ]
    assert data["status"] == "success"