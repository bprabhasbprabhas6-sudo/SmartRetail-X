from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "daily_product_demand.parquet"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "forecasting_training_data.parquet"
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
TOP_N_PRODUCTS = 20


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading forecasting dataset...")

df = pd.read_parquet(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

print(f"Original rows: {len(df):,}")
print(f"Original products: {df['product_id'].nunique():,}")


# ---------------------------------------------------------
# Select top products by total demand
# ---------------------------------------------------------
product_demand = (
    df.groupby(
        ["product_id", "product_name"],
        as_index=False
    )
    .agg(
        total_demand=("demand", "sum"),
        total_revenue=("revenue", "sum"),
        active_days=("date", "nunique")
    )
    .sort_values(
        "total_demand",
        ascending=False
    )
)

top_products = product_demand.head(TOP_N_PRODUCTS)

selected_ids = top_products["product_id"].tolist()

print("\nSelected products:")
print(
    top_products[
        [
            "product_id",
            "product_name",
            "total_demand",
            "total_revenue",
            "active_days"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Filter dataset
# ---------------------------------------------------------
df = df[
    df["product_id"].isin(selected_ids)
].copy()


# ---------------------------------------------------------
# Create complete daily date range
# ---------------------------------------------------------
min_date = df["date"].min()
max_date = df["date"].max()

all_dates = pd.date_range(
    start=min_date,
    end=max_date,
    freq="D"
)

print(f"\nDate range: {min_date.date()} → {max_date.date()}")
print(f"Total dates: {len(all_dates):,}")


# ---------------------------------------------------------
# Create product-date combinations
# ---------------------------------------------------------
products = (
    df[
        ["product_id", "product_name"]
    ]
    .drop_duplicates()
)

calendar = pd.DataFrame(
    {
        "date": all_dates
    }
)

calendar["key"] = 1
products["key"] = 1

complete = calendar.merge(
    products,
    on="key"
).drop(columns="key")


# ---------------------------------------------------------
# Merge actual demand
# ---------------------------------------------------------
complete = complete.merge(
    df[
        [
            "date",
            "product_id",
            "demand",
            "revenue"
        ]
    ],
    on=["date", "product_id"],
    how="left"
)


# ---------------------------------------------------------
# Missing product-days = zero demand
# ---------------------------------------------------------
complete["demand"] = (
    complete["demand"]
    .fillna(0)
)

complete["revenue"] = (
    complete["revenue"]
    .fillna(0)
)


# ---------------------------------------------------------
# Calendar features
# ---------------------------------------------------------
complete["year"] = complete["date"].dt.year
complete["month"] = complete["date"].dt.month
complete["day"] = complete["date"].dt.day
complete["day_of_week"] = complete["date"].dt.dayofweek
complete["week_of_year"] = (
    complete["date"]
    .dt.isocalendar()
    .week
    .astype(int)
)
complete["quarter"] = complete["date"].dt.quarter
complete["is_weekend"] = (
    complete["day_of_week"] >= 5
).astype(int)


# ---------------------------------------------------------
# Sort
# ---------------------------------------------------------
complete = complete.sort_values(
    ["product_id", "date"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------
complete.to_parquet(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\nForecasting training dataset created!")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(complete):,}")
print(f"Products: {complete['product_id'].nunique():,}")
print(f"Dates: {complete['date'].nunique():,}")
print(
    f"Zero-demand rows: "
    f"{(complete['demand'] == 0).sum():,}"
)

print("\nColumns:")
print(complete.columns.tolist())