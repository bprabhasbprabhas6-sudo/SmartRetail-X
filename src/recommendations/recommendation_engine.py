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
    / "product_recommendations.csv"
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

engine = create_engine(DATABASE_URL)


# --------------------------------------------------
# Load customer-product purchases
# --------------------------------------------------

print("Loading customer purchase data...")

query = """
SELECT DISTINCT
    customer_key,
    product_key
FROM analytics.fact_sales
WHERE transaction_type = 'SALE'
  AND customer_key IS NOT NULL
  AND product_key IS NOT NULL
"""

purchases = pd.read_sql(
    query,
    engine,
)

print(
    f"Purchase relationships: "
    f"{len(purchases):,}"
)


# --------------------------------------------------
# Product information
# --------------------------------------------------

product_query = """
SELECT
    product_key,
    product_id,
    product_name
FROM analytics.dim_product
"""

products = pd.read_sql(
    product_query,
    engine,
)


# --------------------------------------------------
# Create product pairs
# --------------------------------------------------

print("Building product co-purchase relationships...")

merged = purchases.merge(
    purchases,
    on="customer_key",
)

# Remove self-pairs
merged = merged[
    merged["product_key_x"]
    != merged["product_key_y"]
]


# Avoid duplicate pair direction
merged = merged[
    merged["product_key_x"]
    < merged["product_key_y"]
]


pair_counts = (
    merged
    .groupby(
        [
            "product_key_x",
            "product_key_y",
        ],
        as_index=False,
    )
    .size()
    .rename(
        columns={
            "size": "co_purchase_count"
        }
    )
)


# --------------------------------------------------
# Product purchase counts
# --------------------------------------------------

product_counts = (
    purchases
    .groupby("product_key")
    .size()
    .reset_index(
        name="purchase_count"
    )
)


# --------------------------------------------------
# Calculate recommendation strength
# --------------------------------------------------

pair_counts = pair_counts.merge(
    product_counts.rename(
        columns={
            "product_key": "product_key_x",
            "purchase_count": "product_x_purchases",
        }
    ),
    on="product_key_x",
    how="left",
)


pair_counts = pair_counts.merge(
    product_counts.rename(
        columns={
            "product_key": "product_key_y",
            "purchase_count": "product_y_purchases",
        }
    ),
    on="product_key_y",
    how="left",
)


# Jaccard-style similarity
pair_counts["similarity"] = (
    pair_counts["co_purchase_count"]
    /
    (
        pair_counts["product_x_purchases"]
        +
        pair_counts["product_y_purchases"]
        -
        pair_counts["co_purchase_count"]
    )
)


# --------------------------------------------------
# Product names
# --------------------------------------------------

pair_counts = pair_counts.merge(
    products,
    left_on="product_key_x",
    right_on="product_key",
    how="left",
).drop(
    columns=["product_key"]
)


pair_counts = pair_counts.rename(
    columns={
        "product_id": "product_x_id",
        "product_name": "product_x_name",
    }
)


pair_counts = pair_counts.merge(
    products,
    left_on="product_key_y",
    right_on="product_key",
    how="left",
).drop(
    columns=["product_key"]
)


pair_counts = pair_counts.rename(
    columns={
        "product_id": "product_y_id",
        "product_name": "product_y_name",
    }
)


# --------------------------------------------------
# Filter weak relationships
# --------------------------------------------------

recommendations = pair_counts[
    pair_counts["co_purchase_count"] >= 3
].copy()


recommendations["similarity"] = (
    recommendations["similarity"]
    .round(4)
)


recommendations = recommendations.sort_values(
    [
        "product_key_x",
        "similarity",
        "co_purchase_count",
    ],
    ascending=[
        True,
        False,
        False,
    ],
)


# --------------------------------------------------
# Keep top recommendations per product
# --------------------------------------------------

recommendations["recommendation_rank"] = (
    recommendations
    .groupby("product_key_x")
    .cumcount()
    + 1
)


recommendations = recommendations[
    recommendations["recommendation_rank"] <= 10
]


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


recommendations.to_csv(
    OUTPUT_PATH,
    index=False,
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n========================================")
print("RECOMMENDATION ENGINE RESULTS")
print("========================================")

print(
    f"Products with recommendations: "
    f"{recommendations['product_key_x'].nunique():,}"
)

print(
    f"Recommendation pairs: "
    f"{len(recommendations):,}"
)


print("\nTop recommendation relationships:")

print(
    recommendations[
        [
            "product_x_id",
            "product_x_name",
            "product_y_id",
            "product_y_name",
            "co_purchase_count",
            "similarity",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\nOutput saved to:")
print(OUTPUT_PATH)

print("\nRecommendation engine completed successfully.")