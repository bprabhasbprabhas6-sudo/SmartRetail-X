from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/anomalies",
    tags=["Sales Anomaly Detection"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

ANOMALY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sales_anomalies.csv"
)


class AnomalyRequest(BaseModel):
    product_id: str


@router.post("/product")
def get_product_anomalies(request: AnomalyRequest):

    if not ANOMALY_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Sales anomaly file not found."
        )

    df = pd.read_csv(ANOMALY_FILE)

    product_data = df[
        df["product_id"].astype(str) == str(request.product_id)
    ].copy()

    if product_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No anomaly records found for product {request.product_id}."
        )

    product_data = product_data.sort_values("date")

    anomalies = []

    for _, row in product_data.iterrows():
        anomalies.append({
            "date": str(row["date"]),
            "product_id": str(row["product_id"]),
            "product_name": str(row["product_name"]),
            "demand": int(row["demand"]),
            "revenue": round(float(row["revenue"]), 2),
            "rolling_mean": round(float(row["rolling_mean"]), 2),
            "rolling_std": round(float(row["rolling_std"]), 2),
            "anomaly_score": round(float(row["anomaly_score"]), 2),
            "anomaly_type": str(row["anomaly_type"]),
            "absolute_deviation": round(
                float(row["absolute_deviation"]), 2
            )
        })

    return {
        "product_id": request.product_id,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "status": "success"
    }