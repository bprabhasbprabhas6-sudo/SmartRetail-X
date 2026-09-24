from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures"


def create_forecasting_fixture():
    data = pd.DataFrame(
        [
            {
                "product_id": "85123A",
                "date": pd.Timestamp("2011-12-09"),
                "lag_1": 20.0,
                "lag_7": 18.0,
                "lag_14": 21.0,
                "lag_28": 19.0,
                "rolling_mean_7": 19.5,
                "rolling_mean_14": 20.0,
                "rolling_mean_28": 20.5,
                "rolling_std_7": 3.0,
                "rolling_max_7": 25.0,
                "month": 12,
                "day_of_week": 4,
                "is_weekend": False,
            }
        ]
    )

    data.to_parquet(
        FIXTURE_DIR / "forecasting_features.parquet",
        index=False,
    )


def create_anomaly_fixture():
    data = pd.DataFrame(
        [
            {
                "date": "2011-12-01",
                "product_id": "37410",
                "product_name": "Test Product",
                "demand": 20,
                "revenue": 200.0,
                "rolling_mean": 15.0,
                "rolling_std": 2.0,
                "anomaly_score": 2.5,
                "anomaly_type": "DEMAND_SPIKE",
                "absolute_deviation": 5.0,
            }
        ]
    )

    data.to_csv(
        FIXTURE_DIR / "sales_anomalies.csv",
        index=False,
    )


def create_customer_segment_fixture():
    data = pd.DataFrame(
        [
            {
                "customer_key": 1,
                "recency": 10,
                "frequency": 12,
                "monetary": 77556.46,
                "r_score": 5,
                "f_score": 5,
                "m_score": 5,
                "rfm_score": 555,
                "segment": "Champions",
                "recommended_action": "Reward and retain",
            }
        ]
    )

    data.to_csv(
        FIXTURE_DIR / "customer_segments.csv",
        index=False,
    )


def create_shap_fixture():
    data = pd.DataFrame(
        [
            {
                "feature": "lag_1",
                "mean_abs_shap": 0.80,
            },
            {
                "feature": "rolling_mean_7",
                "mean_abs_shap": 0.60,
            },
            {
                "feature": "lag_7",
                "mean_abs_shap": 0.40,
            },
        ]
    )

    data.to_csv(
        FIXTURE_DIR / "shap_feature_importance.csv",
        index=False,
    )


def create_inventory_fixture():
    data = pd.DataFrame(
        [
            {
                "product_id": "85123A",
                "average_daily_demand": 22.17,
                "demand_std": 20.85,
                "safety_stock": 91.02,
                "reorder_point": 246.20,
                "target_inventory": 401.38,
                "recommended_order_quantity": 401.38,
                "inventory_priority": "LOW",
            }
        ]
    )

    data.to_csv(
        FIXTURE_DIR / "inventory_recommendations.csv",
        index=False,
    )


def create_recommendation_fixture():
    data = pd.DataFrame(
        [
            {
                "product_x_id": "23131",
                "product_y_id": "10001",
                "product_y_name": "Test Product A",
                "similarity": 0.90,
                "co_purchase_count": 10,
                "recommendation_rank": 1,
            },
            {
                "product_x_id": "23131",
                "product_y_id": "10002",
                "product_y_name": "Test Product B",
                "similarity": 0.80,
                "co_purchase_count": 8,
                "recommendation_rank": 2,
            },
            {
                "product_x_id": "23131",
                "product_y_id": "10003",
                "product_y_name": "Test Product C",
                "similarity": 0.70,
                "co_purchase_count": 6,
                "recommendation_rank": 3,
            },
            {
                "product_x_id": "23131",
                "product_y_id": "10004",
                "product_y_name": "Test Product D",
                "similarity": 0.60,
                "co_purchase_count": 5,
                "recommendation_rank": 4,
            },
            {
                "product_x_id": "23131",
                "product_y_id": "10005",
                "product_y_name": "Test Product E",
                "similarity": 0.50,
                "co_purchase_count": 4,
                "recommendation_rank": 5,
            },
        ]
    )

    data.to_csv(
        FIXTURE_DIR / "product_recommendations.csv",
        index=False,
    )


def create_all_fixtures():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    create_forecasting_fixture()
    create_anomaly_fixture()
    create_customer_segment_fixture()
    create_shap_fixture()
    create_inventory_fixture()
    create_recommendation_fixture()

    print(f"Created test fixtures in: {FIXTURE_DIR}")


if __name__ == "__main__":
    create_all_fixtures()