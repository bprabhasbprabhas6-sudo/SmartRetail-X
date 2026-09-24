
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INVENTORY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "inventory_recommendations.csv"
)


class InventoryRequest(BaseModel):
    product_id: str


@router.post("/recommendation")
def inventory_recommendation(request: InventoryRequest):

    if not INVENTORY_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Inventory recommendations file not found."
        )

    df = pd.read_csv(INVENTORY_FILE)

    product_data = df[
        df["product_id"].astype(str) == str(request.product_id)
    ]

    if product_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Product {request.product_id} was not found."
        )

    row = product_data.iloc[0]

    return {
        "product_id": request.product_id,
        "average_daily_demand": float(
            row["average_daily_demand"]
        ),
        "demand_std": float(
            row["demand_std"]
        ),
        "safety_stock": float(
            row["safety_stock"]
        ),
        "reorder_point": float(
            row["reorder_point"]
        ),
        "target_inventory": float(
            row["target_inventory"]
        ),
        "recommended_order_quantity": float(
            row["recommended_order_quantity"]
        ),
        "inventory_priority": str(
            row["inventory_priority"]
        ),
        "status": "success"
    }