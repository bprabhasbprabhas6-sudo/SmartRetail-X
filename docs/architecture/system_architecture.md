# SmartRetail-X System Architecture



## 1. Project Overview



SmartRetail-X is an industry-oriented retail intelligence platform designed to support demand forecasting, inventory optimization, customer segmentation, product recommendations, anomaly detection, and explainable machine learning.



The platform combines data engineering, analytics, machine learning, APIs, visualization, database management, experiment tracking, automated testing, CI/CD, containerization, and application monitoring.



\---



## 2. High-Level Architecture



```text

&#x20;                   ┌──────────────────────────┐

&#x20;                   │   UCI Online Retail II   │

&#x20;                   │      Raw Dataset         │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │     Data Ingestion        │

&#x20;                   │ Excel → Pandas → Parquet  │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │ Data Cleaning \& Validation │

&#x20;                   │ Duplicates / Types /      │

&#x20;                   │ Returns / Revenue         │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │    Feature Engineering    │

&#x20;                   │ Time / Customer / Product │

&#x20;                   │ Business Features         │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │      PostgreSQL           │

&#x20;                   │ Raw / Staging / Analytics │

&#x20;                   │ ML schemas                │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;            ┌───────────────────┼───────────────────┐

&#x20;            │                   │                   │

&#x20;            ▼                   ▼                   ▼

&#x20;     ┌─────────────┐    ┌──────────────┐    ┌──────────────┐

&#x20;     │ Forecasting │    │ Segmentation │    │ Inventory    │

&#x20;     │ XGBoost     │    │ RFM          │    │ Optimization │

&#x20;     └──────┬──────┘    └──────┬───────┘    └──────┬───────┘

&#x20;            │                   │                   │

&#x20;            └───────────────────┼───────────────────┘

&#x20;                                │

&#x20;            ┌───────────────────┼───────────────────┐

&#x20;            │                   │                   │

&#x20;            ▼                   ▼                   ▼

&#x20;     ┌─────────────┐    ┌──────────────┐    ┌──────────────┐

&#x20;     │Recommender  │    │   Anomaly    │    │ Explainable  │

&#x20;     │   Engine    │    │  Detection   │    │     AI       │

&#x20;     └──────┬──────┘    └──────┬───────┘    └──────┬───────┘

&#x20;            │                   │                   │

&#x20;            └───────────────────┼───────────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │       FastAPI API        │

&#x20;                   │   REST Prediction Layer  │

&#x20;                   └────────────┬─────────────┘

&#x20;                                │

&#x20;                                ▼

&#x20;                   ┌──────────────────────────┐

&#x20;                   │   Streamlit Dashboard    │

&#x20;                   │ Analytics \& Visualization│

&#x20;                   └──────────────────────────┘





Supporting Services

────────────────────────────────────────────────────────────

&#x20;MLflow       → Experiment and model tracking

&#x20;Logging      → API/application monitoring

&#x20;Pytest       → Automated testing

&#x20;Ruff/MyPy    → Code quality and static analysis

&#x20;GitHub CI    → Continuous integration

&#x20;Docker       → Containerization

```



\---



## 3. Data Layer



### Raw Data



The primary dataset is the UCI Online Retail II dataset.



The original data is stored under:



```text

data/raw/

```



Raw files are excluded from Git because of their size.



### Processed Data



Cleaned and feature-engineered datasets are stored under:



```text

data/processed/

```



Parquet is used for efficient analytical storage.



\---



## 4. Data Ingestion Pipeline



The ingestion pipeline performs the following operations:



1\. Loads both Excel sheets.

2\. Combines the datasets.

3\. Standardizes column names.

4\. Converts data types.

5\. Removes exact duplicate transactions.

6\. Identifies sales and returns.

7\. Calculates revenue.

8\. Creates transaction-level business flags.

9\. Handles missing essential values.

10\. Generates date-related features.

11\. Saves the cleaned dataset as Parquet.



Main module:



```text

src/ingestion/load\_online\_retail.py

```



Output:



```text

data/processed/online\_retail\_cleaned.parquet

```



\---



## 5. Data Validation



The validation pipeline checks:



* Missing required fields

* Duplicate transactions

* Invalid quantities

* Invalid prices

* Transaction types

* Revenue calculations

* Date ranges

* Customer availability



Main module:



```text

src/ingestion/validate\_processed\_data.py

```



\---



## 6. Feature Engineering



Feature engineering creates features required for analytics and machine learning.



Examples include:



* Year

* Month

* Day

* Day of week

* Weekend indicator

* Customer-level features

* Product-level features

* Revenue features

* Quantity features

* Purchase indicators



Main module:



```text

src/features/feature\_engineering.py

```



\---



## 7. Database Architecture



PostgreSQL is used as the primary analytical database.



Database:



```text

smartretail\_x

```



Main schemas:



```text

raw

staging

analytics

ml

```



The analytics layer contains:



```text

analytics.dim\_date

analytics.dim\_product

analytics.dim\_customer

analytics.fact\_sales

```



The fact table stores transaction-level sales information while dimension tables provide reusable analytical attributes.



\---



## 8. Machine Learning Layer



### Demand Forecasting



The forecasting pipeline uses XGBoost to predict daily product demand.



Features include:



* Lag 1

* Lag 7

* Lag 14

* Lag 28

* Rolling mean 7

* Rolling mean 14

* Rolling mean 28

* Rolling standard deviation

* Rolling maximum

* Month

* Day of week

* Weekend indicator



A log-transformed target using `log1p` is used for the current forecasting model.



Model artifact:



```text

models/xgboost\_demand\_forecast\_log.json

```



\---



## 9. Inventory Optimization



The inventory module calculates inventory planning metrics including:



