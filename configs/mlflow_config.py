from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"

MLFLOW_TRACKING_URI = f"sqlite:///{MLFLOW_DB_PATH.as_posix()}"

MLFLOW_EXPERIMENT_NAME = "SmartRetail-X Demand Forecasting"