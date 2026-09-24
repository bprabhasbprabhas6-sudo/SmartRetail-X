import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "forecasting"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "daily_product_demand.parquet"


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv(PROJECT_ROOT / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL not found in .env")


# ---------------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------------
engine = create_engine(database_url)


# ---------------------------------------------------------
# SQL query
# ---------------------------------------------------------
query = """
SELECT
    f.invoice_date::DATE AS date,
    f.product_key,
    p.product_id,
    p.product_name,
    SUM(f.sales_quantity) AS demand,
    SUM(f.sales_revenue) AS revenue
FROM analytics.fact_sales f
JOIN analytics.dim_product p
    ON f.product_key = p.product_key
WHERE f.transaction_type = 'SALE'
GROUP BY
    f.invoice_date::DATE,
    f.product_key,
    p.product_id,
    p.product_name
ORDER BY
    date,
    product_id;
"""


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
print("Loading sales data from PostgreSQL...")

df = pd.read_sql(query, engine)

print(f"Rows loaded: {len(df):,}")
print(f"Products: {df['product_id'].nunique():,}")
print(f"Date range: {df['date'].min()} → {df['date'].max()}")


# ---------------------------------------------------------
# Data validation
# ---------------------------------------------------------
df["date"] = pd.to_datetime(df["date"])

df["demand"] = pd.to_numeric(df["demand"], errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

df = df.dropna(
    subset=["date", "product_id", "demand"]
)

df = df[df["demand"] >= 0].copy()


# ---------------------------------------------------------
# Time features
# ---------------------------------------------------------
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
df["quarter"] = df["date"].dt.quarter
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)


# ---------------------------------------------------------
# Sort
# ---------------------------------------------------------
df = df.sort_values(
    ["product_id", "date"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Save dataset
# ---------------------------------------------------------
df.to_parquet(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Final summary
# ---------------------------------------------------------
print("\nForecasting dataset created successfully!")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Products: {df['product_id'].nunique():,}")
print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")

print("\nColumns:")
print(df.columns.tolist())

print("\nSample:")
print(df.head(10).to_string(index=False))