from pathlib import Path

import pandas as pd

INPUT_FILE = Path(
    "data/processed/online_retail_cleaned.parquet"
)

OUTPUT_FILE = Path(
    "data/processed/online_retail_features.parquet"
)


def load_data():

    print("\n1. LOADING CLEANED DATA")
    print("-" * 60)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_parquet(INPUT_FILE)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


def create_time_features(df):

    print("\n2. CREATING TIME FEATURES")
    print("-" * 60)

    # Make sure invoice_date is datetime
    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )

    # Calendar features
    df["year"] = df["invoice_date"].dt.year

    df["month"] = df["invoice_date"].dt.month

    df["day"] = df["invoice_date"].dt.day

    df["day_of_week"] = (
        df["invoice_date"].dt.dayofweek
    )

    df["hour"] = (
        df["invoice_date"].dt.hour
    )

    # Week number
    df["week_of_year"] = (
        df["invoice_date"]
        .dt.isocalendar()
        .week
        .astype("int16")
    )

    # Quarter
    df["quarter"] = (
        df["invoice_date"].dt.quarter
    )

    # Weekend flag
    df["is_weekend"] = (
        df["day_of_week"] >= 5
    )

    # Date only
    df["date"] = (
        df["invoice_date"].dt.normalize()
    )

    print("Time features created:")
    print("  - year")
    print("  - month")
    print("  - day")
    print("  - day_of_week")
    print("  - hour")
    print("  - week_of_year")
    print("  - quarter")
    print("  - is_weekend")
    print("  - date")


def create_business_features(df):

    print("\n3. CREATING BUSINESS FEATURES")
    print("-" * 60)

    # Revenue
    df["revenue"] = (
        df["quantity"] *
        df["unit_price"]
    )

    # Absolute revenue
    df["absolute_revenue"] = (
        df["revenue"].abs()
    )

    # Sales revenue
    df["sales_revenue"] = (
        df["revenue"]
        .where(
            df["transaction_type"] == "SALE",
            0
        )
    )

    # Return value
    df["return_value"] = (
        df["revenue"]
        .where(
            df["transaction_type"] == "RETURN",
            0
        )
        .abs()
    )

    # Net quantity
    df["net_quantity"] = (
        df["sales_quantity"]
        - df["return_quantity"]
    )

    # Unit price category
    df["price_band"] = pd.cut(
        df["unit_price"],
        bins=[
            -float("inf"),
            1,
            5,
            20,
            100,
            float("inf")
        ],
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High"
        ]
    )

    print("Business features created:")
    print("  - revenue")
    print("  - absolute_revenue")
    print("  - sales_revenue")
    print("  - return_value")
    print("  - net_quantity")
    print("  - price_band")


def create_customer_features(df):

    print("\n4. CREATING CUSTOMER FEATURES")
    print("-" * 60)

    # Customer transaction flag
    df["has_customer"] = (
        df["customer_id"].notna()
    )

    # Customer revenue
    df["customer_revenue"] = (
        df["revenue"]
        .where(
            df["customer_id"].notna(),
            0
        )
    )

    # Customer purchase flag
    df["customer_purchase"] = (
        (
            df["customer_id"].notna()
        )
        &
        (
            df["transaction_type"] == "SALE"
        )
    )

    print("Customer features created:")
    print("  - has_customer")
    print("  - customer_revenue")
    print("  - customer_purchase")


def optimize_data_types(df):

    print("\n5. OPTIMIZING DATA TYPES")
    print("-" * 60)

    integer_columns = [
        "year",
        "month",
        "day",
        "day_of_week",
        "hour",
        "week_of_year",
        "quarter"
    ]

    for column in integer_columns:

        df[column] = pd.to_numeric(
            df[column],
            downcast="integer"
        )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        downcast="integer"
    )

    df["sales_quantity"] = pd.to_numeric(
        df["sales_quantity"],
        downcast="integer"
    )

    df["return_quantity"] = pd.to_numeric(
        df["return_quantity"],
        downcast="integer"
    )

    print("Data types optimized.")


def save_features(df):

    print("\n6. SAVING FEATURE DATASET")
    print("-" * 60)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Feature dataset saved to:"
        f"\n{OUTPUT_FILE}"
    )

    print(
        f"File size: "
        f"{OUTPUT_FILE.stat().st_size:,} bytes"
    )


def show_summary(df):

    print("\n7. FEATURE SUMMARY")
    print("-" * 60)

    print(
        f"Rows: {len(df):,}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print("\nNew/important features:")

    features = [
        "week_of_year",
        "quarter",
        "is_weekend",
        "absolute_revenue",
        "sales_revenue",
        "return_value",
        "net_quantity",
        "price_band",
        "has_customer",
        "customer_revenue",
        "customer_purchase"
    ]

    for feature in features:

        if feature in df.columns:
            print(f"  ✓ {feature}")


def main():

    print("=" * 70)
    print("SMARTRETAIL-X FEATURE ENGINEERING PIPELINE")
    print("=" * 70)

    df = load_data()

    create_time_features(df)

    create_business_features(df)

    create_customer_features(df)

    optimize_data_types(df)

    save_features(df)

    show_summary(df)

    print("\n" + "=" * 70)
    print("PHASE 5.8 FEATURE ENGINEERING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()