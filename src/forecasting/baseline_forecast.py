from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "train.parquet"
)

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "test.parquet"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading train and test data...")

train = pd.read_parquet(TRAIN_FILE)
test = pd.read_parquet(TEST_FILE)

train["date"] = pd.to_datetime(train["date"])
test["date"] = pd.to_datetime(test["date"])


# ---------------------------------------------------------
# Baseline prediction
# ---------------------------------------------------------
# The forecasting feature `rolling_mean_7` was calculated
# using only previous days, so it can be used as a baseline.
test = test.copy()

test["prediction"] = test["rolling_mean_7"]


# ---------------------------------------------------------
# Remove missing predictions
# ---------------------------------------------------------
test = test.dropna(
    subset=["prediction", "demand"]
).copy()


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------
actual = test["demand"]
predicted = test["prediction"]

mae = mean_absolute_error(
    actual,
    predicted
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        predicted
    )
)


# ---------------------------------------------------------
# WMAPE
# ---------------------------------------------------------
total_actual = actual.sum()

if total_actual != 0:
    wmape = (
        np.abs(actual - predicted).sum()
        / total_actual
    ) * 100
else:
    wmape = 0


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------
print("\n========================================")
print("7-DAY MOVING AVERAGE BASELINE")
print("========================================")

print(f"Test rows: {len(test):,}")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"WMAPE: {wmape:.2f}%")

print("\nBaseline evaluation completed successfully.")