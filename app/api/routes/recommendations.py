from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Product Recommendations"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RECOMMENDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "product_recommendations.csv"
)


class RecommendationRequest(BaseModel):
    product_id: str
    limit: int = 5


@router.post("/")
def get_recommendations(request: RecommendationRequest):

    if not RECOMMENDATION_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Product recommendation file not found."
        )

    if request.limit < 1 or request.limit > 10:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 10."
        )

    df = pd.read_csv(RECOMMENDATION_FILE)

    product_data = df[
        df["product_x_id"].astype(str) == str(request.product_id)
    ].copy()

    if product_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No recommendations found for product {request.product_id}."
        )

    product_data = product_data.sort_values(
        "recommendation_rank"
    ).head(request.limit)

    recommendations = []

    for _, row in product_data.iterrows():
        recommendations.append({
            "product_id": str(row["product_y_id"]),
            "product_name": str(row["product_y_name"]),
            "similarity": round(float(row["similarity"]), 4),
            "co_purchase_count": int(row["co_purchase_count"]),
            "recommendation_rank": int(row["recommendation_rank"])
        })

    return {
        "product_id": request.product_id,
        "recommendations": recommendations,
        "count": len(recommendations),
        "status": "success"
    }