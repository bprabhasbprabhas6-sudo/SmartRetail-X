from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "daily_product_demand.parquet"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_anomalies.csv"
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROLLING_WINDOW = 28
ANOMALY_THRESHOLD = 3.0


# --------------------------------------------------
# Load data
# --------------------------------------------------

print("Loading daily product demand...")

df = pd.read_parquet(INPUT_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["product_id", "date"]
)

print(f"Rows: {len(df):,}")
print(f"Products: {df['product_id'].nunique():,}")


# --------------------------------------------------
# Rolling statistics
# --------------------------------------------------

grouped = df.groupby(
    "product_id"
)["demand"]


df["rolling_mean"] = (
    grouped
    .transform(
        lambda x: x.shift(1)
        .rolling(ROLLING_WINDOW, min_periods=7)
        .mean()
    )
)


df["rolling_std"] = (
    grouped
    .transform(
        lambda x: x.shift(1)
        .rolling(ROLLING_WINDOW, min_periods=7)
        .std()
    )
)


# --------------------------------------------------
# Calculate anomaly score
# --------------------------------------------------

df["anomaly_score"] = (
    (df["demand"] - df["rolling_mean"])
    /
    df["rolling_std"].replace(0, np.nan)
)


df["anomaly_score"] = (
    df["anomaly_score"]
    .replace(
        [np.inf, -np.inf],
        np.nan,
    )
    .fillna(0)
)


# --------------------------------------------------
# Classify anomalies
# --------------------------------------------------

df["anomaly_type"] = np.select(
    [
        df["anomaly_score"] >= ANOMALY_THRESHOLD,
        df["anomaly_score"] <= -ANOMALY_THRESHOLD,
    ],
    [
        "DEMAND_SPIKE",
        "DEMAND_DROP",
    ],
    default="NORMAL",
)


anomalies = df[
    df["anomaly_type"] != "NORMAL"
].copy()


# --------------------------------------------------
# Add anomaly magnitude
# --------------------------------------------------

anomalies["absolute_deviation"] = (
    anomalies["demand"]
    - anomalies["rolling_mean"]
).abs()


anomalies = anomalies.sort_values(
    "absolute_deviation",
    ascending=False,
)


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


anomalies.to_csv(
    OUTPUT_PATH,
    index=False,
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n========================================")
print("SALES ANOMALY DETECTION")
print("========================================")

print(
    f"Total observations: {len(df):,}"
)

print(
    f"Anomalies detected: {len(anomalies):,}"
)

print(
    f"Anomaly rate: "
    f"{len(anomalies) / len(df) * 100:.2f}%"
)


print("\nAnomaly types:")

print(
    anomalies["anomaly_type"]
    .value_counts()
    .to_string()
)


print("\nTop anomalies:")

print(
    anomalies[
        [
            "date",
            "product_id",
            "product_name",
            "demand",
            "rolling_mean",
            "rolling_std",
            "anomaly_score",
            "anomaly_type",
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\nOutput saved to:")
print(OUTPUT_PATH)

print("\nAnomaly detection completed successfully.")