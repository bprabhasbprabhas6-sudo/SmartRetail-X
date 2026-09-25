

# SmartRetail-X Streamlit Dashboard Documentation



## 1. Overview



SmartRetail-X provides an interactive Streamlit dashboard for monitoring retail intelligence, demand forecasting, inventory recommendations, customer segmentation, product recommendations, anomaly detection, and explainable machine learning insights.



The dashboard provides a business-friendly interface over the SmartRetail-X analytics, machine learning, and FastAPI layers.



The main objective of the dashboard is to transform complex analytical and machine learning outputs into clear visual insights that can support retail decision-making.



\---



## 2. Dashboard Objectives



The Streamlit dashboard is designed to:



\- Monitor important retail KPIs

\- Analyze sales and transaction behavior

\- Visualize product demand

\- Display demand forecasting results

\- Support inventory planning

\- Understand customer segments

\- Provide product recommendations

\- Detect unusual sales behavior

\- Explain machine learning model behavior

\- Provide a centralized interface for the SmartRetail-X platform



The dashboard acts as the primary presentation layer of the project.



\---



## 3. Dashboard Architecture



The dashboard follows a layered architecture.



```text

&#x20;                   SmartRetail-X Dashboard

&#x20;                            |

&#x20;                      Streamlit UI

&#x20;                            |

&#x20;       +--------------------+--------------------+

&#x20;       |                    |                    |

&#x20;    KPI Layer          Visualization Layer    ML Insights

&#x20;       |                    |                    |

&#x20;       +--------------------+--------------------+

&#x20;                            |

&#x20;                        FastAPI

&#x20;                            |

&#x20;       +--------------------+--------------------+

&#x20;       |                    |                    |

&#x20;  Forecasting          Inventory            Analytics

&#x20;       |                    |                    |

&#x20;       +--------------------+--------------------+

&#x20;                            |

&#x20;                      Data / ML Layer

&#x20;                            |

&#x20;       +--------------------+--------------------+

&#x20;       |                    |                    |

&#x20;  PostgreSQL          Parquet/CSV            ML Models



The dashboard can consume processed analytical data, machine learning outputs, and API responses.



4\. Streamlit Technology



The dashboard is implemented using Streamlit.



Main technologies

Python

Streamlit

Pandas

NumPy

Plotly

FastAPI

PostgreSQL

XGBoost

SHAP



Streamlit provides the interactive web interface while Python handles data processing and business logic.



5\. Dashboard Structure



The dashboard is organized into functional sections/pages.



Major dashboard areas include:



Executive Overview

Sales and KPI Analysis

Demand Forecasting

Inventory Recommendations

Customer Segmentation

Product Recommendations

Anomaly Detection

Explainable AI

System Information



The exact page arrangement can evolve as additional dashboard functionality is added.



6\. Executive Overview



The Executive Overview provides a high-level summary of the retail business.



Important metrics include:



Total transactions

Total invoices

Total products

Total customers

Gross sales revenue

Return value

Net revenue

Units sold

Units returned

Return rate



These KPIs allow users to understand the overall state of the retail dataset without inspecting individual transactions.



7\. KPI Cards



The dashboard uses KPI cards to display important business metrics.



Example KPIs:



Transactions

1,033,036



Invoices

53,628



Products

5,304



Customers

5,942



Net Revenue

18,855,533.68



Return Rate

9.13%



The KPI cards provide an immediate summary for business users.



8\. Sales Analysis



The sales analysis section provides visual insights into transaction behavior.



Possible visualizations include:



Revenue over time

Units sold over time

Sales by country

Sales by product

Invoice trends

Return trends

Transaction type distribution



These visualizations help identify changes in business activity over time.



9\. Revenue Analysis



Revenue analysis is performed using transaction-level sales information.



The project calculates:



Revenue = Quantity × Unit Price



Sales revenue and return value are analyzed separately before calculating net revenue.



The dashboard can display revenue trends using line charts and categorical comparisons using bar charts.



10\. Product Analysis



Product-level analysis helps identify important products and demand patterns.



The dashboard can display:



Top products by revenue

Top products by quantity

Product demand trends

Product return behavior

Product-level forecasts

Product recommendations



Products with unusual behavior can also be investigated through the anomaly detection section.



11\. Country Analysis



The original dataset contains country information for transactions.



The dashboard can visualize:



Revenue by country

Transaction count by country

Customer distribution by country

Product demand by country



Country-level analysis helps identify geographical patterns in the available retail data.



12\. Demand Forecasting



The demand forecasting section provides machine learning based demand predictions.



The forecasting workflow uses:



Historical daily demand

Lag features

Rolling statistics

Calendar features

XGBoost regression

Log-transformed target training

Recursive multi-day forecasting



The final forecasting model is stored as:



models/xgboost\_demand\_forecast\_log.json

13\. Forecasting Features



The forecasting model uses engineered features such as:



lag\_1

lag\_7

lag\_14

lag\_28

rolling\_mean\_7

rolling\_mean\_14

rolling\_mean\_28

rolling\_std\_7

rolling\_max\_7

day of week

day of month

month

quarter

year

weekend indicator



Lag and rolling features are created using previous observations to reduce the risk of future-data leakage.



14\. Seven-Day Forecast



The dashboard provides a seven-day demand forecasting view.



The forecast generation process uses recursive prediction.



Historical Demand

&#x20;      |

Feature Generation

&#x20;      |

XGBoost Model

&#x20;      |

Day 1 Forecast

&#x20;      |

Updated Features

&#x20;      |

Day 2 Forecast

&#x20;      |

Updated Features

&#x20;      |

...

&#x20;      |

Day 7 Forecast



The generated forecast is stored in:



data/processed/forecasting/forecast\_7\_days.csv

15\. Forecast Visualization



Forecast results can be displayed using:



Line charts

Product-level demand tables

Forecast trend charts

Historical versus predicted demand

Seven-day forecast summaries



Users can select products or forecasting outputs depending on the dashboard implementation.



16\. Forecasting Model Performance



The current log-target XGBoost model produced the following evaluation results on the configured test period:



MAE: 90.17

RMSE: 1527.03

WMAPE: 84.49%



The metrics should be interpreted in the context of the selected products, time split, demand distribution, and forecasting horizon.



These values should not be treated as universal performance guarantees for future data.



17\. Inventory Optimization



The inventory section connects demand information with inventory planning.



The system calculates inventory recommendations using:



Average daily demand

Demand variability

Safety stock

Reorder point

Target inventory

Recommended order quantity



The output file is:



data/processed/inventory\_recommendations.csv

18\. Inventory Recommendation Workflow

Historical Demand

&#x20;      |

Demand Statistics

&#x20;      |

Safety Stock

&#x20;      |

Reorder Point

&#x20;      |

Target Inventory

&#x20;      |

Recommended Order Quantity



This provides a structured approach for inventory planning.



19\. Inventory Dashboard



The dashboard can display:



Product ID

Average daily demand

Demand standard deviation

Safety stock

Reorder point

Target inventory

Recommended order quantity

Priority



Users can filter recommendations based on product or priority.



20\. Inventory Limitation



The current inventory optimization module does not have access to real-time physical on-hand inventory.



Therefore, recommended order quantities should be interpreted as analytical planning recommendations rather than real-time purchase orders.



Future versions can integrate:



Current stock

Supplier lead time

Purchase orders

Warehouse inventory

Stock-out history

Supplier constraints

21\. Customer Segmentation



The customer segmentation section provides an RFM-based view of customer behavior.



RFM represents:



Recency

Frequency

Monetary value



The segmentation output is stored in:



data/processed/customer\_segments.csv

22\. RFM Analysis

Recency



Measures how recently a customer purchased.



Frequency



Measures how frequently a customer purchased.



Monetary



Measures the customer's total monetary contribution.



These values are transformed into RFM scores for segmentation.



23\. Customer Segment Visualization



The dashboard can display:



Customer segment distribution

Recency distribution

Frequency distribution

Monetary distribution

RFM scores

Segment-level customer counts



Example segments include:



Champions

Loyal Customers

Potential Loyalists

New Customers

At Risk

Lost Customers



The exact segment assignment depends on the implemented RFM scoring logic.



24\. Customer Insights



Customer segmentation can help identify groups requiring different business actions.



For example:



High-value active customers

&#x20;       |

Retention strategies



At-risk customers

&#x20;       |

Re-engagement strategies



New customers

&#x20;       |

Onboarding strategies



These are analytical recommendations and should be combined with business context before operational decisions.



25\. Product Recommendation Engine



The recommendation section provides product relationship insights.



The recommendation engine analyzes product co-occurrence patterns from transaction data.



The output file is:



data/processed/product\_recommendations.csv

26\. Recommendation Visualization



The dashboard can display:



Selected product

Recommended products

Recommendation score

Product relationship information



Example workflow:



Select Product

&#x20;     |

Find Related Products

&#x20;     |

Calculate Recommendation Score

&#x20;     |

Display Recommendations

27\. Recommendation Use Cases



Product recommendations can support:



Cross-selling

Product discovery

Basket analysis

Promotional planning

Personalized retail experiences



The current recommendation implementation is a baseline and can be extended with more advanced collaborative filtering or hybrid recommendation approaches.



28\. Anomaly Detection



The anomaly detection section identifies unusual sales behavior.



The output is stored in:



data/processed/sales\_anomalies.csv



Anomalies can be investigated at product or transaction levels depending on the available data.



29\. Anomaly Dashboard



The dashboard can display:



Product ID

Date

Observed sales

Expected behavior

Anomaly score

Anomaly flag



Users can filter anomalies by product and investigate unusual activity.



30\. Anomaly Detection Workflow

Sales Data

&#x20;   |

Feature Preparation

&#x20;   |

Anomaly Detection

&#x20;   |

Anomaly Score

&#x20;   |

Flag Unusual Records

&#x20;   |

Dashboard Visualization



Anomaly detection can help identify unusual sales spikes, drops, or transaction behavior.



31\. Explainable AI



The dashboard includes an Explainable AI section based on SHAP analysis.



The current implementation provides global feature importance using mean absolute SHAP values.



The output file is:



data/processed/explainability/shap\_feature\_importance.csv

32\. SHAP Visualization



The dashboard can display:



Feature names

Mean absolute SHAP values

Feature importance ranking



The visualization helps users understand which features contributed most strongly to model predictions in aggregate.



The current global SHAP output should not be interpreted as showing whether a feature increases or decreases demand because mean absolute SHAP values represent magnitude rather than direction.



33\. API Integration



The Streamlit dashboard can communicate with the FastAPI backend.



The API provides endpoints for:



Demand forecasting

Inventory recommendations

Customer segmentation

Product recommendations

Anomaly detection

Explainability



The API base URL during local development is:



http://127.0.0.1:8001

34\. Dashboard and API Flow

User

&#x20;|

Streamlit Dashboard

&#x20;|

FastAPI

&#x20;|

Business Logic

&#x20;|

ML / Analytics Layer

&#x20;|

PostgreSQL / Processed Data / Models

&#x20;|

Response

&#x20;|

Streamlit Visualization



This architecture separates presentation logic from API and machine learning services.



35\. Dashboard Data Sources



The dashboard can use multiple project data sources.



Important outputs include:



data/processed/online\_retail\_cleaned.parquet

data/processed/online\_retail\_features.parquet

data/processed/forecasting/daily\_product\_demand.parquet

data/processed/forecasting/forecast\_7\_days.csv

data/processed/inventory\_recommendations.csv

data/processed/customer\_segments.csv

data/processed/product\_recommendations.csv

data/processed/sales\_anomalies.csv

data/processed/explainability/shap\_feature\_importance.csv



PostgreSQL provides an additional analytical data source.



36\. Interactive Dashboard Controls



Streamlit allows interactive controls such as:



Select boxes

Multiselect filters

Date filters

Product filters

Country filters

Segment filters

Priority filters

Buttons

Data tables



These controls allow users to explore the data without directly writing SQL or Python code.



37\. Visualization Technology



Plotly can be used for interactive charts.



Potential visualizations include:



Line charts

Bar charts

Pie charts

Histograms

Scatter plots

Heatmaps

Distribution plots



Interactive charts allow users to inspect values through hover information and filtering.



38\. Dashboard User Workflow



A typical user workflow is:



1\. Open Dashboard

&#x20;      |

2\. Review KPIs

&#x20;      |

3\. Analyze Sales

&#x20;      |

4\. Inspect Demand Forecast

&#x20;      |

5\. Review Inventory Recommendations

&#x20;      |

6\. Analyze Customer Segments

&#x20;      |

7\. View Product Recommendations

&#x20;      |

8\. Investigate Anomalies

&#x20;      |

9\. Review Explainable AI Insights



This workflow connects descriptive analytics with predictive and prescriptive components.



39\. Error Handling



The dashboard should handle common errors such as:



Missing data files

Invalid product IDs

API connection failures

Empty query results

Invalid user inputs

Model loading errors



User-friendly messages should be displayed instead of exposing internal exceptions.



40\. Dashboard Logging



The FastAPI layer includes centralized request logging.



Logged information includes:



HTTP method

Request path

Response status

Request duration

Failed requests



Application logs are stored under:



logs/smartretail.log



Log files are excluded from Git through .gitignore.



41\. Dashboard Testing



Dashboard-related functionality is supported by the project's automated testing architecture.



The project currently includes:



Unit tests

API tests

Integration tests

Fixture generation

Pytest

Ruff

MyPy



The project test suite currently passes successfully.



42\. Code Quality



The SmartRetail-X project uses:



Ruff for linting

MyPy for static type checking

Pytest for automated testing

Git for version control

GitHub Actions for CI/CD



The CI pipeline validates the project automatically when changes are pushed to the main branch.



43\. Deployment



The dashboard can be run locally using Streamlit.



Typical command:



streamlit run app/dashboard/dashboard.py



The exact dashboard entry file may change as the dashboard architecture evolves.



The project also contains Docker and CI/CD infrastructure for deployment workflows.



44\. Security Considerations



The dashboard should not expose:



Database passwords

API credentials

Environment secrets

Private keys

Local configuration secrets



Sensitive configuration should be stored using environment variables or .env files that are excluded from Git.



45\. Scalability



The dashboard architecture is designed so that the presentation layer can evolve independently from the backend.



Future scalability improvements include:



API caching

Database connection pooling

Asynchronous API calls

Pagination

Query optimization

Pre-aggregated analytics

Cloud deployment

Container orchestration

Authentication and authorization

46\. Current Dashboard Limitations



Current limitations include:



Some dashboard data is based on historical retail transactions.

Physical inventory on-hand data is not currently integrated.

Supplier lead times are not included in the inventory optimizer.

Recommendation logic is currently a baseline implementation.

Forecasting is focused on selected products.

SHAP analysis currently provides global mean absolute importance.

Real-time streaming data is not yet implemented.

Dashboard authentication is not yet implemented.

47\. Future Dashboard Improvements



Future versions can include:



Real-time sales monitoring

Live inventory integration

Advanced customer personalization

Improved recommendation algorithms

Forecast confidence intervals

Automated model retraining

Drift monitoring

Role-based dashboards

Authentication

Cloud deployment

Mobile-friendly views

Advanced business alerts

48\. Business Value



The SmartRetail-X dashboard brings together multiple analytical capabilities in one interface.



It helps users:



Understand retail performance

Monitor important KPIs

Analyze product demand

Forecast future demand

Plan inventory

Understand customer behavior

Discover product relationships

Detect unusual activity

Interpret machine learning outputs



The dashboard therefore connects data engineering, analytics, machine learning, APIs, and business intelligence into a unified platform.



49\. End-to-End Dashboard Architecture



The complete workflow can be summarized as:



UCI Online Retail II

&#x20;       |

&#x20;       v

Data Ingestion

&#x20;       |

&#x20;       v

Data Cleaning

&#x20;       |

&#x20;       v

Feature Engineering

&#x20;       |

&#x20;       +--------------------+

&#x20;       |                    |

&#x20;       v                    v

&#x20;  PostgreSQL          Processed Files

&#x20;       |                    |

&#x20;       +----------+---------+

&#x20;                  |

&#x20;                  v

&#x20;           Analytics / ML

&#x20;                  |

&#x20;      +-----------+-----------+

&#x20;      |           |           |

&#x20;      v           v           v

&#x20;Forecasting   Segmentation  Recommendations

&#x20;      |           |           |

&#x20;      +-----------+-----------+

&#x20;                  |

&#x20;                  v

&#x20;         Inventory / Anomaly

&#x20;                  |

&#x20;                  v

&#x20;             FastAPI

&#x20;                  |

&#x20;                  v

&#x20;            Streamlit

&#x20;                  |

&#x20;                  v

&#x20;               User

50\. Technology Stack Summary

Layer	Technology

Programming	Python

Dashboard	Streamlit

Visualization	Plotly

Data Processing	Pandas, NumPy

Database	PostgreSQL

API	FastAPI

Forecasting	XGBoost

Explainability	SHAP

Testing	Pytest

Linting	Ruff

Type Checking	MyPy

Experiment Tracking	MLflow

Version Control	Git/GitHub

CI/CD	GitHub Actions

Containerization	Docker

51\. Reproducibility



The dashboard is part of a reproducible machine learning project.



Important reproducibility components include:



Version-controlled source code

Documented data pipeline

Reusable feature engineering

Saved machine learning models

MLflow experiment tracking

Automated tests

CI/CD

Configuration files

Documentation



These components make it easier to reproduce and maintain the platform.



52\. Design Goals



The dashboard is designed around the following principles:



Simplicity

Interactivity

Business relevance

Reproducibility

Explainability

Scalability

Maintainability

Clear visualization



The goal is to make advanced data science outputs accessible to both technical and business users.



53\. Conclusion



The SmartRetail-X Streamlit dashboard serves as the interactive presentation layer of the complete retail intelligence platform.



It connects historical transaction data, PostgreSQL analytics, machine learning models, inventory optimization, customer segmentation, recommendations, anomaly detection, explainable AI, and FastAPI services.



By combining these capabilities into a single interface, SmartRetail-X demonstrates an end-to-end approach to building an industry-oriented retail analytics and machine learning platform.





### Step 4 — Save the file



In Notepad:



\*\*Ctrl + S\*\*



Then close Notepad.



After closing it, run \*\*only\*\*:



```powershell

Get-Item docs\\dashboard\\dashboard\_documentation.md | Select-Object Name,Length


