# SmartRetail-X Machine Learning and Forecasting Workflow

## 1. Overview

SmartRetail-X includes a machine learning workflow designed to forecast product demand and support inventory planning.

The forecasting system transforms historical retail transactions into daily product demand, creates time-series features, trains an XGBoost regression model, evaluates forecasting performance, tracks experiments with MLflow, generates future demand predictions, and connects the predictions to inventory optimization.

The complete workflow is:

```text
Historical Transactions
        ↓
Daily Product Demand
        ↓
Product Selection
        ↓
Forecasting Features
        ↓
Time-Based Train/Test Split
        ↓
XGBoost Model
        ↓
Log1p Target Transformation
        ↓
Model Evaluation
        ↓
MLflow Experiment Tracking
        ↓
7-Day Forecast
        ↓
Inventory Optimization
2. Machine Learning Objective

The primary machine learning objective is:

Predict future daily demand for retail products using historical transaction data.

Accurate demand forecasts can support:

Inventory planning
Reorder decisions
Safety stock calculations
Demand monitoring
Business planning
Stock availability analysis
3. Machine Learning Architecture

The SmartRetail-X forecasting architecture follows:

                    Transaction Data
                           │
                           ▼
                Daily Product Demand
                           │
                           ▼
              Forecasting Dataset
                           │
                           ▼
              Feature Engineering
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        Lag Features              Rolling Features
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  Calendar Features
                           │
                           ▼
                 Time-Based Split
                    /          \
                   /            \
                  ▼              ▼
               Training        Testing
                  │              │
                  └──────┬───────┘
                         ▼
                    XGBoost
                         │
                         ▼
                  Model Evaluation
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
           MLflow                 SHAP
              │                     │
              ▼                     ▼
        Model Tracking        Explainability
              │
              ▼
        7-Day Forecast
              │
              ▼
    Inventory Optimization
4. Source Data

The forecasting workflow uses the processed SmartRetail-X retail transaction dataset.

Primary source:

data/processed/online_retail_features.parquet

The feature dataset contains:

Rows: 1,033,036
Columns: 31

The dataset covers:

2009-12-01
to
2011-12-09
5. Forecasting Dataset Creation

The first forecasting stage converts transaction-level records into daily product demand.

Script:

src/forecasting/create_forecasting_dataset.py

The process groups transaction data by:

Product
Date

The demand value is calculated from valid sales quantities.

The resulting dataset is:

data/processed/forecasting/daily_product_demand.parquet
6. Daily Product Demand Dataset

The daily product demand dataset contains:

Rows: 534,499
Columns: 13
Products: 4,984

Date range:

2009-12-01
to
2011-12-09

Demand validation:

Missing demand: 0
Zero demand: 0
Negative demand: 0

Total demand:

11,455,913 units

Total revenue represented in the forecasting dataset:

20,317,957.86
7. Product Selection

Training forecasting models for every product can create unnecessary computational complexity.

SmartRetail-X therefore creates a focused forecasting dataset containing the top products based on demand.

Script:

src/forecasting/prepare_forecasting_data.py

The current forecasting workflow uses:

20 products

The resulting structure covers:

20 products × 711 days

for a total of:

14,220 product-day observations

This provides a manageable dataset for model development and evaluation.

8. Forecasting Feature Engineering

Forecasting features are generated using:

src/forecasting/create_forecasting_features.py

The objective is to provide the model with historical demand context without using future information.

The feature engineering process uses only information available before the prediction date.

9. Lag Features

Lag features represent historical demand values.

SmartRetail-X creates:

lag_1
lag_7
lag_14
lag_28

Meaning:

lag_1  → demand from previous day
lag_7  → demand from previous week
lag_14 → demand from two weeks earlier
lag_28 → demand from four weeks earlier

These features help the model identify short-term and recurring demand patterns.

10. Rolling Features

The workflow also creates rolling statistics.

Features include:

rolling_mean_7
rolling_mean_14
rolling_mean_28
rolling_std_7
rolling_max_7

These features represent:

Recent average demand
Medium-term demand
Longer-term demand
Demand variability
Recent maximum demand
11. Prevention of Data Leakage

Time-series forecasting requires careful prevention of future information leakage.

SmartRetail-X creates lagged values before calculating rolling statistics.

Conceptually:

Current Demand
      │
      └── excluded from historical rolling calculation

The rolling calculations are based on shifted historical observations.

This ensures that future demand does not become an input feature for predicting the current period.

12. Calendar Features

Calendar information is added to the forecasting dataset.

Examples include:

day_of_week
month
quarter
year
week
is_weekend

Calendar features allow the model to learn patterns associated with:

Weekdays
Weekends
Months
Seasons
Calendar periods
13. Forecasting Feature Dataset

The resulting feature dataset is stored under:

data/processed/forecasting/

Important files include:

daily_product_demand.parquet
forecasting_features.parquet
forecasting_training_data.parquet

These files form the intermediate data layer for model training.

14. Train/Test Split

Time-series data must not be randomly shuffled before splitting.

SmartRetail-X uses a chronological train/test split.

Script:

src/forecasting/split_forecasting_data.py

The dataset is divided into:

Training period
       ↓
Earlier observations

Testing period
       ↓
Later observations

This better represents real-world forecasting, where the model learns from the past and predicts the future.

15. Training Dataset

The current training dataset contains:

Training rows: 11,360

The model uses:

16 features

The training data contains historical observations available before the testing period.

16. Testing Dataset

The current testing dataset contains:

Testing rows: 2,860

The test period is later than the training period.

This allows evaluation of how the model performs on unseen future-like observations.

17. Baseline XGBoost Model

The initial forecasting model uses XGBoost regression.

The baseline model produced:

MAE: 121.67
RMSE: 1528.48
WMAPE: 114.01%

These results indicated that additional model improvements were necessary.

18. Improved XGBoost Model

The forecasting workflow was improved through model configuration and target transformation.

The improved configuration includes:

n_estimators: 800
learning_rate: 0.03
max_depth: 6
min_child_weight: 5
subsample: 0.8
colsample_bytree: 0.8
reg_alpha: 0.1
reg_lambda: 2.0
random_state: 42
n_jobs: -1

These parameters provide a more controlled gradient boosting configuration.

19. Target Transformation

The improved forecasting workflow uses a logarithmic transformation of the target variable.

Transformation:

log1p(demand)

During prediction, the transformation is reversed using:

expm1(prediction)

Conceptually:

Original Demand
      ↓
    log1p
      ↓
Transformed Target
      ↓
    XGBoost
      ↓
Prediction
      ↓
    expm1
      ↓
Original Demand Scale

This can help reduce the influence of highly skewed demand values.

20. Log-Target Training Script

The primary log-target training implementation is:

src/forecasting/train_xgboost_log.py

The script:

Loads the forecasting training data.
Separates features and target.
Applies log1p to the target.
Creates the XGBoost regressor.
Trains the model.
Generates predictions.
Applies expm1.
Calculates evaluation metrics.
Saves the trained model.
Logs the experiment to MLflow.
21. Model Evaluation

The forecasting model is evaluated using multiple metrics.

The main metrics are:

MAE
RMSE
WMAPE

These metrics provide different views of forecasting performance.

22. Mean Absolute Error

Mean Absolute Error measures the average absolute difference between actual and predicted demand.

Conceptually:

MAE
=
Average(|Actual - Predicted|)

A lower MAE indicates smaller average absolute prediction errors.

The log-target model achieved:

MAE: 90.17

on the current evaluation dataset.

23. Root Mean Squared Error

RMSE measures prediction error while assigning greater influence to larger errors.

Conceptually:

RMSE
=
Square Root of Average Squared Error

The current log-target model achieved:

RMSE: 1527.03

The relatively large RMSE compared with MAE indicates that some observations have substantially larger errors.

24. Weighted Mean Absolute Percentage Error

WMAPE measures absolute forecasting error relative to the total actual demand.

The current log-target model achieved:

WMAPE: 84.49%

WMAPE should be interpreted together with MAE and RMSE because each metric captures different characteristics of prediction error.

25. Model Artifacts

The forecasting workflow stores trained XGBoost models under:

models/

Important model artifacts include:

xgboost_demand_forecast.json
xgboost_demand_forecast_improved.json
xgboost_demand_forecast_log.json

The log-target model is used by the current seven-day forecasting workflow.

26. Seven-Day Forecasting

The seven-day forecast is generated using:

src/forecasting/generate_7day_forecast.py

The process uses the trained log-target XGBoost model.

Workflow:

Latest Historical Data
        ↓
Generate Features
        ↓
Predict Day 1
        ↓
Update Historical Context
        ↓
Predict Day 2
        ↓
Continue Recursively
        ↓
Predict Day 7
27. Recursive Forecasting

The seven-day forecasting process generates future predictions sequentially.

The prediction for one future day can become part of the historical context used for the next forecast day.

Conceptually:

Day 1 Prediction
      ↓
Day 2 Features
      ↓
Day 2 Prediction
      ↓
Day 3 Features
      ↓
Day 3 Prediction
      ↓
...
      ↓
Day 7 Prediction

Predictions are clipped to prevent negative demand values.

28. Forecast Output

The generated seven-day forecast is stored as:

data/processed/forecasting/forecast_7_days.csv

The output can be consumed by:

Inventory optimization
Streamlit dashboard
API services
Business reporting
29. MLflow Experiment Tracking

SmartRetail-X uses MLflow to track machine learning experiments.

Configuration:

configs/mlflow_config.py

Tracking backend:

sqlite:///mlflow.db

Experiment name:

SmartRetail-X Demand Forecasting
30. MLflow Parameters

The forecasting training process logs important parameters.

Examples include:

n_estimators
learning_rate
max_depth
min_child_weight
subsample
colsample_bytree
reg_alpha
reg_lambda
random_state
target_transformation
feature_count
training_rows
testing_rows

This makes experiments reproducible and comparable.

31. MLflow Metrics

The training workflow records:

MAE
RMSE
WMAPE

The current tracked run includes:

Run ID:
935add848e0d437da8c406a8eba2897f

MLflow therefore provides a persistent record of the forecasting experiment.

32. MLflow Model Artifact

The trained XGBoost model is also logged to MLflow.

The training script uses:

mlflow.xgboost.log_model(...)

This provides model lifecycle support beyond storing the model JSON file directly in the project.

33. SHAP Explainability

SmartRetail-X uses SHAP for model explainability.

Script:

src/monitoring/shap_demand_explanation.py

Output:

data/processed/explainability/shap_feature_importance.csv

The current implementation calculates global mean absolute SHAP feature importance.

This identifies which features have the largest average contribution magnitude to model predictions.

34. SHAP Interpretation

The current SHAP output should be interpreted as global feature importance.

It does not directly indicate whether a feature increases or decreases demand.

For example:

Higher mean absolute SHAP value
        ↓
Greater average contribution magnitude

Directional conclusions require examining individual SHAP values or dependence plots.

35. Forecasting and Inventory Optimization

The demand forecasting model provides an input to the inventory optimization system.

Workflow:

Historical Demand
       ↓
XGBoost Forecast
       ↓
Future Demand
       ↓
Demand Statistics
       ↓
Safety Stock
       ↓
Reorder Point
       ↓
Recommended Order Quantity

This connects machine learning predictions with operational inventory planning.

36. Inventory Optimization Inputs

The inventory optimization module uses demand-related statistics such as:

Average daily demand
Demand variability
Safety stock
Reorder point
Target inventory

Output:

data/processed/inventory_recommendations.csv

The current system does not have actual real-time warehouse on-hand inventory from the UCI dataset.

Therefore, recommendations are demand-based planning estimates rather than real-time stock commands.

37. FastAPI Integration

The forecasting model is exposed through the FastAPI application.

Forecast endpoint:

POST /api/v1/forecast

The API provides programmatic access to forecasting functionality.

This enables other applications or services to request demand predictions without directly interacting with the underlying model implementation.

38. Streamlit Integration

The forecasting output can also be presented through the Streamlit dashboard.

The dashboard can display:

Historical demand
Forecasted demand
Product-level trends
Forecast horizons
Inventory recommendations
Model insights

This provides a business-facing interface for the machine learning system.

39. Testing the Forecasting Workflow

The forecasting implementation is supported by automated tests.

Testing areas include:

Feature generation
Forecasting utilities
API behavior
Data validation
Model-related functionality
Fixture generation

The project currently contains:

38 passing tests

The tests are executed locally and through GitHub Actions.

40. Code Quality

The forecasting workflow is checked using:

Ruff
MyPy
Pytest

Current project validation results:

Ruff:
All checks passed

MyPy:
Success: no issues found

Pytest:
38 passed

This helps maintain consistent and reliable machine learning code.

41. Limitations

The current forecasting implementation has several limitations.

Product Coverage

The training workflow currently focuses on the top 20 products rather than every product.

Historical Data

The model uses historical transaction data and does not currently incorporate external factors such as:

Promotions
Marketing campaigns
Holidays from an external calendar
Competitor pricing
Real-time inventory
Supplier lead times
Weather
Evaluation

The current evaluation metrics show that forecasting error remains significant, especially when measured using RMSE and WMAPE.

Recursive Forecasting

Multi-step recursive forecasting can accumulate prediction errors across the forecast horizon.

These limitations should be considered when interpreting model outputs.

42. Future Improvements

Future versions of SmartRetail-X can improve the forecasting system through:

Forecasting more products
Hyperparameter optimization
Cross-validation designed for time series
Product-specific models
Global forecasting models
LightGBM or CatBoost comparison
Temporal Fusion Transformer
LSTM or GRU models
External holiday features
Promotion features
Pricing features
Inventory availability
Supplier lead-time data
Automated model retraining
Forecast drift monitoring
Forecast confidence intervals
43. Model Retraining Strategy

A production deployment could retrain the forecasting model periodically.

Example workflow:

New Transaction Data
        ↓
Data Validation
        ↓
Feature Engineering
        ↓
Model Retraining
        ↓
Model Evaluation
        ↓
MLflow Tracking
        ↓
Model Approval
        ↓
Model Deployment

Retraining frequency could be determined by:

Data volume
Forecast drift
Model performance
Business requirements
Availability of new data
44. Model Monitoring

A production forecasting system should monitor:

MAE
RMSE
WMAPE
Prediction distribution
Actual vs predicted demand
Feature distribution
Data drift
Forecast drift

Significant degradation can trigger model review or retraining.

45. Reproducibility

The forecasting workflow is designed to be reproducible.

Important components are version controlled:

src/forecasting/
configs/mlflow_config.py
tests/
models/

Training parameters are recorded through MLflow.

The dataset processing steps are documented so that the forecasting workflow can be repeated using the same source data.

46. End-to-End Forecasting Workflow

The complete workflow is:

UCI Online Retail II
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Daily Product Demand
        ↓
Top 20 Product Selection
        ↓
Lag Features
        ↓
Rolling Features
        ↓
Calendar Features
        ↓
Time-Based Train/Test Split
        ↓
Log1p Target Transformation
        ↓
XGBoost Training
        ↓
MAE / RMSE / WMAPE
        ↓
MLflow Tracking
        ↓
SHAP Explainability
        ↓
7-Day Recursive Forecast
        ↓
Inventory Optimization
        ↓
FastAPI
        ↓
Streamlit Dashboard
47. Business Value

The forecasting workflow provides a machine-learning foundation for retail decision support.

Potential business uses include:

Anticipating product demand
Supporting inventory planning
Reducing stockout risk
Identifying demand patterns
Supporting reorder planning
Improving operational visibility
Providing forecast-driven dashboard insights

The model should be treated as a decision-support component rather than a replacement for operational inventory systems.

48. Machine Learning Design Goals

The SmartRetail-X forecasting architecture is designed to provide:

Reproducible model training
Time-aware evaluation
Leakage prevention
Explainable predictions
Experiment tracking
Model artifact management
Automated testing
API integration
Dashboard integration
Inventory integration
Production-oriented scalability


