from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import inventory

client = TestClient(app)


def test_inventory_recommendation(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "inventory_recommendations.csv"
    )

    monkeypatch.setattr(
        inventory,
        "INVENTORY_FILE",
        fixture_path,
    )

    response = client.post(
        "/api/v1/inventory/recommendation",
        json={
            "product_id": "85123A"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "85123A"
    assert data["inventory_priority"] == "LOW"
    assert data["recommended_order_quantity"] >= 0
    assert data["reorder_point"] > 0
    assert data["status"] == "success"