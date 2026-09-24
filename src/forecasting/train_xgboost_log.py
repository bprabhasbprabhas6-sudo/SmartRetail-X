from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_PATH = BASE_DIR / "data" / "processed" / "forecasting" / "train.parquet"
TEST_PATH = BASE_DIR / "data" / "processed" / "forecasting" / "test.parquet"

MODEL_PATH = BASE_DIR / "models" / "xgboost_demand_forecast_log.json"


FEATURES = [
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


def wmape(actual, predicted):
    denominator = np.sum(np.abs(actual))

    if denominator == 0:
        return 0.0

    return np.sum(np.abs(actual - predicted)) / denominator * 100


print("Loading training and test data...")

train = pd.read_parquet(TRAIN_PATH)
test = pd.read_parquet(TEST_PATH)

print(f"Training rows: {len(train):,}")
print(f"Testing rows: {len(test):,}")

X_train = train[FEATURES]
X_test = test[FEATURES]

y_train = train["demand"]
y_test = test["demand"]

print(f"Features: {len(FEATURES)}")

print("\nTransforming target using log1p...")

y_train_log = np.log1p(y_train)

print("Training XGBoost model...")

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

model.fit(X_train, y_train_log)

print("Generating predictions...")

pred_log = model.predict(X_test)

# Convert predictions back to original demand scale
predictions = np.expm1(pred_log)

# Demand cannot be negative
predictions = np.maximum(predictions, 0)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
wmape_value = wmape(y_test.values, predictions)

print("\n========================================")
print("LOG-TARGET XGBOOST RESULTS")
print("========================================")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"WMAPE: {wmape_value:.2f}%")

importance = (
    pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": model.feature_importances_,
        }
    )
    .sort_values("importance", ascending=False)
)

print("\nTop Feature Importance:")
print(importance.head(10).to_string(index=False))

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

model.save_model(MODEL_PATH)

print("\nModel saved to:")
print(MODEL_PATH)

print("\nLog-target XGBoost forecasting completed successfully.")