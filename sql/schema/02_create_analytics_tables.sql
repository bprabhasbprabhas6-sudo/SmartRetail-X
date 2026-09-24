-- ============================================================
-- SMARTRETAIL-X
-- PHASE 5.10 - ANALYTICS DATABASE SCHEMA
-- ============================================================

CREATE SCHEMA IF NOT EXISTS analytics;

-- ============================================================
-- 1. DATE DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_key        INTEGER PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,
    year            SMALLINT NOT NULL,
    quarter         SMALLINT NOT NULL,
    month           SMALLINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    day             SMALLINT NOT NULL,
    day_of_week     SMALLINT NOT NULL,
    day_name        VARCHAR(20) NOT NULL,
    week_of_year    SMALLINT NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

-- ============================================================
-- 2. PRODUCT DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.dim_product (
    product_key     BIGSERIAL PRIMARY KEY,
    product_id      VARCHAR(50) NOT NULL UNIQUE,
    product_name    TEXT,
    country         VARCHAR(100)
);

-- ============================================================
-- 3. CUSTOMER DIMENSION
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.dim_customer (
    customer_key    BIGSERIAL PRIMARY KEY,
    customer_id     VARCHAR(50) NOT NULL UNIQUE
);

-- ============================================================
-- 4. SALES FACT TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.fact_sales (
    sales_key           BIGSERIAL PRIMARY KEY,

    invoice_id          VARCHAR(50) NOT NULL,
    product_key         BIGINT REFERENCES analytics.dim_product(product_key),
    customer_key        BIGINT REFERENCES analytics.dim_customer(customer_key),
    date_key            INTEGER REFERENCES analytics.dim_date(date_key),

    invoice_date        TIMESTAMP NOT NULL,

    quantity            INTEGER NOT NULL,
    unit_price          NUMERIC(12,4),
    revenue             NUMERIC(14,2),

    transaction_type    VARCHAR(20),
    country             VARCHAR(100),

    sales_quantity      INTEGER,
    return_quantity     INTEGER,
    sales_revenue       NUMERIC(14,2),
    return_value        NUMERIC(14,2),
    net_quantity        INTEGER
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_fact_sales_invoice
ON analytics.fact_sales(invoice_id);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product
ON analytics.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
ON analytics.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date
ON analytics.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_invoice_date
ON analytics.fact_sales(invoice_date);

-- ============================================================
-- COMPLETED
-- ============================================================

SELECT 'Analytics schema created successfully' AS status;