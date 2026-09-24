import numpy as np
import pandas as pd


def calculate_anomaly_score(value, rolling_mean, rolling_std):
    if rolling_std == 0:
        return 0.0

    return (value - rolling_mean) / rolling_std


def classify_anomaly(score, threshold=3.0):
    if score >= threshold:
        return "DEMAND_SPIKE"

    if score <= -threshold:
        return "DEMAND_DROP"

    return "NORMAL"


def test_positive_anomaly_score():
    score = calculate_anomaly_score(
        value=100,
        rolling_mean=50,
        rolling_std=10,
    )

    assert score == 5.0


def test_negative_anomaly_score():
    score = calculate_anomaly_score(
        value=20,
        rolling_mean=50,
        rolling_std=10,
    )

    assert score == -3.0


def test_demand_spike_classification():
    assert classify_anomaly(3.5) == "DEMAND_SPIKE"


def test_demand_drop_classification():
    assert classify_anomaly(-3.5) == "DEMAND_DROP"


def test_normal_classification():
    assert classify_anomaly(1.5) == "NORMAL"


def test_zero_standard_deviation():
    score = calculate_anomaly_score(
        value=100,
        rolling_mean=100,
        rolling_std=0,
    )

    assert score == 0.0


def test_anomaly_score_calculation_with_dataframe():
    df = pd.DataFrame(
        {
            "demand": [100, 120, 200],
            "rolling_mean": [100, 100, 100],
            "rolling_std": [10, 10, 20],
        }
    )

    df["anomaly_score"] = (
        (df["demand"] - df["rolling_mean"])
        / df["rolling_std"]
    )

    assert np.isclose(df.loc[1, "anomaly_score"], 2.0)
    assert np.isclose(df.loc[2, "anomaly_score"], 5.0)