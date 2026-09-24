from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_shap_feature_importance():
    response = client.get(
        "/api/v1/explainability/feature-importance"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["method"] == "SHAP TreeExplainer"
    assert data["status"] == "success"

    assert "feature_count" in data
    assert "features" in data

    assert data["feature_count"] > 0
    assert data["feature_count"] == len(data["features"])

    # Verify expected forecasting feature exists
    assert any(
        feature["feature"] == "lag_7"
        for feature in data["features"]
    )

    # Verify SHAP values are non-negative
    for feature in data["features"]:
        assert "rank" in feature
        assert "feature" in feature
        assert "mean_abs_shap" in feature

        assert feature["rank"] >= 1
        assert feature["mean_abs_shap"] >= 0

    # Verify features are sorted by importance
    shap_values = [
        feature["mean_abs_shap"]
        for feature in data["features"]
    ]

    assert shap_values == sorted(
        shap_values,
        reverse=True
    )