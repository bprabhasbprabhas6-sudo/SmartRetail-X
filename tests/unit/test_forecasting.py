import numpy as np
import pandas as pd


def test_lag_feature_creation():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=5),
            "demand": [10, 20, 30, 40, 50],
        }
    )

    df["lag_1"] = df["demand"].shift(1)

    assert pd.isna(df.loc[0, "lag_1"])
    assert df.loc[1, "lag_1"] == 10
    assert df.loc[4, "lag_1"] == 40


def test_rolling_mean_uses_previous_values():
    df = pd.DataFrame(
        {
            "demand": [10, 20, 30, 40, 50]
        }
    )

    df["rolling_mean_3"] = (
        df["demand"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    assert pd.isna(df.loc[0, "rolling_mean_3"])
    assert pd.isna(df.loc[1, "rolling_mean_3"])
    assert pd.isna(df.loc[2, "rolling_mean_3"])

    assert df.loc[3, "rolling_mean_3"] == 20.0
    assert df.loc[4, "rolling_mean_3"] == 30.0


def test_forecast_prediction_is_non_negative():
    predictions = np.array([10.5, 0.0, 25.7, 100.2])

    predictions = np.maximum(predictions, 0)

    assert np.all(predictions >= 0)


def test_log_transform_inverse():
    demand = np.array([0, 1, 10, 100])

    transformed = np.log1p(demand)
    restored = np.expm1(transformed)

    assert np.allclose(demand, restored)