

# SmartRetail-X Data Pipeline



## 1. Overview



SmartRetail-X implements an end-to-end data pipeline that transforms raw retail transaction data into validated, feature-rich datasets used by analytics, machine learning, forecasting, inventory optimization, customer segmentation, recommendations, and anomaly detection.



The pipeline is designed to provide:



\- Reproducible data processing

\- Data quality validation

\- Feature engineering

\- Structured storage

\- Machine learning readiness

\- Data lineage

\- Scalable processing

\- Separation of raw, processed, and analytical data



\---



## 2. Pipeline Architecture



The complete SmartRetail-X data pipeline follows this architecture:



```text

&#x20;                   UCI Online Retail II

&#x20;                           │

&#x20;                           ▼

&#x20;                   Excel Source Dataset

&#x20;                           │

&#x20;                           ▼

&#x20;                Data Ingestion Pipeline

&#x20;                           │

&#x20;                           ▼

&#x20;                   Data Cleaning

&#x20;                           │

&#x20;                           ▼

&#x20;                 Data Validation

&#x20;                           │

&#x20;                           ▼

&#x20;                Feature Engineering

&#x20;                           │

&#x20;                           ▼

&#x20;                   Parquet Dataset

&#x20;                           │

&#x20;            ┌──────────────┴──────────────┐

&#x20;            │                             │

&#x20;            ▼                             ▼

&#x20;      PostgreSQL                    ML Pipelines

&#x20;      Analytics Layer                     │

&#x20;            │                             │

&#x20;            │              ┌──────────────┼──────────────┐

&#x20;            │              │              │              │

&#x20;            ▼              ▼              ▼              ▼

&#x20;       Business        Forecasting   Segmentation   Recommendations

&#x20;       Analytics

&#x20;                                          │

&#x20;                                          ▼

&#x20;                                   Anomaly Detection

&#x20;                                          │

&#x20;                                          ▼

&#x20;                                   API / Dashboard

3\. Source Dataset



SmartRetail-X uses the UCI Online Retail II dataset.



Source:



UCI Machine Learning Repository

Online Retail II



The dataset contains approximately 1.07 million transaction records covering two years of online retail activity.



The original dataset contains:



Invoice

StockCode

Description

Quantity

InvoiceDate

Price

Customer ID

Country



The source data is provided in Excel format.



Raw file:



data/raw/online\_retail\_II.xlsx

4\. Data Ingestion



The ingestion stage loads both worksheets from the source Excel workbook.



Source sheets:



Year 2009-2010

Year 2010-2011



The ingestion pipeline combines both sheets into a single transaction dataset.



Main script:



src/ingestion/load\_online\_retail.py



Responsibilities:



Load the Excel workbook.

Read both worksheets.

Combine the datasets.

Standardize column names.

Convert data types.

Detect duplicate records.

Classify transaction types.

Calculate revenue-related fields.

Create date features.

Remove invalid records.

Save the cleaned dataset.

5\. Raw Dataset Size



The original combined dataset contains:



1,067,371 rows



The ingestion process identifies:



34,335 exact duplicate rows



These duplicates are removed during cleaning.



After processing, the cleaned dataset contains:



1,033,036 rows

6\. Data Cleaning



The cleaning stage prepares the raw transaction data for analytical and machine learning workloads.



Major cleaning operations include:



Duplicate removal

Data type conversion

Quantity validation

Price validation

Missing-value handling

Transaction classification

Revenue calculation

Date feature extraction

Essential-field validation

7\. Duplicate Removal



Exact duplicate transaction rows are identified across the combined dataset.



The pipeline removes:



34,335 duplicate rows



This prevents duplicate transactions from affecting:



Revenue calculations

Demand calculations

Customer metrics

Product statistics

Forecasting models

8\. Transaction Classification



SmartRetail-X distinguishes between sales and returns.



Transaction classification is based on transaction quantity.



Positive Quantity

&#x20;      │

&#x20;      ▼

&#x20;    SALE



Negative Quantity

&#x20;      │

&#x20;      ▼

&#x20;   RETURN



The processed dataset contains:



SALE     1,010,540

RETURN      22,496



There are no zero-quantity records in the final processed dataset.



9\. Revenue Calculation



Revenue is calculated using transaction quantity and unit price.



The pipeline creates revenue-related fields that support financial and demand analysis.



Important fields include:



revenue

sales\_quantity

return\_quantity



These fields allow the system to separately analyze:



Sales revenue

Return value

Units sold

Units returned

Net revenue

10\. Missing Data Handling



The source dataset contains missing values, particularly in customer identifiers and product descriptions.



The ingestion pipeline evaluates missing values before analytical processing.



Customer identifiers may be missing for some transactions.



The pipeline retains valid transaction records while maintaining a separate indicator for customer availability.



Field:



customer\_available



This allows customer-level analysis to distinguish identified customers from transactions without customer information.



11\. Price Validation



The pipeline validates product prices before using them in revenue calculations.



A validation indicator is created:



price\_valid



This allows downstream processes to distinguish transactions with valid and invalid prices.



Processed dataset statistics:



Valid prices:    1,027,017

Invalid prices:      6,019

12\. Processed Dataset



The cleaned transaction dataset is stored as:



data/processed/online\_retail\_cleaned.parquet



Final dataset size:



Rows: 1,033,036



Parquet is used because it provides:



Efficient storage

Column-based access

Fast analytical queries

Data type preservation

Good compatibility with pandas and PyArrow

13\. Data Validation



After cleaning, the dataset is validated before feature engineering.



Validation script:



src/ingestion/validate\_processed\_data.py



Validation checks include:



Required fields

Missing values

Quantity values

Price values

Transaction types

Revenue consistency

Duplicate records

Date ranges

Customer availability

14\. Validation Results



The validated dataset contains:



Rows: 1,033,036

Columns: 20



Required field validation:



invoice\_id missing: 0

product\_id missing: 0

invoice\_date missing: 0

quantity missing: 0

unit\_price missing: 0



Transaction validation:



SALE:   1,010,540

RETURN:    22,496



Duplicate validation:



Duplicates remaining: 0



Revenue validation:



Revenue mismatches: 0



Date range:



2009-12-01

to

2011-12-09

15\. Feature Engineering



After validation, the pipeline creates machine-learning and analytical features.



Main script:



src/features/feature\_engineering.py



The feature engineering stage creates:



Date features

Time features

Business features

Customer features

Transaction features

Optimized data types

16\. Time Features



The pipeline extracts temporal information from the transaction date.



Examples include:



year

month

day

day\_of\_week

week

quarter

hour

is\_weekend



These features support:



Seasonal analysis

Demand forecasting

Sales trend analysis

Business intelligence

Time-based anomaly detection

17\. Business Features



Business-level features are generated from transaction information.



Important features include:



revenue

sales\_quantity

return\_quantity

transaction\_type

price\_valid

customer\_available



These fields provide a foundation for downstream analytical workflows.



18\. Feature Dataset



The final feature dataset is stored as:



data/processed/online\_retail\_features.parquet



Dataset size:



Rows: 1,033,036

Columns: 31



The feature dataset is the primary input for:



PostgreSQL loading

Demand forecasting

Customer segmentation

Recommendation generation

Anomaly detection

Inventory analysis

19\. PostgreSQL Loading



The feature dataset is loaded into PostgreSQL for structured analytical storage.



Database:



smartretail\_x



Loader:



scripts/load\_features\_to\_postgres.py



Destination staging table:



staging.online\_retail\_transactions



Rows loaded:



1,033,036

20\. PostgreSQL Transformation



The staging data is transformed into an analytical dimensional model.



The analytics layer contains:



analytics.dim\_date

analytics.dim\_product

analytics.dim\_customer

analytics.fact\_sales



The central fact table contains transaction-level sales records.



21\. Analytics Data Model



The data flow into the analytical database is:



Feature Dataset

&#x20;     │

&#x20;     ▼

PostgreSQL Staging

&#x20;     │

&#x20;     ▼

┌───────────────────────────┐

│      Analytics Layer      │

├───────────────────────────┤

│ dim\_date                  │

│ dim\_product               │

│ dim\_customer              │

│ fact\_sales                │

└───────────────────────────┘



Current table sizes:



dim\_date       761

dim\_product    5,304

dim\_customer   5,942

fact\_sales     1,033,036

22\. Machine Learning Data Flow



The processed data is used by multiple machine learning pipelines.



&#x20;                Feature Dataset

&#x20;                      │

&#x20;       ┌──────────────┼──────────────┐

&#x20;       │              │              │

&#x20;       ▼              ▼              ▼

&#x20;  Forecasting    Segmentation   Recommendations

&#x20;       │              │              │

&#x20;       ▼              ▼              ▼

&#x20;  Demand Model     RFM Model     Product Pairs

&#x20;       │

&#x20;       ▼

&#x20;Inventory Optimization

&#x20;       │

&#x20;       ▼

&#x20;  Business Actions

23\. Demand Forecasting Pipeline



Demand forecasting uses historical product demand.



The forecasting pipeline includes:



Transaction Data

&#x20;      │

&#x20;      ▼

Daily Product Demand

&#x20;      │

&#x20;      ▼

Lag Features

&#x20;      │

&#x20;      ▼

Rolling Features

&#x20;      │

&#x20;      ▼

Train/Test Split

&#x20;      │

&#x20;      ▼

XGBoost Model

&#x20;      │

&#x20;      ▼

7-Day Forecast



Main forecasting components are stored under:



src/forecasting/

24\. Forecasting Features



The forecasting pipeline creates historical demand features including:



lag\_1

lag\_7

lag\_14

lag\_28

rolling\_mean\_7

rolling\_mean\_14

rolling\_mean\_28

rolling\_std\_7

rolling\_max\_7



Calendar features are also used to capture time-related patterns.



25\. Customer Segmentation Pipeline



Customer transaction history is transformed into RFM features.



The pipeline calculates:



Recency

Frequency

Monetary



These values are used to classify customers into behavioral segments.



Output:



data/processed/customer\_segments.csv



The segmentation results can support:



Customer retention

Marketing campaigns

Customer prioritization

Business analysis

26\. Recommendation Pipeline



The recommendation engine analyzes product co-purchase relationships.



Pipeline:



Transactions

&#x20;    │

&#x20;    ▼

Customer Purchase History

&#x20;    │

&#x20;    ▼

Product Pair Analysis

&#x20;    │

&#x20;    ▼

Co-Purchase Relationships

&#x20;    │

&#x20;    ▼

Product Recommendations



Output:



data/processed/product\_recommendations.csv

27\. Anomaly Detection Pipeline



The anomaly detection system analyzes sales behavior to identify unusual activity.



Pipeline:



Historical Sales

&#x20;      │

&#x20;      ▼

Sales Patterns

&#x20;      │

&#x20;      ▼

Anomaly Detection

&#x20;      │

&#x20;      ▼

Anomaly Records



Output:



data/processed/sales\_anomalies.csv

28\. Inventory Optimization Pipeline



Inventory optimization uses historical demand statistics to calculate inventory recommendations.



The workflow includes:



Historical Demand

&#x20;      │

&#x20;      ▼

Average Daily Demand

&#x20;      │

&#x20;      ▼

Demand Variability

&#x20;      │

&#x20;      ▼

Safety Stock

&#x20;      │

&#x20;      ▼

Reorder Point

&#x20;      │

&#x20;      ▼

Recommended Order Quantity



Output:



data/processed/inventory\_recommendations.csv



Because actual on-hand inventory is not available in the source dataset, the recommendation system uses calculated demand-based targets rather than real-time warehouse stock.



29\. Explainable AI Pipeline



The forecasting model is supported by SHAP-based explainability.



Pipeline:



Trained XGBoost Model

&#x20;       │

&#x20;       ▼

SHAP Analysis

&#x20;       │

&#x20;       ▼

Feature Importance

&#x20;       │

&#x20;       ▼

Explainability Output



Output:



data/processed/explainability/shap\_feature\_importance.csv



The current implementation provides global mean absolute SHAP feature importance.



30\. MLflow Integration



The machine learning pipeline integrates MLflow for experiment tracking.



MLflow records:



Model parameters

Training configuration

Evaluation metrics

Training dataset information

Model artifacts

Experiment runs



Tracking database:



mlflow.db



Experiment:



SmartRetail-X Demand Forecasting



This provides reproducibility and model lifecycle support.



31\. API Integration



Processed analytical and machine learning outputs are exposed through FastAPI.



Main API endpoints include:



/api/v1/forecast

/api/v1/inventory/recommendation

/api/v1/customer/segment

/api/v1/recommendations/

/api/v1/anomalies/product

/api/v1/explainability/feature-importance



The API provides a programmatic interface between machine learning services and the application layer.



32\. Dashboard Integration



The Streamlit dashboard consumes processed analytics and machine learning outputs.



The dashboard can present:



Retail KPIs

Sales trends

Demand forecasts

Inventory recommendations

Customer segments

Product recommendations

Sales anomalies

Model explainability



This converts the data pipeline outputs into business-facing insights.



33\. Data Lineage



The complete data lineage is:



UCI Online Retail II

&#x20;       │

&#x20;       ▼

online\_retail\_II.xlsx

&#x20;       │

&#x20;       ▼

load\_online\_retail.py

&#x20;       │

&#x20;       ▼

Data Cleaning

&#x20;       │

&#x20;       ▼

validate\_processed\_data.py

&#x20;       │

&#x20;       ▼

online\_retail\_cleaned.parquet

&#x20;       │

&#x20;       ▼

feature\_engineering.py

&#x20;       │

&#x20;       ▼

online\_retail\_features.parquet

&#x20;       │

&#x20;       ├──────────────────────┐

&#x20;       ▼                      ▼

PostgreSQL                ML Pipelines

&#x20;       │                      │

&#x20;       ▼              ┌───────┼────────┐

Analytics             ▼       ▼        ▼

Tables             Forecast  RFM   Recommendations

&#x20;                       │

&#x20;                       ▼

&#x20;                 Inventory / Anomaly

&#x20;                       │

&#x20;                       ▼

&#x20;                  FastAPI / Streamlit

34\. Reproducibility



The pipeline is designed so that data processing can be reproduced from the source dataset.



Important components are version-controlled:



src/

scripts/

sql/

configs/

tests/

docs/



Generated datasets and sensitive configuration files are excluded from Git where appropriate.



Examples:



data/raw/*

data/processed/*

.env

logs/*

models/*.pkl

models/*.joblib

mlflow.db

35\. Data Quality Controls



The pipeline implements multiple data quality controls.



These include:



Duplicate detection

Required-field validation

Quantity validation

Price validation

Revenue validation

Transaction classification validation

Date validation

Feature consistency checks

Database row-count validation

Automated tests



The validation layer prevents invalid data from silently propagating into downstream machine learning workflows.



36\. Error Handling



Pipeline stages are designed to fail clearly when critical data assumptions are violated.



Examples include:



Missing required columns

Invalid data types

Missing essential fields

Invalid transaction types

Revenue calculation mismatches

Missing forecasting features

Database connection failures



This improves reliability and simplifies debugging.



37\. Scalability



The current pipeline processes more than one million transaction records.



The architecture can be extended through:



Incremental data ingestion

Batch processing

Database indexing

PostgreSQL partitioning

Parallel processing

Cloud object storage

Scheduled pipelines

Containerized execution

Workflow orchestration



Potential future orchestration technologies include:



Apache Airflow

Prefect

Dagster

38\. Pipeline Monitoring



Pipeline and API activity can be monitored using the SmartRetail-X logging system.



Logging configuration:



configs/logging\_config.py



Log output:



logs/smartretail.log



The API logs:



HTTP method

Request path

Response status

Request duration

Failed requests



This provides operational visibility into the application layer.



39\. Testing



The data pipeline and application are supported by automated testing.



The project currently includes:



tests/

├── unit/

├── integration/

├── api/

└── fixtures/



The project test suite currently contains:



38 tests



All tests pass in the validated local environment.



40\. CI/CD Integration



The data and application code are validated through GitHub Actions.



The CI pipeline performs:



Checkout Code

&#x20;     │

&#x20;     ▼

Setup Python

&#x20;     │

&#x20;     ▼

Install Dependencies

&#x20;     │

&#x20;     ▼

Create Test Fixtures

&#x20;     │

&#x20;     ▼

Ruff

&#x20;     │

&#x20;     ▼

MyPy

&#x20;     │

&#x20;     ▼

Pytest



This helps prevent broken code from being merged into the main branch.



41\. End-to-End Pipeline Summary



The complete SmartRetail-X pipeline can be summarized as:



SOURCE

&#x20; │

&#x20; ▼

UCI Online Retail II

&#x20; │

&#x20; ▼

INGESTION

&#x20; │

&#x20; ▼

Cleaning + Type Conversion

&#x20; │

&#x20; ▼

VALIDATION

&#x20; │

&#x20; ▼

Validated Transactions

&#x20; │

&#x20; ▼

FEATURE ENGINEERING

&#x20; │

&#x20; ▼

Feature Dataset

&#x20; │

&#x20; ├───────────────┐

&#x20; ▼               ▼

PostgreSQL        ML Pipelines

&#x20; │               │

&#x20; ▼               ├── Forecasting

Analytics         ├── Segmentation

&#x20; │               ├── Recommendations

&#x20; │               ├── Anomaly Detection

&#x20; │               └── Inventory Optimization

&#x20; │

&#x20; └───────────────┬───────────────┘

&#x20;                 ▼

&#x20;            FastAPI Services

&#x20;                 │

&#x20;                 ▼

&#x20;           Streamlit Dashboard

&#x20;                 │

&#x20;                 ▼

&#x20;            Business Insights

42\. Pipeline Design Goals



The SmartRetail-X data pipeline is designed to provide:



Reliability

Reproducibility

Data quality

Traceability

Scalability

Maintainability

Machine learning readiness

Analytical flexibility

API integration

Dashboard integration

Automated validation



The architecture provides a complete path from raw retail transactions to production-oriented business intelligence and machine learning services.





### After pasting



Save the file with:



**Ctrl + S**



Then close Notepad.



**Do not run Git commands yet.**



When you've saved and closed Notepad, reply:



**`saved`**



Then we'll verify the file before committing it.


