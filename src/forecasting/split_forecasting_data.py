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
    / "forecasting_features.parquet"
)

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "train.parquet"
)

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting"
    / "test.parquet"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading forecasting features...")

df = pd.read_parquet(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)

print(f"Total rows: {len(df):,}")
print(f"Start date: {df['date'].min().date()}")
print(f"End date: {df['date'].max().date()}")


# ---------------------------------------------------------
# Determine time-based split
# ---------------------------------------------------------
unique_dates = sorted(df["date"].unique())

split_index = int(len(unique_dates) * 0.80)

split_date = unique_dates[split_index]

print(f"\nSplit date: {pd.Timestamp(split_date).date()}")


# ---------------------------------------------------------
# Train / Test split
# ---------------------------------------------------------
train = df[
    df["date"] < split_date
].copy()

test = df[
    df["date"] >= split_date
].copy()


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------
train.to_parquet(
    TRAIN_FILE,
    index=False
)

test.to_parquet(
    TEST_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\nTime-based split completed!")

print("\nTRAINING DATA")
print(f"Rows: {len(train):,}")
print(f"Start: {train['date'].min().date()}")
print(f"End: {train['date'].max().date()}")
print(f"Products: {train['product_id'].nunique():,}")

print("\nTEST DATA")
print(f"Rows: {len(test):,}")
print(f"Start: {test['date'].min().date()}")
print(f"End: {test['date'].max().date()}")
print(f"Products: {test['product_id'].nunique():,}")

print("\nFiles created:")
print(TRAIN_FILE)
print(TEST_FILE)