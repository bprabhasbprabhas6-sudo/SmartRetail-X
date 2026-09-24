import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import mlflow
import mlflow.xgboost
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from configs.mlflow_config import (
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_TRACKING_URI,
)

BASE_DIR = PROJECT_ROOT

TRAIN_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "train.parquet"
)

TEST_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "test.parquet"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "xgboost_demand_forecast_log.json"
)

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

    return (
        np.sum(np.abs(actual - predicted))
        / denominator
        * 100
    )


print("Configuring MLflow...")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

print(f"MLflow experiment: {MLFLOW_EXPERIMENT_NAME}")
print(f"MLflow tracking URI: {MLFLOW_TRACKING_URI}")

print("\nLoading training and test data...")

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

params = {
    "objective": "reg:squarederror",
    "n_estimators": 800,
    "learning_rate": 0.03,
    "max_depth": 6,
    "min_child_weight": 5,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 2.0,
    "random_state": 42,
    "n_jobs": -1,
}

with mlflow.start_run(
    run_name="xgboost_log_demand_forecast"
):
    print("\nTraining XGBoost model...")

    model = XGBRegressor(**params)

    model.fit(X_train, y_train_log)

    print("Generating predictions...")

    pred_log = model.predict(X_test)

    predictions = np.expm1(pred_log)

    predictions = np.maximum(predictions, 0)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions,
        )
    )

    wmape_value = wmape(
        y_test.values,
        predictions,
    )

    print("\n========================================")
    print("LOG-TARGET XGBOOST RESULTS")
    print("========================================")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"WMAPE: {wmape_value:.2f}%")

    print("\nLogging parameters...")

    mlflow.log_params(params)

    mlflow.log_param(
        "target_transformation",
        "log1p",
    )

    mlflow.log_param(
        "feature_count",
        len(FEATURES),
    )

    mlflow.log_param(
        "training_rows",
        len(train),
    )

    mlflow.log_param(
        "testing_rows",
        len(test),
    )

    print("Logging metrics...")

    mlflow.log_metric("mae", float(mae))
    mlflow.log_metric("rmse", float(rmse))
    mlflow.log_metric("wmape", float(wmape_value))

    importance = (
        pd.DataFrame(
            {
                "feature": FEATURES,
                "importance": model.feature_importances_,
            }
        )
        .sort_values(
            "importance",
            ascending=False,
        )
    )

    print("\nTop Feature Importance:")
    print(
        importance.head(10).to_string(
            index=False
        )
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    model.save_model(MODEL_PATH)

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nLogging XGBoost model to MLflow...")

    mlflow.xgboost.log_model(
        model,
        name="xgboost_demand_forecast",
    )

    print("\nMLflow run completed successfully.")

    active_run = mlflow.active_run()

if active_run is not None:
    print(f"Run ID: {active_run.info.run_id}")

print("\nLog-target XGBoost forecasting completed successfully.")