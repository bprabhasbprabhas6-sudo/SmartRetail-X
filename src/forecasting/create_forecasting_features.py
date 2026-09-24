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
    / "forecasting_training_data.parquet"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "forecasting_features.parquet"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading forecasting training data...")

df = pd.read_parquet(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["product_id", "date"]
).reset_index(drop=True)

print(f"Rows loaded: {len(df):,}")
print(f"Products: {df['product_id'].nunique():,}")


# ---------------------------------------------------------
# Create lag features
# ---------------------------------------------------------
print("\nCreating lag features...")

grouped_demand = df.groupby(
    "product_id"
)["demand"]

df["lag_1"] = grouped_demand.shift(1)
df["lag_7"] = grouped_demand.shift(7)
df["lag_14"] = grouped_demand.shift(14)
df["lag_28"] = grouped_demand.shift(28)


# ---------------------------------------------------------
# Create rolling demand features
# ---------------------------------------------------------
print("Creating rolling features...")

df["rolling_mean_7"] = (
    df.groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(7).mean()
    )
)

df["rolling_mean_14"] = (
    df.groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(14).mean()
    )
)

df["rolling_mean_28"] = (
    df.groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(28).mean()
    )
)


# ---------------------------------------------------------
# Additional demand features
# ---------------------------------------------------------
df["rolling_std_7"] = (
    df.groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(7).std()
    )
)

df["rolling_max_7"] = (
    df.groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(7).max()
    )
)


# ---------------------------------------------------------
# Save rows with complete historical features
# ---------------------------------------------------------
feature_columns = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28",
    "rolling_std_7",
    "rolling_max_7",
]

before = len(df)

df = df.dropna(
    subset=feature_columns
).copy()

after = len(df)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------
df.to_parquet(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\nForecasting features created successfully!")

print(f"Output: {OUTPUT_FILE}")
print(f"Rows before feature cleanup: {before:,}")
print(f"Rows after feature cleanup: {after:,}")
print(f"Rows removed: {before - after:,}")
print(f"Products: {df['product_id'].nunique():,}")

print("\nFeature columns:")

for column in feature_columns:
    print(f" - {column}")

print("\nSample:")
print(
    df[
        [
            "date",
            "product_id",
            "demand",
            "lag_1",
            "lag_7",
            "lag_14",
            "lag_28",
            "rolling_mean_7",
            "rolling_mean_14",
            "rolling_mean_28",
        ]
    ].head(10).to_string(index=False)
)