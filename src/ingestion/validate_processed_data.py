from pathlib import Path

import pandas as pd

PROCESSED_FILE = Path(
    "data/processed/online_retail_cleaned.parquet"
)


def validate_file_exists():

    print("\n1. FILE CHECK")
    print("-" * 60)

    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"Processed file not found: {PROCESSED_FILE}"
        )

    print("Processed file exists: YES")


def load_data():

    print("\n2. DATA LOADING")
    print("-" * 60)

    df = pd.read_parquet(PROCESSED_FILE)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df


def validate_columns(df):

    print("\n3. COLUMN CHECK")
    print("-" * 60)

    required_columns = [
        "invoice_id",
        "product_id",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "customer_id",
        "country",
        "transaction_type",
        "price_valid",
        "customer_available",
        "revenue",
        "sales_quantity",
        "return_quantity",
        "date",
        "year",
        "month",
        "day",
        "day_of_week",
        "hour",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print("Missing columns:")

        for column in missing_columns:
            print(f"  - {column}")

        raise ValueError(
            "Required columns are missing."
        )

    print("All required columns exist: YES")


def validate_missing_values(df):

    print("\n4. MISSING VALUE CHECK")
    print("-" * 60)

    important_columns = [
        "invoice_id",
        "product_id",
        "invoice_date",
        "quantity",
        "unit_price",
    ]

    problems_found = False

    for column in important_columns:

        missing = df[column].isna().sum()

        print(
            f"{column}: {missing:,} missing"
        )

        if missing > 0:
            problems_found = True

    if not problems_found:
        print(
            "\nEssential columns contain no missing values: YES"
        )


def validate_quantity(df):

    print("\n5. QUANTITY CHECK")
    print("-" * 60)

    negative_quantity = (
        df["quantity"] < 0
    ).sum()

    positive_quantity = (
        df["quantity"] > 0
    ).sum()

    zero_quantity = (
        df["quantity"] == 0
    ).sum()

    print(
        f"Positive quantity: {positive_quantity:,}"
    )

    print(
        f"Negative quantity: {negative_quantity:,}"
    )

    print(
        f"Zero quantity: {zero_quantity:,}"
    )

    print(
        "\nNegative quantities are retained as RETURN records."
    )


def validate_price(df):

    print("\n6. PRICE CHECK")
    print("-" * 60)

    invalid_price = (
        df["unit_price"] <= 0
    ).sum()

    valid_price = (
        df["unit_price"] > 0
    ).sum()

    print(
        f"Valid prices: {valid_price:,}"
    )

    print(
        f"Invalid prices: {invalid_price:,}"
    )

    print(
        "\nInvalid prices are flagged using price_valid."
    )


def validate_transaction_type(df):

    print("\n7. TRANSACTION TYPE CHECK")
    print("-" * 60)

    print(
        df["transaction_type"].value_counts()
    )

    invalid_types = ~df[
        "transaction_type"
    ].isin(
        ["SALE", "RETURN"]
    )

    invalid_count = invalid_types.sum()

    print(
        f"\nInvalid transaction types: {invalid_count:,}"
    )


def validate_revenue(df):

    print("\n8. REVENUE CHECK")
    print("-" * 60)

    calculated_revenue = (
        df["quantity"] * df["unit_price"]
    )

    revenue_matches = (
        calculated_revenue.round(6)
        == df["revenue"].round(6)
    )

    mismatches = (
        ~revenue_matches
    ).sum()

    print(
        f"Revenue mismatches: {mismatches:,}"
    )

    if mismatches == 0:
        print(
            "Revenue calculation is correct: YES"
        )


def validate_duplicates(df):

    print("\n9. DUPLICATE CHECK")
    print("-" * 60)

    duplicates = df.duplicated().sum()

    print(
        f"Duplicate rows remaining: {duplicates:,}"
    )

    if duplicates == 0:
        print(
            "No exact duplicate rows remain: YES"
        )


def validate_dates(df):

    print("\n10. DATE CHECK")
    print("-" * 60)

    min_date = df["invoice_date"].min()
    max_date = df["invoice_date"].max()

    print(f"Minimum date: {min_date}")
    print(f"Maximum date: {max_date}")

    invalid_dates = (
        df["invoice_date"].isna()
    ).sum()

    print(
        f"Invalid dates: {invalid_dates:,}"
    )


def final_summary(df):

    print("\n" + "=" * 70)
    print("PHASE 5.7 VALIDATION SUMMARY")
    print("=" * 70)

    print(
        f"Final rows: {len(df):,}"
    )

    print(
        f"Final columns: {len(df.columns)}"
    )

    print(
        f"Sales records: "
        f"{(df['transaction_type'] == 'SALE').sum():,}"
    )

    print(
        f"Return records: "
        f"{(df['transaction_type'] == 'RETURN').sum():,}"
    )

    print(
        f"Customer IDs available: "
        f"{df['customer_id'].notna().sum():,}"
    )

    print(
        f"Customer IDs missing: "
        f"{df['customer_id'].isna().sum():,}"
    )

    print("\nDATA VALIDATION COMPLETED SUCCESSFULLY")


def main():

    print("=" * 70)
    print("SMARTRETAIL-X DATA VALIDATION PIPELINE")
    print("=" * 70)

    validate_file_exists()

    df = load_data()

    validate_columns(df)

    validate_missing_values(df)

    validate_quantity(df)

    validate_price(df)

    validate_transaction_type(df)

    validate_revenue(df)

    validate_duplicates(df)

    validate_dates(df)

    final_summary(df)

    print("=" * 70)


if __name__ == "__main__":
    main()