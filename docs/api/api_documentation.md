# SmartRetail-X API Documentation



## 1. Overview



SmartRetail-X exposes a FastAPI-based REST API for retail intelligence, demand forecasting, inventory planning, customer segmentation, product recommendations, anomaly detection, and machine-learning explainability.



The API acts as the service layer between the machine-learning components, PostgreSQL-backed analytics, and the Streamlit dashboard.



The API provides structured JSON responses that can be consumed by dashboards, applications, automated workflows, and future production clients.



\---



## 2. API Architecture



The API layer is implemented using FastAPI.



The main application is:



```text

app/api/main.py

```



API routes are organized under:



```text

app/api/routes/

```



The API architecture is:



```text

Client

&#x20;  |

&#x20;  v

FastAPI Application

&#x20;  |

&#x20;  +-- Forecast API

&#x20;  |

&#x20;  +-- Inventory API

&#x20;  |

&#x20;  +-- Customer Segmentation API

&#x20;  |

&#x20;  +-- Recommendation API

&#x20;  |

&#x20;  +-- Anomaly Detection API

&#x20;  |

&#x20;  +-- Explainability API

&#x20;  |

&#x20;  v

Machine Learning / Analytics Components

&#x20;  |

&#x20;  +-- PostgreSQL

&#x20;  +-- Processed Data

&#x20;  +-- ML Models

&#x20;  +-- MLflow

```



\---



## 3. Technology Stack



| Component           | Technology         |

| ------------------- | ------------------ |

| API Framework       | FastAPI            |

| Web Server          | Uvicorn            |

| Validation          | Pydantic           |

| Language            | Python 3.13        |

| Database            | PostgreSQL         |

| Machine Learning    | XGBoost            |

| Explainability      | SHAP               |

| Experiment Tracking | MLflow             |

| Dashboard           | Streamlit          |

| Testing             | Pytest             |

| API Testing         | FastAPI TestClient |

| Logging             | Python logging     |



\---



## 4. Base URL



During local development, the API runs at:



```text

http://127.0.0.1:8001

```



Interactive Swagger documentation:



```text

http://127.0.0.1:8001/docs

```



ReDoc documentation:



```text

http://127.0.0.1:8001/redoc

```



\---



## 5. Starting the API



From the SmartRetail-X project root:



```powershell

uvicorn app.api.main:app --host 127.0.0.1 --port 8001

```



The API will then be available at:



```text

http://127.0.0.1:8001

```



\---



## 6. API Root



### Endpoint



```http

GET /

```



### Purpose



Provides basic information about the SmartRetail-X API service.



### Example



```text

GET http://127.0.0.1:8001/

```



\---



## 7. Health Check



### Endpoint



```http

GET /health

```



### Purpose



Checks whether the SmartRetail-X API service is running correctly.



### Example



```text

GET http://127.0.0.1:8001/health

```



### Example Response



```json

{

&#x20; "status": "healthy",

&#x20; "service": "SmartRetail-X API"

}

```



### Expected Status



```text

200 OK

```



\---



## 8. API Information



### Endpoint



```http

GET /api/v1/info

```



### Purpose



Returns information about the API service and its available capabilities.



This endpoint can be used by clients to discover the services provided by SmartRetail-X.



\---



## 9. Demand Forecast API



### Endpoint



```http

POST /api/v1/forecast

```



### Purpose



Generates product demand forecasts using the SmartRetail-X machine-learning forecasting workflow.



The forecasting pipeline transforms historical retail transactions into daily product demand and uses time-series features with an XGBoost regression model.



The current forecasting workflow uses a log-transformed target.



### Example Request



```json

{

&#x20; "product\_id": "85123A",

&#x20; "forecast\_days": 7

}

```



### Response



The endpoint returns forecast information in JSON format.



Example structure:



```json

{

&#x20; "product\_id": "85123A",

&#x20; "forecast": \[

&#x20;   {

&#x20;     "date": "2026-01-01",

&#x20;     "predicted\_demand": 21.4

&#x20;   }

&#x20; ]

}

```



The exact response fields are defined by the corresponding Pydantic schema.



### Business Applications



The forecast API can support:



\* demand planning

\* replenishment planning

\* inventory optimization

\* purchasing decisions

\* stockout prevention

\* operational planning



\---



## 10. Inventory Recommendation API



### Endpoint



```http

POST /api/v1/inventory/recommendation

```



