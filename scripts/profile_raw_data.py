from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/online_retail_II.xlsx")


def profile_sheet(excel_file: pd.ExcelFile, sheet_name: str) -> None:
    print("\n" + "=" * 80)
    print(f"SHEET: {sheet_name}")
    print("=" * 80)

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    missing_table = pd.DataFrame(
        {
            "Missing": missing,
            "Missing %": missing_pct,
        }
    )

    print(missing_table[missing_table["Missing"] > 0])

    print("\nDuplicate rows:")
    print(f"  {df.duplicated().sum():,}")

    print("\nDate range:")
    dates = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    print(f"  Min: {dates.min()}")
    print(f"  Max: {dates.max()}")

    print("\nNumeric summary:")
    print(df[["Quantity", "Price"]].describe())

    print("\nUnique values:")
    print(f"  Invoices:      {df['Invoice'].nunique():,}")
    print(f"  Stock codes:   {df['StockCode'].nunique():,}")
    print(f"  Customers:     {df['Customer ID'].nunique():,}")
    print(f"  Countries:     {df['Country'].nunique():,}")

    print("\nQuantity checks:")
    print(f"  Quantity <= 0: {(df['Quantity'] <= 0).sum():,}")
    print(f"  Quantity < 0:  {(df['Quantity'] < 0).sum():,}")
    print(f"  Quantity == 0: {(df['Quantity'] == 0).sum():,}")

    print("\nPrice checks:")
    print(f"  Price <= 0: {(df['Price'] <= 0).sum():,}")
    print(f"  Price < 0:  {(df['Price'] < 0).sum():,}")
    print(f"  Price == 0: {(df['Price'] == 0).sum():,}")

    print("\nSample records:")
    print(df.head(3).to_string(index=False))


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}"
        )

    print("=" * 80)
    print("SMARTRETAIL-X RAW DATA PROFILING")
    print("=" * 80)
    print(f"File: {RAW_FILE}")
    print(f"File size: {RAW_FILE.stat().st_size:,} bytes")

    excel_file = pd.ExcelFile(RAW_FILE)

    print(f"\nSheets found: {excel_file.sheet_names}")

    for sheet_name in excel_file.sheet_names:
        profile_sheet(excel_file, sheet_name)

    print("\n" + "=" * 80)
    print("PROFILING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()