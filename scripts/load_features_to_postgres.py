from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "online_retail_features.parquet"
)

ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL was not found in .env file."
    )


# ============================================================
# 3. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# 4. EXPECTED SOURCE COLUMNS
# ============================================================

EXPECTED_SOURCE_COLUMNS = [
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

    "year",
    "month",
    "day",
    "day_of_week",
    "hour",
    "week_of_year",
    "quarter",
    "is_weekend",

    "date",

    "absolute_revenue",
    "sales_revenue",
    "return_value",
    "net_quantity",

    "price_band",

    "has_customer",
    "customer_revenue",
    "customer_purchase",
]


# ============================================================
# 5. DATABASE COLUMN NAMES
# ============================================================

DATABASE_COLUMNS = [
    "invoice_id",
    "stock_code",
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

    "year",
    "month",
    "day",
    "day_of_week",
    "hour",
    "week_of_year",
    "quarter",
    "is_weekend",

    "date",

    "absolute_revenue",
    "sales_revenue",
    "return_value",
    "net_quantity",

    "price_band",

    "has_customer",
    "customer_revenue",
    "customer_purchase",
]


# ============================================================
# 6. BOOLEAN COLUMNS
# ============================================================

BOOLEAN_COLUMNS = [
    "price_valid",
    "customer_available",
    "is_weekend",
    "has_customer",
    "customer_purchase",
]


# ============================================================
# 7. NUMERIC COLUMNS
# ============================================================

INTEGER_COLUMNS = [
    "quantity",
    "sales_quantity",
    "return_quantity",
    "year",
    "month",
    "day",
    "day_of_week",
    "hour",
    "week_of_year",
    "quarter",
    "net_quantity",
]

FLOAT_COLUMNS = [
    "unit_price",
    "revenue",
    "absolute_revenue",
    "sales_revenue",
    "return_value",
    "customer_revenue",
]


# ============================================================
# 8. LOAD PARQUET DATA
# ============================================================

def load_data():
    print("=" * 70)
    print("SMARTRETAIL-X - LOAD FEATURES INTO POSTGRESQL")
    print("=" * 70)

    print(f"\nProject root:")
    print(PROJECT_ROOT)

    print(f"\nInput file:")
    print(DATA_FILE)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Processed feature file not found:\n{DATA_FILE}"
        )

    print("\nLoading Parquet file...")

    df = pd.read_parquet(DATA_FILE)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")


    # ========================================================
    # 9. CHECK SOURCE COLUMNS
    # ========================================================

    missing_columns = [
        column
        for column in EXPECTED_SOURCE_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"\nMissing columns in feature file:\n{missing_columns}"
        )

    print("\nAll required source columns found.")


    # ========================================================
    # 10. SELECT ONLY REQUIRED COLUMNS
    # ========================================================

    df = df[EXPECTED_SOURCE_COLUMNS].copy()


    # ========================================================
    # 11. RENAME product_id → stock_code
    # ========================================================

    df = df.rename(
        columns={
            "product_id": "stock_code"
        }
    )

    print("Mapped product_id → stock_code")


    # ========================================================
    # 12. CLEAN STRING COLUMNS
    # ========================================================

    string_columns = [
        "invoice_id",
        "stock_code",
        "description",
        "customer_id",
        "country",
        "transaction_type",
        "price_band",
    ]

    for column in string_columns:
        df[column] = df[column].astype("object")

        df[column] = df[column].where(
            df[column].notna(),
            None
        )


    # ========================================================
    # 13. CONVERT INTEGER COLUMNS
    # ========================================================

    for column in INTEGER_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        # PostgreSQL INTEGER requires whole numbers.
        df[column] = df[column].round()

        df[column] = df[column].astype("Int64")


    # ========================================================
    # 14. CONVERT FLOAT / NUMERIC COLUMNS
    # ========================================================

    for column in FLOAT_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    # ========================================================
    # 15. CONVERT BOOLEAN COLUMNS
    # ========================================================

    for column in BOOLEAN_COLUMNS:

        df[column] = df[column].astype("boolean")


    # ========================================================
    # 16. CONVERT DATETIME COLUMN
    # ========================================================

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )


    # ========================================================
    # 17. CONVERT DATE COLUMN
    # ========================================================

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).dt.date


    # ========================================================
    # 18. CHECK INVALID DATES
    # ========================================================

    invalid_invoice_dates = df["invoice_date"].isna().sum()
    invalid_dates = df["date"].isna().sum()

    print(
        f"\nInvalid invoice dates: "
        f"{invalid_invoice_dates:,}"
    )

    print(
        f"Invalid dates: "
        f"{invalid_dates:,}"
    )


    # ========================================================
    # 19. CONVERT NaN / NA TO None
    # ========================================================

    df = df.astype(object)

    df = df.where(
        pd.notna(df),
        None
    )


    # ========================================================
    # 20. FINAL COLUMN ORDER
    # ========================================================

    df = df[DATABASE_COLUMNS]


    # ========================================================
    # 21. DISPLAY DATA INFORMATION
    # ========================================================

    print("\nFinal columns:")
    print(list(df.columns))

    print(
        f"\nFinal rows ready for PostgreSQL: "
        f"{len(df):,}"
    )


    # ========================================================
    # 22. DATABASE TEST
    # ========================================================

    print("\nTesting PostgreSQL connection...")

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database();")
        )

        database_name = result.scalar()

        print(
            f"Connected database: "
            f"{database_name}"
        )


    # ========================================================
    # 23. LOAD DATA
    # ========================================================

    print(
        "\nLoading data into "
        "staging.online_retail_transactions..."
    )

    df.to_sql(
        name="online_retail_transactions",
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        chunksize=5000,
        method=None,
    )


    # ========================================================
    # 24. VERIFY INSERTED ROWS
    # ========================================================

    with engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM staging.online_retail_transactions;
                """
            )
        )

        total_rows = result.scalar()


    # ========================================================
    # 25. FINAL RESULT
    # ========================================================

    print("\n" + "=" * 70)
    print("DATA LOAD COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"\nRows loaded into PostgreSQL: "
        f"{total_rows:,}"
    )

    print(
        "\nTable:"
        "\nstaging.online_retail_transactions"
    )

    print("\nSmartRetail-X Phase 5.9/5.10 data loading completed.")


# ============================================================
# 26. MAIN
# ============================================================

if __name__ == "__main__":

    try:
        load_data()

    except Exception as error:

        print("\n" + "=" * 70)
        print("DATA LOAD FAILED")
        print("=" * 70)

        print(
            f"\nError type: "
            f"{type(error).__name__}"
        )

        print(
            f"\nError message:\n"
            f"{error}"
        )

        raise