* Average daily demand

* Demand variability

* Safety stock

* Reorder point

* Target inventory

* Recommended order quantity

* Inventory priority



Main module:



```text

src/inventory/inventory\_optimizer.py

```



\---



## 10. Customer Segmentation



Customer segmentation uses RFM analysis.



The three core dimensions are:



```text

R = Recency

F = Frequency

M = Monetary Value

```



Customers are assigned RFM scores and business segments.



Output:



```text

data/processed/customer\_segments.csv

```



\---



## 11. Recommendation Engine



The recommendation engine identifies related products using product co-purchase behavior and similarity.



Output:



```text

data/processed/product\_recommendations.csv

```



\---



## 12. Anomaly Detection



The anomaly detection module identifies unusual product demand behavior using statistical deviation from rolling demand patterns.



Output:



```text

data/processed/sales\_anomalies.csv

```



\---



## 13. Explainable AI



SHAP is used to explain the demand forecasting model.



The current implementation provides global feature importance using mean absolute SHAP values.



Output:



```text

data/processed/explainability/shap\_feature\_importance.csv

```



Important interpretation rule:



> Mean absolute SHAP values indicate the magnitude of feature contribution to the model output, but do not by themselves indicate whether a feature increases or decreases the prediction.



\---



## 14. API Layer



FastAPI exposes machine learning and analytics functionality through REST endpoints.



Current API modules include:



```text

/api/v1/forecast

/api/v1/inventory/recommendation

/api/v1/customer/segment

/api/v1/recommendations/

/api/v1/anomalies/product

/api/v1/explainability/feature-importance

```



Health endpoint:



```text

/health

```



API entry point:



```text

app/api/main.py

```



\---



## 15. Monitoring and Logging



SmartRetail-X includes centralized application logging.



Logging configuration:



```text

configs/logging\_config.py

```



Log output:



```text

logs/smartretail.log

```



The FastAPI middleware records:



* HTTP method

* Request path

* Response status code

* Request duration

* Exceptions



Example:



```text

Request started | method=GET | path=/health

Request completed | method=GET | path=/health | status=200 | duration\_ms=2.88

```



Log files use rotation to prevent uncontrolled log growth.



\---



## 16. MLflow Model Management



MLflow is used to track demand forecasting experiments.



Tracked information includes:



* Model parameters

* Training rows

* Testing rows

* Feature count

* MAE

* RMSE

* WMAPE

* Target transformation

* XGBoost model artifact



The local MLflow tracking database is:



```text

mlflow.db

```



It is intentionally excluded from Git.



\---



## 17. Testing Architecture



The project uses automated tests with Pytest.



Test categories include:



```text

tests/

├── unit/

├── integration/

├── api/

└── fixtures/

```



Production data is not required for CI API tests. Test fixtures are generated automatically.



Current test suite:



```text

38 tests passing

```



\---



## 18. Code Quality



The project uses:



### Ruff



For:



* Code style

* Import organization

* Static linting



### MyPy



For:



* Static type checking



Both checks are executed during development and CI.



\---



## 19. CI/CD



GitHub Actions automatically runs:



```text

Checkout

&#x20;  ↓

Python 3.13

&#x20;  ↓

Install dependencies

&#x20;  ↓

Create test fixtures

&#x20;  ↓

Ruff

&#x20;  ↓

MyPy

&#x20;  ↓

Pytest

```



The workflow is located at:



```text

.github/workflows/tests.yml

```



\---



## 20. Containerization



Docker is used to provide a reproducible runtime environment.



The Docker configuration is maintained under:



```text

docker/

```



This allows the API and application environment to be packaged consistently for deployment.



\---



## 21. End-to-End Data Flow



```text

Raw Retail Transactions

&#x20;         │

&#x20;         ▼

&#x20;     Ingestion

&#x20;         │

&#x20;         ▼

&#x20;Cleaning + Validation

&#x20;         │

&#x20;         ▼

&#x20;Feature Engineering

&#x20;         │

&#x20;         ▼

&#x20;     PostgreSQL

&#x20;         │

&#x20;         ├───────────────┐

&#x20;         ▼               ▼

&#x20;  Analytics / ML     Forecasting

&#x20;         │               │

&#x20;         └───────┬───────┘

&#x20;                 ▼

&#x20;       Business Intelligence

&#x20;                 │

&#x20;       ┌─────────┴─────────┐

&#x20;       ▼                   ▼

&#x20;    FastAPI            Streamlit

&#x20;       │                   │

&#x20;       └─────────┬─────────┘

&#x20;                 ▼

&#x20;            End Users



Supporting:

MLflow + Logging + Testing + CI/CD + Docker

```



\---



## 22. Technology Stack



| Layer               | Technology            |

| ------------------- | --------------------- |

| Programming         | Python 3.13           |

| Data Processing     | Pandas, NumPy, SciPy  |

| Machine Learning    | Scikit-learn, XGBoost |

| Explainability      | SHAP                  |

| Database            | PostgreSQL            |

| API                 | FastAPI               |

| Dashboard           | Streamlit             |

| Visualization       | Plotly, Matplotlib    |

| Data Storage        | Parquet               |

| Experiment Tracking | MLflow                |

| Testing             | Pytest                |

| Code Quality        | Ruff, MyPy            |

| CI/CD               | GitHub Actions        |

| Containerization    | Docker                |

| Version Control     | Git / GitHub          |



\---



## 23. Architecture Goals



The architecture is designed around the following principles:



* Modular components

* Reproducible machine learning

* Separation of data and application layers

* Automated testing

* Version-controlled development

* Experiment tracking

* Explainable predictions

* API-based model serving

* Application monitoring

* Containerized deployment

* CI/CD automation