### Purpose



Provides inventory recommendations using historical demand statistics and inventory-planning calculations.



The inventory module calculates:



\* average daily demand

\* demand variability

\* safety stock

\* reorder point

\* target inventory

\* recommended order quantity



### Example Request



```json

{

&#x20; "product\_id": "85123A"

}

```



### Example Response



```json

{

&#x20; "product\_id": "85123A",

&#x20; "average\_daily\_demand": 22.17,

&#x20; "safety\_stock": 91.02,

&#x20; "reorder\_point": 246.2,

&#x20; "target\_inventory": 401.38,

&#x20; "recommended\_order\_qty": 401.38

}

```



The exact response structure is defined by the API schema.



### Important Limitation



The current implementation does not consume live warehouse on-hand inventory.



Therefore, the recommended order quantity should be considered a planning recommendation rather than a live purchase-order quantity.



\---



## 11. Customer Segmentation API



### Endpoint



```http

POST /api/v1/customer/segment

```



### Purpose



Identifies a customer's RFM-based segment.



The segmentation workflow uses:



\* Recency

\* Frequency

\* Monetary value



These values are converted into RFM scores and used to assign customer segments.



### Example Request



```json

{

&#x20; "customer\_id": 12345

}

```



### Example Response



```json

{

&#x20; "customer\_id": 12345,

&#x20; "segment": "At Risk"

}

```



The exact response structure is defined by the corresponding Pydantic schema.



### Business Applications



Customer segmentation can support:



\* retention campaigns

\* customer targeting

\* loyalty programs

\* marketing personalization

\* customer-value analysis



\---



## 12. Product Recommendation API



### Endpoint



```http

POST /api/v1/recommendations/

```



### Purpose



Returns product recommendations based on historical product association patterns.



The recommendation engine uses product co-occurrence relationships to identify related products.



### Example Request



```json

{

&#x20; "product\_id": "23131"

}

```



### Example Response



```json

{

&#x20; "product\_id": "23131",

&#x20; "recommendations": \[

&#x20;   "22423",

&#x20;   "22457",

&#x20;   "22699"

&#x20; ]

}

```



The exact response structure is defined by the corresponding API schema.



### Business Applications



The recommendation service can support:



\* cross-selling

\* product discovery

\* basket expansion

\* personalized shopping experiences



\---



## 13. Anomaly Detection API



### Endpoint



```http

POST /api/v1/anomalies/product

```



### Purpose



Identifies anomalous sales activity associated with a product.



The endpoint uses the project's precomputed sales anomaly results.



### Example Request



```json

{

&#x20; "product\_id": "37410"

}

```



### Example Response



```json

{

&#x20; "product\_id": "37410",

&#x20; "anomalies": \[]

}

```



The exact response structure is defined by the corresponding API schema.



### Business Applications



Anomaly detection can help identify:



\* unusual sales spikes

\* unusual sales drops

\* abnormal transaction behavior

\* potential data-quality issues

\* unusual demand patterns



\---



## 14. Explainability API



### Endpoint



```http

GET /api/v1/explainability/feature-importance

```



### Purpose



Provides global feature-importance information generated using SHAP.



The current implementation calculates mean absolute SHAP values to describe the relative contribution magnitude of model features across the evaluated dataset.



### Example



```text

GET http://127.0.0.1:8001/api/v1/explainability/feature-importance

```



### Example Response



```json

{

&#x20; "feature\_importance": \[

&#x20;   {

&#x20;     "feature": "lag\_7",

&#x20;     "importance": 0.42

&#x20;   }

&#x20; ]

}

```



### Interpretation



The current implementation provides global mean absolute SHAP importance.



It should not be interpreted as showing whether a feature increases or decreases an individual prediction.



\---



## 15. API Route Summary



| Method | Endpoint                                    | Purpose                   |

| ------ | ------------------------------------------- | ------------------------- |

| GET    | `/`                                         | API root                  |

| GET    | `/health`                                   | Health check              |

| GET    | `/api/v1/info`                              | API information           |

| POST   | `/api/v1/forecast`                          | Demand forecasting        |

| POST   | `/api/v1/inventory/recommendation`          | Inventory recommendation  |

| POST   | `/api/v1/customer/segment`                  | Customer segmentation     |

| POST   | `/api/v1/recommendations/`                  | Product recommendations   |

