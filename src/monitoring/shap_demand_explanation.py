from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import shap
import xgboost as xgb

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "train.parquet"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "xgboost_demand_forecast_log.json"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "explainability"
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


# --------------------------------------------------
# Load data
# --------------------------------------------------

print("Loading training data...")

train = pd.read_parquet(TRAIN_PATH)

X = train[FEATURES]

# Use a sample so SHAP remains efficient
sample_size = min(3000, len(X))

X_sample = X.sample(
    n=sample_size,
    random_state=42,
)

print(
    f"SHAP sample size: {len(X_sample):,}"
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

print("Loading XGBoost model...")

model = xgb.XGBRegressor()

model.load_model(
    MODEL_PATH
)

print("Model loaded successfully.")


# --------------------------------------------------
# Create SHAP explainer
# --------------------------------------------------

print("Creating SHAP explainer...")

explainer = shap.TreeExplainer(
    model
)

shap_values = explainer.shap_values(
    X_sample
)


# --------------------------------------------------
# Output directory
# --------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# Global feature importance
# --------------------------------------------------

print("Calculating global feature importance...")

importance = pd.DataFrame(
    {
        "feature": FEATURES,
        "mean_abs_shap": abs(shap_values).mean(axis=0),
    }
)

importance = importance.sort_values(
    "mean_abs_shap",
    ascending=False,
)


importance_path = (
    OUTPUT_DIR
    / "shap_feature_importance.csv"
)

importance.to_csv(
    importance_path,
    index=False,
)


print("\n========================================")
print("SHAP FEATURE IMPORTANCE")
print("========================================")

print(
    importance.to_string(
        index=False
    )
)


# --------------------------------------------------
# SHAP summary plot
# --------------------------------------------------

print("\nCreating SHAP summary plot...")

plt.figure()

shap.summary_plot(
    shap_values,
    X_sample,
    show=False,
)

plt.tight_layout()

summary_path = (
    OUTPUT_DIR
    / "shap_summary.png"
)

plt.savefig(
    summary_path,
    dpi=200,
    bbox_inches="tight",
)

plt.close()


# --------------------------------------------------
# SHAP bar plot
# --------------------------------------------------

print("Creating SHAP bar plot...")

plt.figure()

shap.summary_plot(
    shap_values,
    X_sample,
    plot_type="bar",
    show=False,
)

plt.tight_layout()

bar_path = (
    OUTPUT_DIR
    / "shap_feature_importance.png"
)

plt.savefig(
    bar_path,
    dpi=200,
    bbox_inches="tight",
)

plt.close()


print("\nFiles created:")

print(importance_path)
print(summary_path)
print(bar_path)

print("\nSHAP explainability completed successfully.")