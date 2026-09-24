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

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "xgboost_demand_forecast.json"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading training and test data...")

train = pd.read_parquet(TRAIN_FILE)
test = pd.read_parquet(TEST_FILE)

train["date"] = pd.to_datetime(train["date"])
test["date"] = pd.to_datetime(test["date"])


# ---------------------------------------------------------
# Features
# ---------------------------------------------------------
feature_columns = [
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


# ---------------------------------------------------------
# Prepare X and y
# ---------------------------------------------------------
X_train = train[feature_columns]
y_train = train["demand"]

X_test = test[feature_columns]
y_test = test["demand"]


print(f"Training rows: {len(X_train):,}")
print(f"Testing rows: {len(X_test):,}")
print(f"Features: {len(feature_columns)}")


# ---------------------------------------------------------
# XGBoost model
# ---------------------------------------------------------
print("\nTraining XGBoost model...")

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


# ---------------------------------------------------------
# Train
# ---------------------------------------------------------
model.fit(
    X_train,
    y_train,
    verbose=False
)


# ---------------------------------------------------------
# Predict
# ---------------------------------------------------------
print("Generating predictions...")

predictions = model.predict(X_test)

# Demand cannot be negative
predictions = np.maximum(
    predictions,
    0
)


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------
mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

total_actual = y_test.sum()

if total_actual != 0:
    wmape = (
        np.abs(
            y_test - predictions
        ).sum()
        / total_actual
    ) * 100
else:
    wmape = 0


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------
model.save_model(MODEL_FILE)


# ---------------------------------------------------------
# Feature importance
# ---------------------------------------------------------
importance = pd.DataFrame(
    {
        "feature": feature_columns,
        "importance": model.feature_importances_,
    }
).sort_values(
    "importance",
    ascending=False
)


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------
print("\n========================================")
print("XGBOOST DEMAND FORECASTING RESULTS")
print("========================================")

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"WMAPE: {wmape:.2f}%")

print("\nTop Feature Importance:")

print(
    importance.head(10)
    .to_string(index=False)
)

print("\nModel saved to:")
print(MODEL_FILE)

print("\nXGBoost forecasting completed successfully.")