| POST   | `/api/v1/anomalies/product`                 | Product anomaly detection |

| GET    | `/api/v1/explainability/feature-importance` | SHAP feature importance   |



\---



## 16. HTTP Status Codes



The API follows standard HTTP status conventions.



| Status | Meaning                      |

| ------ | ---------------------------- |

| 200    | Successful request           |

| 400    | Invalid client request       |

| 404    | Requested resource not found |

| 422    | Request validation error     |

| 500    | Internal server error        |



FastAPI and Pydantic provide automatic validation for invalid request bodies.



\---



## 17. Request Validation



Request and response structures are validated using Pydantic models.



Schemas are organized under:



```text

app/api/schemas/

```



Pydantic validation provides:



\* type validation

\* required-field validation

\* structured API contracts

\* predictable JSON responses

\* automatic OpenAPI documentation



\---



## 18. Error Handling



The API uses FastAPI's exception-handling mechanisms and validation system.



Invalid requests return structured HTTP error responses.



Unexpected exceptions are captured by the centralized API logging middleware.



This helps developers identify failures while maintaining a consistent API interface.



\---



## 19. API Request Logging



SmartRetail-X includes centralized API request logging.



Each request records:



\* HTTP method

\* request path

\* response status

\* response duration



Example:



```text

Request started | method=GET | path=/health

Request completed | method=GET | path=/health | status=200 | duration\_ms=...

```



Failed requests are also logged with exception information.



\---



## 20. Logging Architecture



Centralized logging is implemented in:



```text

configs/logging\_config.py

```



Application logs are written to:



```text

logs/smartretail.log

```



The application uses a rotating file handler to prevent unlimited log-file growth.



The `logs/` directory is excluded from Git version control.



\---



## 21. Machine-Learning Model Integration



The API connects the service layer with the machine-learning components.



The demand forecasting workflow uses an XGBoost model.



Model artifacts are stored under:



```text

models/

```



The primary log-target forecasting model is:



```text

models/xgboost\_demand\_forecast\_log.json

```



The model uses a `log1p` target transformation during training and converts predictions back to the original demand scale.



\---



## 22. MLflow Integration



The forecasting workflow is tracked using MLflow.



MLflow records:



\* model parameters

\* training information

\* evaluation metrics

\* model artifacts

\* experiment runs



The experiment name is:



```text

SmartRetail-X Demand Forecasting

```



The documented training run produced:



```text

MAE: 90.17

RMSE: 1527.03

WMAPE: 84.49%

```



These metrics describe the evaluated forecasting dataset and should not be interpreted as universal production performance.



\---



## 23. Streamlit Integration



The Streamlit dashboard can consume the API endpoints to present machine-learning and analytics results through an interactive interface.



The integration architecture is:



```text

Streamlit Dashboard

&#x20;       |

&#x20;       v

&#x20;    FastAPI

&#x20;       |

&#x20;       +---- Forecasting

&#x20;       +---- Inventory

&#x20;       +---- Segmentation

&#x20;       +---- Recommendations

&#x20;       +---- Anomalies

&#x20;       +---- Explainability

```



This separation keeps the user interface independent from the underlying machine-learning implementation.



\---



## 24. API Testing



The API is tested using Pytest and FastAPI TestClient.



Testing covers:



\* health endpoint

\* API behavior

\* request logging

\* forecasting functionality

\* inventory functionality

\* segmentation functionality

\* recommendation functionality

\* anomaly detection

\* explainability



The project currently reports:



```text

38 tests passed

```



\---



## 25. OpenAPI Documentation



FastAPI automatically generates OpenAPI documentation.



Swagger UI:



```text

http://127.0.0.1:8001/docs

```



ReDoc:



```text

http://127.0.0.1:8001/redoc

```



Swagger UI can be used to:



1\. inspect available endpoints

2\. view request schemas

3\. submit test requests

4\. inspect JSON responses

5\. validate API behavior during development



\---



## 26. Security Considerations



The current API is designed primarily for local development and project demonstration.



A production deployment should additionally implement:



\* authentication

\* authorization

\* HTTPS

\* API rate limiting

\* secure secret management

\* request-size limits

\* input sanitization

\* CORS configuration

\* database connection security

\* audit logging



Credentials and environment secrets must never be committed to Git.



\---



## 27. Scalability Considerations



The API architecture can be extended for production workloads.



Potential improvements include:



\* asynchronous processing

