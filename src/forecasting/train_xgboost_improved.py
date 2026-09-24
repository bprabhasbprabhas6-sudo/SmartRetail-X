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

MODEL_FILE = (
    MODEL_DIR
    / "xgboost_demand_forecast_improved.json"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading forecasting data...")

train = pd.read_parquet(TRAIN_FILE)
test = pd.read_parquet(TEST_FILE)


# ---------------------------------------------------------
# Features
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
    "month",
    "day_of_week",
    "is_weekend",
]


X_train = train[features]
y_train = train["demand"]

X_test = test[features]
y_test = test["demand"]


print(f"Training rows: {len(X_train):,}")
print(f"Testing rows: {len(X_test):,}")
print(f"Features: {len(features)}")


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------
print("\nTraining improved XGBoost model...")

model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=800,
    learning_rate=0.03,
    max_depth=6,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=2.0,
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

wmape = (
    np.abs(
        y_test - predictions
    ).sum()
    / y_test.sum()
) * 100


# ---------------------------------------------------------
# Feature importance
# ---------------------------------------------------------
importance = pd.DataFrame(
    {
        "feature": features,
        "importance": model.feature_importances_,
    }
).sort_values(
    "importance",
    ascending=False
)


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------
model.save_model(MODEL_FILE)


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------
print("\n========================================")
print("IMPROVED XGBOOST FORECASTING RESULTS")
print("========================================")

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"WMAPE: {wmape:.2f}%")

print("\nFeature Importance:")

print(
    importance.to_string(
        index=False
    )
)

print("\nModel saved to:")
print(MODEL_FILE)

print("\nImproved forecasting completed successfully.")