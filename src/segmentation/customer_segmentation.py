from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = __import__("os").getenv("DATABASE_URL")

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_segments.csv"
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

engine = create_engine(DATABASE_URL)


# --------------------------------------------------
# Build RFM dataset
# --------------------------------------------------

print("Loading customer transaction data...")

query = """
SELECT
    customer_key,
    MAX(invoice_date)::DATE AS last_purchase_date,
    COUNT(DISTINCT invoice_id) AS frequency,
    SUM(sales_revenue) AS monetary
FROM analytics.fact_sales
WHERE transaction_type = 'SALE'
  AND customer_key IS NOT NULL
GROUP BY customer_key
"""


rfm = pd.read_sql(query, engine)

print(f"Customers found: {len(rfm):,}")


# --------------------------------------------------
# Recency
# --------------------------------------------------

# Convert PostgreSQL date values to Pandas datetime
rfm["last_purchase_date"] = pd.to_datetime(
    rfm["last_purchase_date"],
    errors="coerce"
)

analysis_date = rfm["last_purchase_date"].max()

rfm["recency"] = (
    analysis_date - rfm["last_purchase_date"]
).dt.days

# --------------------------------------------------
# Remove invalid values
# --------------------------------------------------

rfm["frequency"] = rfm["frequency"].clip(lower=1)

rfm["monetary"] = rfm["monetary"].clip(lower=0)


# --------------------------------------------------
# RFM scoring
# --------------------------------------------------

print("Calculating RFM scores...")


rfm["r_score"] = pd.qcut(
    rfm["recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1],
).astype(int)


rfm["f_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5],
).astype(int)


rfm["m_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5],
).astype(int)


rfm["rfm_score"] = (
    rfm["r_score"].astype(str)
    + rfm["f_score"].astype(str)
    + rfm["m_score"].astype(str)
)


# --------------------------------------------------
# Customer segmentation
# --------------------------------------------------

def assign_segment(row):

    r = row["r_score"]
    f = row["f_score"]
    m = row["m_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    if r >= 3 and f >= 4:
        return "Loyal Customers"

    if r >= 4 and f <= 3:
        return "Potential Loyalists"

    if r <= 2 and f >= 3:
        return "At Risk"

    return "Lost Customers"


rfm["segment"] = rfm.apply(
    assign_segment,
    axis=1,
)


# --------------------------------------------------
# Business action
# --------------------------------------------------

segment_actions = {

    "Champions":
        "Reward loyalty and encourage referrals",

    "Loyal Customers":
        "Upsell and cross-sell relevant products",

    "Potential Loyalists":
        "Use personalized offers to increase frequency",

    "At Risk":
        "Run retention campaigns and targeted incentives",

    "Lost Customers":
        "Use win-back campaigns and reactivation offers",
}


rfm["recommended_action"] = (
    rfm["segment"]
    .map(segment_actions)
)


# --------------------------------------------------
# Save
# --------------------------------------------------

rfm = rfm.sort_values(
    ["segment", "monetary"],
    ascending=[True, False],
)


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


rfm.to_csv(
    OUTPUT_PATH,
    index=False,
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n========================================")
print("CUSTOMER SEGMENTATION RESULTS")
print("========================================")

print(f"Analysis date: {analysis_date}")
print(f"Customers analyzed: {len(rfm):,}")


print("\nSegment distribution:")

print(
    rfm["segment"]
    .value_counts()
    .to_string()
)


print("\nSegment summary:")

summary = (
    rfm
    .groupby("segment")
    .agg(
        customers=("customer_key", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    )
    .round(2)
    .sort_values(
        "customers",
        ascending=False,
    )
)


print(summary.to_string())


print("\nOutput saved to:")
print(OUTPUT_PATH)

print("\nCustomer segmentation completed successfully.")