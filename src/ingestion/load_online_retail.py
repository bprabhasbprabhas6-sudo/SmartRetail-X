from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/online_retail_II.xlsx")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "online_retail_cleaned.parquet"


def load_data():
    print("Loading Excel dataset...")

    excel_file = pd.ExcelFile(RAW_FILE)

    print("Sheets:", excel_file.sheet_names)

    dataframes = []

    for sheet in excel_file.sheet_names:
        print(f"Reading: {sheet}")

        df = pd.read_excel(
            excel_file,
            sheet_name=sheet
        )

        print(f"Rows: {len(df):,}")

        dataframes.append(df)

    combined = pd.concat(
        dataframes,
        ignore_index=True
    )

    print(f"\nTotal raw rows: {len(combined):,}")

    return combined


def clean_data(df):

    print("\nCleaning data...")

    # Rename columns
    df = df.rename(
        columns={
            "Invoice": "invoice_id",
            "StockCode": "product_id",
            "Description": "description",
            "Quantity": "quantity",
            "InvoiceDate": "invoice_date",
            "Price": "unit_price",
            "Customer ID": "customer_id",
            "Country": "country",
        }
    )

    # Remove exact duplicate rows
    duplicates = df.duplicated().sum()

    print(f"Duplicate rows found: {duplicates:,}")

    df = df.drop_duplicates().copy()

    # Convert data types
    df["invoice_id"] = df["invoice_id"].astype(str).str.strip()

    df["product_id"] = df["product_id"].astype(str).str.strip()

    df["description"] = (
        df["description"]
        .astype("string")
        .str.strip()
    )

    df["country"] = (
        df["country"]
        .astype("string")
        .str.strip()
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    df["customer_id"] = pd.to_numeric(
        df["customer_id"],
        errors="coerce"
    )

    # Identify sales and returns
    df["transaction_type"] = "SALE"

    df.loc[
        df["quantity"] < 0,
        "transaction_type"
    ] = "RETURN"

    # Price validation
    df["price_valid"] = df["unit_price"] > 0

    # Customer availability
    df["customer_available"] = (
        df["customer_id"].notna()
    )

    # Calculate revenue
    df["revenue"] = (
        df["quantity"] * df["unit_price"]
    )

    # Sales quantity
    df["sales_quantity"] = (
        df["quantity"].clip(lower=0)
    )

    # Return quantity
    df["return_quantity"] = (
        df["quantity"]
        .where(df["quantity"] < 0, 0)
        .abs()
    )

    # Date features
    df["date"] = df["invoice_date"].dt.date

    df["year"] = df["invoice_date"].dt.year

    df["month"] = df["invoice_date"].dt.month

    df["day"] = df["invoice_date"].dt.day

    df["day_of_week"] = (
        df["invoice_date"].dt.dayofweek
    )

    df["hour"] = df["invoice_date"].dt.hour

    # Remove rows missing essential fields
    before = len(df)

    df = df.dropna(
        subset=[
            "invoice_id",
            "product_id",
            "invoice_date",
            "quantity",
            "unit_price"
        ]
    ).copy()

    removed = before - len(df)

    print(
        f"Rows removed due to invalid essential fields: "
        f"{removed:,}"
    )

    # Sort data
    df = df.sort_values(
        [
            "invoice_date",
            "invoice_id",
            "product_id"
        ]
    )

    df = df.reset_index(drop=True)

    print(f"Final cleaned rows: {len(df):,}")

    return df


def save_data(df):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nCleaned dataset saved successfully!")

    print(
        f"Location: {OUTPUT_FILE}"
    )

    print(
        f"File size: "
        f"{OUTPUT_FILE.stat().st_size:,} bytes"
    )


def main():

    print("=" * 70)
    print("SMARTRETAIL-X DATA CLEANING PIPELINE")
    print("=" * 70)

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}"
        )

    df = load_data()

    df = clean_data(df)

    save_data(df)

    print("\n" + "=" * 70)
    print("DATA CLEANING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()