\* connection pooling

\* Redis caching

\* background task queues

\* horizontal API scaling

\* container orchestration

\* centralized monitoring

\* cloud model serving

\* load balancing



\---



## 28. Docker Deployment



The application can be containerized using Docker.



A production-oriented architecture can be represented as:



```text

Load Balancer

&#x20;     |

&#x20;     v

FastAPI Containers

&#x20;     |

&#x20;     +---- PostgreSQL

&#x20;     |

&#x20;     +---- ML Model Store

&#x20;     |

&#x20;     +---- Monitoring

&#x20;     |

&#x20;     +---- MLflow

```



Docker configuration is maintained under:



```text

docker/

```



\---



## 29. CI/CD Integration



The GitHub Actions workflow automatically performs project quality checks.



The CI pipeline includes:



\* dependency installation

\* test fixture creation

\* Ruff linting

\* MyPy static analysis

\* Pytest execution



This helps prevent defective changes from being merged into the main branch.



\---



## 30. Code Quality



The API follows the project's code-quality standards.



Current checks include:



```text

Ruff

MyPy

Pytest

```



The project has been validated with:



```text

Ruff: All checks passed

MyPy: Success

Pytest: 38 passed

```



\---



## 31. API Data Flow



The complete request flow is:



```text

Client Request

&#x20;     |

&#x20;     v

FastAPI Router

&#x20;     |

&#x20;     v

Pydantic Validation

&#x20;     |

&#x20;     v

Business / ML Logic

&#x20;     |

&#x20;     +---- Processed Data

&#x20;     +---- PostgreSQL

&#x20;     +---- ML Model

&#x20;     +---- MLflow Artifacts

&#x20;     |

&#x20;     v

JSON Response

&#x20;     |

&#x20;     v

Client / Streamlit Dashboard

```



\---



## 32. API Design Goals



The SmartRetail-X API is designed around:



\* modularity

\* maintainability

\* reusable services

\* validated inputs

\* structured outputs

\* machine-learning integration

\* explainability

\* observability

\* automated testing

\* production scalability



\---



## 33. Current Limitations



### 33.1 Authentication



Authentication is not currently implemented.



### 33.2 Live Inventory



Inventory recommendations do not currently consume live warehouse stock levels.



### 33.3 Forecast Scope



The demand forecasting model was trained using selected high-volume products rather than every product in the original dataset.



### 33.4 Recommendation Coverage



The recommendation engine is based on historical product associations and may not capture every possible recommendation relationship.



### 33.5 Explainability



The current SHAP endpoint provides global feature importance rather than individual prediction explanations.



### 33.6 Production Infrastructure



The local development API is not equivalent to a fully production-hardened deployment.



\---



## 34. Future API Improvements



Planned improvements include:



\* JWT authentication

\* role-based access control

\* API version management

\* pagination

\* request caching

\* real-time inventory integration

\* batch forecasting

\* asynchronous prediction jobs

\* individual prediction explanations

\* API rate limiting

\* centralized observability

\* cloud deployment

\* model version selection



\---



## 35. Example Development Workflow



A typical development workflow is:



```text

1\. Activate virtual environment

2\. Start PostgreSQL

3\. Start FastAPI

4\. Open Swagger UI

5\. Test health endpoint

6\. Test forecast endpoint

7\. Test inventory endpoint

8\. Test segmentation endpoint

9\. Test recommendation endpoint

10\. Test anomaly endpoint

11\. Test explainability endpoint

12\. Run automated tests

13\. Run Ruff

14\. Run MyPy

15\. Commit changes

16\. Push to GitHub

```



\---



## 36. Repository Locations



API implementation:



```text

app/api/

```



API routes:



```text

app/api/routes/

```



API schemas:



```text

app/api/schemas/

```



Configuration:



```text

configs/

```



Tests:



```text

tests/

```



Documentation:



```text

docs/api/

```



\---



## 37. Conclusion



The SmartRetail-X API provides a modular service layer connecting machine-learning models, analytics data, inventory intelligence, customer segmentation, product recommendations, anomaly detection, and explainability.



The FastAPI architecture separates API routing from machine-learning and data-processing components while providing request validation, automatic OpenAPI documentation, centralized logging, automated testing, and a foundation for future production deployment.



The API serves as the integration layer between the SmartRetail-X intelligence platform and external clients such as the Streamlit dashboard.




