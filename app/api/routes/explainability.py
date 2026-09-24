from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/v1/explainability",
    tags=["Explainable AI"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SHAP_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "explainability"
    / "shap_feature_importance.csv"
)


@router.get("/feature-importance")
def get_shap_feature_importance():

    if not SHAP_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="SHAP feature importance file not found."
        )

    df = pd.read_csv(SHAP_FILE)

    df = df.sort_values(
        "mean_abs_shap",
        ascending=False
    ).reset_index(drop=True)

    features = []

    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        features.append({
            "rank": rank,
            "feature": str(row["feature"]),
            "mean_abs_shap": round(
                float(row["mean_abs_shap"]),
                6
            )
        })

    return {
        "method": "SHAP TreeExplainer",
        "feature_count": len(features),
        "features": features,
        "status": "success"
    }