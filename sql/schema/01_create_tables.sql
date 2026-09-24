-- ============================================================
-- SmartRetail-X
-- Database Schema
-- Phase 5.10
-- ============================================================

-- ============================================================
-- STAGING: Online Retail Transactions
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.online_retail_transactions (
    invoice_id              VARCHAR(50),
    stock_code              VARCHAR(50),
    description             TEXT,
    quantity                INTEGER,
    invoice_date            TIMESTAMP,
    unit_price              NUMERIC(12, 4),
    customer_id             VARCHAR(50),
    country                 VARCHAR(100),

    transaction_type        VARCHAR(20),
    price_valid             BOOLEAN,
    customer_available      BOOLEAN,

    revenue                 NUMERIC(14, 2),
    sales_quantity          INTEGER,
    return_quantity         INTEGER,

    year                    SMALLINT,
    month                   SMALLINT,
    day                     SMALLINT,
    day_of_week             SMALLINT,
    hour                    SMALLINT,
    week_of_year            SMALLINT,
    quarter                 SMALLINT,
    is_weekend              BOOLEAN,

    date                    DATE,

    absolute_revenue        NUMERIC(14, 2),
    sales_revenue           NUMERIC(14, 2),
    return_value            NUMERIC(14, 2),
    net_quantity            INTEGER,

    price_band              VARCHAR(30),

    has_customer            BOOLEAN,
    customer_revenue        NUMERIC(14, 2),
    customer_purchase       INTEGER
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_retail_invoice
    ON staging.online_retail_transactions(invoice_id);

CREATE INDEX IF NOT EXISTS idx_retail_customer
    ON staging.online_retail_transactions(customer_id);

CREATE INDEX IF NOT EXISTS idx_retail_product
    ON staging.online_retail_transactions(stock_code);

CREATE INDEX IF NOT EXISTS idx_retail_date
    ON staging.online_retail_transactions(invoice_date);

CREATE INDEX IF NOT EXISTS idx_retail_country
    ON staging.online_retail_transactions(country);