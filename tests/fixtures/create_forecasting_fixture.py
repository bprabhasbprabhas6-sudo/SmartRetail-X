from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures"
FIXTURE_PATH = FIXTURE_DIR / "forecasting_features.parquet"


def create_forecasting_fixture():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

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

    data.to_parquet(FIXTURE_PATH, index=False)

    print(f"Created fixture: {FIXTURE_PATH}")


if __name__ == "__main__":
    create_forecasting_fixture()
