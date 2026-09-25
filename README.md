# SmartRetail-X

## Real-Time Retail Intelligence, Demand Forecasting & Inventory Optimization Platform

SmartRetail-X is an end-to-end retail intelligence platform designed to transform transactional retail data into actionable business insights.

The platform combines data engineering, exploratory data analysis, machine learning, demand forecasting, inventory optimization, customer segmentation, product recommendations, anomaly detection, explainable AI, REST APIs, interactive dashboards, MLflow experiment tracking, automated testing, Docker containerization, and CI/CD.

---

## Key Capabilities

- Retail transaction data ingestion and cleaning
- Data validation and feature engineering
- PostgreSQL analytical database
- Exploratory data analysis
- Product-level demand forecasting
- Seven-day demand forecasting
- Inventory optimization
- Reorder recommendations
- Customer segmentation using RFM analysis
- Product recommendation engine
- Sales anomaly detection
- SHAP-based model explainability
- FastAPI REST API
- Streamlit interactive dashboard
- MLflow experiment tracking
- Centralized application logging
- Automated testing with Pytest
- Code quality with Ruff and MyPy
- Docker containerization
- GitHub Actions CI/CD

---

## Project Overview

Retail businesses generate large volumes of transaction data but often struggle to convert that data into reliable operational decisions.

SmartRetail-X addresses this problem by providing a unified analytics and machine-learning platform that connects the complete workflow:

