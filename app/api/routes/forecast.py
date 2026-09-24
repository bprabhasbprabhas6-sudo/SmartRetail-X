from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1",
    tags=["Forecasting"]
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "xgboost_demand_forecast_log.json"
)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "forecasting_features.parquet"
)


# ============================================================
# MODEL FEATURES
# ============================================================

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


# ============================================================
# LOAD MODEL
# ============================================================

model = None

if MODEL_PATH.exists():
    model = xgb.XGBRegressor()
    model.load_model(str(MODEL_PATH))


# ============================================================
# REQUEST SCHEMA
# ============================================================

class ForecastRequest(BaseModel):
    product_id: str


# ============================================================
# FORECAST ENDPOINT
# ============================================================

@router.post("/forecast")
def forecast_demand(request: ForecastRequest):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Forecasting model not found."
        )

    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Forecasting feature dataset not found."
        )

    # Load forecasting data
    df = pd.read_parquet(DATA_PATH)

    # Check product
    product_data = df[
        df["product_id"].astype(str) == str(request.product_id)
    ].copy()

    if product_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Product {request.product_id} was not found."
        )

    # Sort by date
    if "date" in product_data.columns:
        product_data = product_data.sort_values("date")

    # Use latest available row
    latest_row = product_data.iloc[-1]

    # Check required features
    missing_features = [
        feature
        for feature in FEATURES
        if feature not in product_data.columns
    ]

    if missing_features:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Required forecasting features are missing.",
                "missing_features": missing_features,
            }
        )

    # Create model input
    X = pd.DataFrame(
        [latest_row[FEATURES].values],
        columns=FEATURES
    )

    # Convert boolean to integer
    if "is_weekend" in X.columns:
        X["is_weekend"] = X["is_weekend"].astype(int)

    # Handle missing values
    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    X = X.fillna(0)

    # Predict log demand
    log_prediction = model.predict(X)[0]

    # Convert back to original demand scale
    prediction = np.expm1(log_prediction)

    prediction = max(
        0,
        float(prediction)
    )

    return {
        "product_id": request.product_id,
        "predicted_demand": round(prediction, 2),
        "model": "xgboost_demand_forecast_log",
        "status": "success",
    }