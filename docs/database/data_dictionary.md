# SmartRetail-X Data Dictionary

## 1. Customers

| Column | Type | Description |
|---|---|---|
| customer_id | string | Unique customer identifier |
| customer_name | string | Customer name |
| gender | string | Customer gender |
| age | integer | Customer age |
| city | string | Customer city |
| registration_date | date | Customer registration date |

## 2. Products

| Column | Type | Description |
|---|---|---|
| product_id | string | Unique product identifier |
| product_name | string | Product name |
| category_id | string | Product category |
| category_name | string | Product category name |
| brand | string | Product brand |
| unit_cost | float | Product procurement cost |
| selling_price | float | Product selling price |

## 3. Stores

| Column | Type | Description |
|---|---|---|
| store_id | string | Unique store identifier |
| store_name | string | Store name |
| city | string | Store city |
| state | string | Store state |
| store_type | string | Store type |

## 4. Transactions

| Column | Type | Description |
|---|---|---|
| transaction_id | string | Unique transaction identifier |
| transaction_date | datetime | Date and time of transaction |
| customer_id | string | Customer making purchase |
| store_id | string | Store where purchase occurred |
| payment_method | string | Payment method |
| total_amount | float | Total transaction value |

## 5. Transaction Items

| Column | Type | Description |
|---|---|---|
| transaction_item_id | string | Unique transaction-item identifier |
| transaction_id | string | Related transaction |
| product_id | string | Purchased product |
| quantity | integer | Quantity purchased |
| unit_price | float | Selling price per unit |
| discount | float | Discount amount |
| revenue | float | Final revenue |

## 6. Inventory

| Column | Type | Description |
|---|---|---|
| inventory_id | string | Unique inventory record |
| date | date | Inventory date |
| store_id | string | Store identifier |
| product_id | string | Product identifier |
| opening_stock | integer | Stock at beginning of day |
| units_received | integer | Units received |
| units_sold | integer | Units sold |
| closing_stock | integer | Stock at end of day |
| reorder_level | integer | Reorder threshold |

## 7. Promotions

| Column | Type | Description |
|---|---|---|
| promotion_id | string | Unique promotion identifier |
| product_id | string | Product affected |
| store_id | string | Store affected |
| start_date | date | Promotion start date |
| end_date | date | Promotion end date |
| discount_percentage | float | Promotion discount |

## 8. Weather

| Column | Type | Description |
|---|---|---|
| weather_id | string | Unique weather record |
| date | date | Observation date |
| city | string | Weather location |
| temperature | float | Temperature |
| rainfall | float | Rainfall |
| humidity | float | Humidity |

## 9. Forecasts

| Column | Type | Description |
|---|---|---|
| forecast_id | string | Unique forecast |
| forecast_date | date | Date being forecast |
| product_id | string | Product |
| store_id | string | Store |
| predicted_demand | float | Forecasted demand |
| model_version | string | Model version |

## 10. Customer Segments

| Column | Type | Description |
|---|---|---|
| customer_id | string | Customer identifier |
| recency | integer | Days since last purchase |
| frequency | integer | Number of purchases |
| monetary | float | Total customer spending |
| segment | string | Assigned customer segment |

## 11. Anomalies

| Column | Type | Description |
|---|---|---|
| anomaly_id | string | Unique anomaly |
| date | date | Anomaly date |
| product_id | string | Product |
| store_id | string | Store |
| metric | string | Metric being monitored |
| value | float | Observed value |
| anomaly_score | float | Model anomaly score |
| detection_method | string | Detection algorithm |