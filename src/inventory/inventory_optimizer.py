from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "forecast_7_days.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_recommendations.csv"
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

LEAD_TIME_DAYS = 7
SERVICE_LEVEL_Z = 1.65
REVIEW_PERIOD_DAYS = 7


# --------------------------------------------------
# Load forecast
# --------------------------------------------------

print("Loading 7-day demand forecast...")

forecast = pd.read_csv(FORECAST_PATH)

forecast["date"] = pd.to_datetime(forecast["date"])

forecast["predicted_demand"] = pd.to_numeric(
    forecast["predicted_demand"],
    errors="coerce",
).fillna(0)

print(f"Forecast rows: {len(forecast):,}")


# --------------------------------------------------
# Product-level demand statistics
# --------------------------------------------------

product_stats = (
    forecast
    .groupby(
        ["product_id", "product_name"],
        as_index=False,
    )
    .agg(
        forecast_total_demand=("predicted_demand", "sum"),
        average_daily_demand=("predicted_demand", "mean"),
        demand_std=("predicted_demand", "std"),
    )
)

product_stats["demand_std"] = (
    product_stats["demand_std"]
    .fillna(0)
)


# --------------------------------------------------
# Inventory calculations
# --------------------------------------------------

# Safety Stock
product_stats["safety_stock"] = (
    SERVICE_LEVEL_Z
    * product_stats["demand_std"]
    * np.sqrt(LEAD_TIME_DAYS)
)


# Reorder Point
product_stats["reorder_point"] = (
    product_stats["average_daily_demand"]
    * LEAD_TIME_DAYS
    + product_stats["safety_stock"]
)


# Expected demand during review period
product_stats["review_period_demand"] = (
    product_stats["average_daily_demand"]
    * REVIEW_PERIOD_DAYS
)


# Target inventory level
product_stats["target_inventory"] = (
    product_stats["reorder_point"]
    + product_stats["review_period_demand"]
)


# Recommended order quantity
product_stats["recommended_order_quantity"] = (
    product_stats["target_inventory"]
)


# Round inventory quantities
inventory_columns = [
    "forecast_total_demand",
    "average_daily_demand",
    "demand_std",
    "safety_stock",
    "reorder_point",
    "review_period_demand",
    "target_inventory",
    "recommended_order_quantity",
]

for column in inventory_columns:
    product_stats[column] = (
        product_stats[column]
        .clip(lower=0)
        .round(2)
    )


# --------------------------------------------------
# Inventory priority
# --------------------------------------------------

product_stats["inventory_priority"] = np.select(
    [
        product_stats["recommended_order_quantity"] >= 1000,
        product_stats["recommended_order_quantity"] >= 500,
        product_stats["recommended_order_quantity"] >= 100,
    ],
    [
        "HIGH",
        "MEDIUM",
        "LOW",
    ],
    default="VERY LOW",
)


# --------------------------------------------------
# Save results
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

product_stats = product_stats.sort_values(
    "recommended_order_quantity",
    ascending=False,
)

product_stats.to_csv(
    OUTPUT_PATH,
    index=False,
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n========================================")
print("INVENTORY OPTIMIZATION RESULTS")
print("========================================")

print(
    f"Products analyzed: "
    f"{len(product_stats):,}"
)

print(
    f"Lead time: "
    f"{LEAD_TIME_DAYS} days"
)

print(
    f"Service-level Z value: "
    f"{SERVICE_LEVEL_Z}"
)

print("\nTop inventory recommendations:")

print(
    product_stats[
        [
            "product_id",
            "product_name",
            "forecast_total_demand",
            "safety_stock",
            "reorder_point",
            "recommended_order_quantity",
            "inventory_priority",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\nPriority distribution:")

print(
    product_stats["inventory_priority"]
    .value_counts()
    .to_string()
)


print("\nOutput saved to:")
print(OUTPUT_PATH)

print("\nInventory optimization completed successfully.")