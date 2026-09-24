from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/customer",
    tags=["Customer Segmentation"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SEGMENT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_segments.csv"
)


class CustomerSegmentRequest(BaseModel):
    customer_key: int


@router.post("/segment")
def customer_segment(request: CustomerSegmentRequest):

    if not SEGMENT_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Customer segmentation file not found."
        )

    df = pd.read_csv(SEGMENT_FILE)

    customer_data = df[
        df["customer_key"] == request.customer_key
    ]

    if customer_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {request.customer_key} was not found."
        )

    row = customer_data.iloc[0]

    return {
        "customer_key": int(row["customer_key"]),
        "recency": int(row["recency"]),
        "frequency": int(row["frequency"]),
        "monetary": round(float(row["monetary"]), 2),
        "r_score": int(row["r_score"]),
        "f_score": int(row["f_score"]),
        "m_score": int(row["m_score"]),
        "rfm_score": int(row["rfm_score"]),
        "segment": str(row["segment"]),
        "recommended_action": str(row["recommended_action"]),
        "status": "success"
    }