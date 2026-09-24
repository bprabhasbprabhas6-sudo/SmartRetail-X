from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

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

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "xgboost_demand_forecast.json"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading forecasting data...")

train = pd.read_parquet(TRAIN_FILE)
test = pd.read_parquet(TEST_FILE)

train["date"] = pd.to_datetime(train["date"])
test["date"] = pd.to_datetime(test["date"])


# ---------------------------------------------------------
# XGBoost features
# ---------------------------------------------------------
features = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28",
    "rolling_std_7",
    "rolling_max_7",
    "year",
    "month",
    "day",
    "day_of_week",
    "week_of_year",
    "quarter",
    "is_weekend",
]


X_train = train[features]
y_train = train["demand"]

X_test = test[features]
y_test = test["demand"]


# ---------------------------------------------------------
# Train comparison model
# ---------------------------------------------------------
print("Training comparison XGBoost model...")

model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train, verbose=False)

xgb_predictions = np.maximum(
    model.predict(X_test),
    0
)


# ---------------------------------------------------------
# Baseline prediction
# ---------------------------------------------------------
baseline_predictions = test["rolling_mean_7"].values


# ---------------------------------------------------------
# Evaluation function
# ---------------------------------------------------------
def evaluate(actual, predicted):
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

    wmape = (
        np.abs(actual - predicted).sum()
        / actual.sum()
    ) * 100

    return mae, rmse, wmape


# ---------------------------------------------------------
# Calculate metrics
# ---------------------------------------------------------
baseline_mae, baseline_rmse, baseline_wmape = evaluate(
    y_test,
    baseline_predictions
)

xgb_mae, xgb_rmse, xgb_wmape = evaluate(
    y_test,
    xgb_predictions
)


# ---------------------------------------------------------
# Comparison
# ---------------------------------------------------------
results = pd.DataFrame(
    {
        "Model": [
            "7-Day Moving Average",
            "XGBoost"
        ],
        "MAE": [
            baseline_mae,
            xgb_mae
        ],
        "RMSE": [
            baseline_rmse,
            xgb_rmse
        ],
        "WMAPE (%)": [
            baseline_wmape,
            xgb_wmape
        ]
    }
)


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------
print("\n========================================")
print("FORECASTING MODEL COMPARISON")
print("========================================")

print(
    results.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------
output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "model_comparison.csv"
)

results.to_csv(
    output_file,
    index=False
)

print("\nComparison saved to:")
print(output_file)