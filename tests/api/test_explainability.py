from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import explainability

client = TestClient(app)


def test_shap_feature_importance(monkeypatch):
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "shap_feature_importance.csv"
    )

    monkeypatch.setattr(
        explainability,
        "SHAP_FILE",
        fixture_path,
    )

    response = client.get(
        "/api/v1/explainability/feature-importance"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["method"] == "SHAP TreeExplainer"
    assert "features" in data
    assert data["feature_count"] == 3
    assert len(data["features"]) == 3

    assert data["features"][0]["feature"] == "lag_1"
    assert data["features"][0]["mean_abs_shap"] == 0.80
    assert data["features"][0]["rank"] == 1

    assert data["status"] == "success"