```text
Raw Data
   ↓
Data Engineering
   ↓
Data Validation
   ↓
Feature Engineering
   ↓
PostgreSQL
   ↓
Analytics
   ↓
Machine Learning
   ↓
Business Intelligence
   ↓
FastAPI + Streamlit
   ↓
Monitoring + MLflow + Testing + CI/CD

The system is designed with modular components so that individual services can be improved, tested, deployed, and scaled independently.

Dataset

The project uses the UCI Online Retail II dataset.

The dataset contains real-world transactional data from a UK-based non-store online retailer covering approximately two years.

Dataset Statistics
Metric	Value
Original transactions	1,067,371
Cleaned transactions	1,033,036
Duplicate rows removed	34,335
Products	5,304
Invoices	53,628
Customers	5,942
Date range	Dec 2009 – Dec 2011

Source:

UCI Machine Learning Repository — Online Retail II

Architecture
                    ┌──────────────────────┐
                    │   UCI Online Retail  │
                    │      Dataset        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Ingestion &     │
                    │ Data Cleaning        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Validation &    │
                    │ Feature Engineering  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │ Analytics Database   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌─────────────┐
       │ Forecasting│   │ Customer   │   │ Anomaly     │
       │    ML      │   │Segmentation│   │ Detection   │
       └──────┬─────┘   └─────┬──────┘   └──────┬──────┘
              │                │                 │
              └────────────────┼─────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Business Intelligence│
                    │ & Recommendations   │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │    FastAPI      │        │    Streamlit    │
        │    REST API     │        │    Dashboard    │
        └─────────────────┘        └─────────────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Monitoring / MLflow  │
                    │ Testing / CI/CD      │
                    └──────────────────────┘
Technology Stack
Programming & Data
Python 3.13
Pandas
NumPy
SciPy
PyArrow
OpenPyXL
Machine Learning
Scikit-learn
XGBoost
SHAP
MLflow
Database
PostgreSQL
SQLAlchemy
psycopg2
Backend
FastAPI
Pydantic
Uvicorn
Dashboard
Streamlit
Plotly
Matplotlib
Seaborn
Development & DevOps
Git
GitHub
GitHub Actions
Docker
Pytest
Ruff
MyPy
Repository Structure
SmartRetail-X/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   │
│   └── dashboard/
│       └── pages/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── features/
│   ├── forecasting/
│   ├── inventory/
│   ├── segmentation/
│   ├── recommendations/
│   ├── anomaly_detection/
│   └── monitoring/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── models/
├── notebooks/
│
├── sql/
│   ├── schema/
│   ├── migrations/
│   └── analytics/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── fixtures/
│
├── configs/
├── scripts/
│
├── docs/
│   ├── architecture/
│   ├── database/
│   ├── research/
│   ├── api/
│   ├── dashboard/
│   ├── testing/
│   └── deployment/
│
├── docker/
├── logs/
│
├── README.md
├── .gitignore
└── pyproject.toml
Core Modules
1. Data Ingestion

The ingestion pipeline loads the UCI Online Retail II Excel dataset, combines the available sheets, standardizes column names, converts data types, removes exact duplicates, and prepares the dataset for downstream analytics.

Key processing steps:

Excel data ingestion
Sheet consolidation
Data type conversion
Duplicate removal
Transaction classification
Revenue calculation
Date feature generation
Data quality validation

Final cleaned dataset:

1,033,036 records
34,335 duplicate records removed
2. Feature Engineering

SmartRetail-X creates business and machine-learning features from the cleaned transaction data.

Features include:

Transaction type
Revenue
Sales quantity
Return quantity
Customer availability
Calendar features
Customer-level features
Product-level features
Time-based features

The feature engineering pipeline produces a reusable Parquet dataset for analytics and machine learning.

3. PostgreSQL Analytics Database

The platform uses PostgreSQL as its analytical database.

The database is organized into multiple logical schemas:

PostgreSQL
│
├── raw
├── staging
├── analytics
└── ml

The analytics layer follows a dimensional modeling approach.

Main tables:

analytics.dim_date
analytics.dim_product
analytics.dim_customer
analytics.fact_sales

Current database statistics:

Table	Records
dim_date	761
dim_product	5,304
dim_customer	5,942
fact_sales	1,033,036
Exploratory Data Analysis

The EDA layer analyzes retail performance across multiple business dimensions.

Analysis includes:

Revenue trends
Sales volume
Product performance
Customer behavior
Country-level sales
Returns
Transaction patterns
Customer RFM analysis
Correlation analysis

Current calculated metrics include:

Metric	Value
Sales revenue	20,317,957.86
Return value	1,462,424.18
Net revenue	18,855,533.68
Units sold	11,455,913
Units returned	1,046,134
Return rate	9.13%
Machine Learning

SmartRetail-X contains multiple machine-learning and analytical components.

Demand Forecasting

The forecasting system predicts daily product demand using historical transaction patterns.

Historical Sales
       │
       ▼
Daily Demand Dataset
       │
       ▼
Lag Features
       │
       ▼
Rolling Statistics
       │
       ▼
Calendar Features
       │
       ▼
Time-Based Train/Test Split
       │
       ▼
XGBoost Model
       │
       ▼
Seven-Day Forecast
Forecasting Features

The model uses:

Lag 1 day
Lag 7 days
Lag 14 days
Lag 28 days
Rolling mean 7 days
Rolling mean 14 days
Rolling mean 28 days
Rolling standard deviation
Rolling maximum
Day of week
Month
Quarter
Year
Weekend indicators

Feature engineering uses historical shifts before rolling calculations to reduce future-data leakage.

Final Forecasting Model

The current forecasting implementation uses XGBoost with a log-transformed target.

Parameter	Value
Estimators	800
Learning rate	0.03
Max depth	6
Min child weight	5
Subsample	0.80
Column sample	0.80
Regularization alpha	0.10
Regularization lambda	2.00
Random state	42
Current Evaluation
Metric	Result
MAE	90.17
RMSE	1527.03
WMAPE	84.49%

Forecasting metrics are based on the current project dataset and model configuration and may change after future model improvements.

Inventory Optimization

The inventory module converts demand history into inventory planning recommendations.

The workflow uses:

Average daily demand
Demand variability
Safety stock
Reorder point
Target inventory
Recommended order quantity
Historical Demand
       │
       ▼
Average Demand
       │
       ▼
Demand Variability
       │
       ▼
Safety Stock
       │
       ▼
Reorder Point
       │
       ▼
Target Inventory
       │
       ▼
Recommended Order Quantity
Limitation

The current implementation does not use real-time warehouse on-hand inventory.

Therefore, recommendations should be treated as planning recommendations rather than live purchase orders.

Customer Segmentation

Customer segmentation uses RFM analysis.

RFM Dimensions

Recency

How recently the customer purchased.

Frequency

How frequently the customer purchased.

Monetary

How much revenue the customer generated.

The system assigns RFM scores and maps customers into business segments.

Example segments include:

Champions
Loyal Customers
Potential Loyalists
At Risk
Lost Customers
New Customers

The segmentation output can support targeted retention and marketing analysis.

Product Recommendation Engine

SmartRetail-X includes a product association-based recommendation component.

The system analyzes product co-purchases to identify products that are frequently purchased together.

Potential applications:

Cross-selling
Product bundling
Personalized recommendations
Promotional campaigns
Basket analysis

The generated recommendation dataset contains product relationships that can be consumed by the API and dashboard.

Anomaly Detection

The anomaly detection module identifies unusual sales behavior.

Potential anomalies include:

Unusually high sales
Unusually low sales
Abnormal product activity
Unexpected transaction patterns

The anomaly detection output is stored as a reusable dataset and exposed through the FastAPI service.

Explainable AI

SmartRetail-X uses SHAP (SHapley Additive exPlanations) to provide model explainability.

The current implementation generates global feature importance based on mean absolute SHAP values.

This helps identify which forecasting features contribute most strongly to model predictions.

Mean absolute SHAP importance describes feature contribution magnitude. It does not by itself indicate whether a feature increases or decreases the prediction.

MLflow Experiment Tracking

MLflow is integrated into the demand forecasting workflow.

The system tracks:

Experiment name
Model parameters
Training rows
Testing rows
Feature count
MAE
RMSE
WMAPE
Model artifact

Current experiment:

SmartRetail-X Demand Forecasting

The MLflow integration improves:

Experiment reproducibility
Model comparison
Parameter tracking
Metric tracking
Model lifecycle management
FastAPI REST API

SmartRetail-X exposes machine-learning functionality through a FastAPI REST API.

API Endpoints
Method	Endpoint	Purpose
GET	/	API root
GET	/health	Health check
GET	/api/v1/info	API information
POST	/api/v1/forecast	Demand forecasting
POST	/api/v1/inventory/recommendation	Inventory recommendation
POST	/api/v1/customer/segment	Customer segmentation
POST	/api/v1/recommendations/	Product recommendations
POST	/api/v1/anomalies/product	Product anomaly detection
GET	/api/v1/explainability/feature-importance	SHAP feature importance
API Documentation

When the FastAPI application is running:

http://127.0.0.1:8001/docs

OpenAPI schema:

http://127.0.0.1:8001/openapi.json
Streamlit Dashboard

The Streamlit dashboard provides an interactive business intelligence interface.

Dashboard capabilities include:

Executive KPIs
Revenue analysis
Sales analysis
Product performance
Country analysis
Demand forecasting
Seven-day forecast visualization
Inventory recommendations
Customer segmentation
Product recommendations
Sales anomaly detection
SHAP feature importance
Interactive filters and charts
Monitoring and Logging

SmartRetail-X includes centralized application logging.

The logging system records:

Request start
Request completion
HTTP method
API path
Response status
Request duration
Exceptions

Logs are written to:

logs/smartretail.log

Rotating file logging is configured to prevent unlimited log-file growth.

The project uses timezone-aware UTC timestamps for application monitoring.

Testing

The project uses automated testing with Pytest.

Testing covers:

API health checks
API request logging
Forecasting workflow
Data validation
Model output validation
Anomaly detection
Customer segmentation
Recommendations
Inventory recommendations
Explainability outputs
Integration behavior
Current Test Result
38 passed
Code Quality

The project uses automated static analysis tools.

Ruff

Ruff is used for Python linting and code-quality checks.

Current status:

All checks passed
MyPy

MyPy is used for static type checking.

Current status:

Success: no issues found in 35 source files
CI/CD

GitHub Actions is used for continuous integration.

The CI pipeline automatically runs when changes are pushed to the main branch or submitted through pull requests.

Git Push / Pull Request
          │
          ▼
   GitHub Actions
          │
          ▼
   Python 3.13 Setup
          │
          ▼
   Install Dependencies
          │
          ▼
   Create Test Fixtures
          │
          ▼
      Ruff Check
          │
          ▼
       MyPy Check
          │
          ▼
      Pytest Suite
          │
          ▼
      Quality Gate
Docker

The project includes Docker-based deployment support.

Docker provides a consistent runtime environment for the application and its services.

Containerization supports:

FastAPI
Streamlit
PostgreSQL
MLflow
Persistent storage
Application networking
Security

Security considerations include:

Secrets excluded from Git
.env files excluded through .gitignore
Database credentials kept outside source code
API validation using Pydantic
Dependency management
Container security practices
Separation of configuration from application logic

Sensitive credentials should never be committed to the repository.

Reproducibility

The project is structured to make data processing and machine-learning experiments reproducible.

Reproducibility is supported through:

Version-controlled source code
Fixed random states where applicable
Defined feature pipelines
Documented datasets
MLflow experiment tracking
Model artifacts
Automated tests
CI/CD validation
Configuration files
Technical documentation
Project Documentation

Detailed technical documentation is available in the docs/ directory.

Architecture
docs/architecture/
├── system_architecture.md
├── data_pipeline.md
└── ml_forecasting_workflow.md
Database
docs/database/
├── database_architecture.md
└── data_dictionary.md
API
docs/api/
└── api_documentation.md
Dashboard
docs/dashboard/
└── dashboard_documentation.md
Research
docs/research/
└── technical_methodology.md
Testing
docs/testing/
└── testing_and_quality_assurance.md
Deployment
docs/deployment/
└── deployment_and_devops.md
Installation
Clone the Repository
git clone https://github.com/bprabhasbprabhas6-sudo/SmartRetail-X.git
cd SmartRetail-X
Create Virtual Environment

Windows:

python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1
Install Dependencies
python -m pip install -r requirements.txt

If requirements.txt is not available in a particular development version, install dependencies according to the project's pyproject.toml and environment configuration.

Running the FastAPI Service

From the project root:

uvicorn app.api.main:app --host 127.0.0.1 --port 8001

API:

http://127.0.0.1:8001

Swagger documentation:

http://127.0.0.1:8001/docs
Running the Streamlit Dashboard

Run the configured Streamlit dashboard entry point.

Example:

streamlit run app/dashboard/app.py

The exact dashboard entry point may vary depending on the deployment configuration.

Running Tests

Run the complete test suite:

pytest -v

Run Ruff:

ruff check app src tests configs

Run MyPy:

mypy app src --ignore-missing-imports
Running MLflow

The demand forecasting pipeline logs experiments to MLflow.

The project uses a local SQLite tracking database:

mlflow.db

Start the MLflow UI:

mlflow ui

Then open:

http://127.0.0.1:5000
GitHub Repository

Source code and documentation:

https://github.com/bprabhasbprabhas6-sudo/SmartRetail-X

Project Status

SmartRetail-X currently includes an integrated data engineering, analytics, machine-learning, API, dashboard, testing, monitoring, containerization, and CI/CD workflow.

Component	Status
Data ingestion	✅ Complete
Data cleaning	✅ Complete
Data validation	✅ Complete
Feature engineering	✅ Complete
PostgreSQL database	✅ Complete
Exploratory data analysis	✅ Complete
Demand forecasting	✅ Complete
Inventory optimization	✅ Complete
Customer segmentation	✅ Complete
Recommendation engine	✅ Complete
Anomaly detection	✅ Complete
Explainable AI	✅ Complete
FastAPI	✅ Complete
Streamlit dashboard	✅ Complete
MLflow tracking	✅ Complete
Automated testing	✅ Complete
Ruff	✅ Passing
MyPy	✅ Passing
Docker	✅ Complete
CI/CD	✅ Complete
Technical documentation	✅ Complete
Future Improvements

Potential future improvements include:

Real-time transaction ingestion
Real-time inventory synchronization
Improved demand forecasting models
Deep-learning forecasting models
Probabilistic forecasting
Automated model retraining
Data-drift detection
Model-drift monitoring
Advanced recommendation algorithms
Real-time anomaly detection
Redis caching
Background task processing
Cloud deployment
Kubernetes orchestration
Infrastructure as Code
Automated production deployment
Advanced observability
Role-based API authentication
Author

B. Prabhas

B.Tech — Computer Science & Engineering (Data Science)

Aditya University

GitHub:

https://github.com/bprabhasbprabhas6-sudo

Acknowledgement

This project was developed as an end-to-end data science and software engineering project with an emphasis on practical machine learning, analytics, production-oriented architecture, testing, and DevOps practices.

Conclusion

SmartRetail-X demonstrates how retail transaction data can be transformed into an integrated decision-support platform.

The project combines:

Data Engineering + Analytics + Machine Learning + Forecasting + Optimization + Explainable AI + APIs + Dashboards + Testing + DevOps

