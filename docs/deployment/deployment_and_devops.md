# SmartRetail-X Deployment and DevOps Documentation



## 1. Overview



SmartRetail-X is designed as a modular retail intelligence platform that combines data engineering, machine learning, analytics, APIs, dashboards, containerization, and automated CI/CD.



The deployment and DevOps architecture provides a structured approach for running, testing, packaging, and maintaining the application.



The main DevOps technologies used are:



\- Docker

\- Docker Compose

\- Git

\- GitHub

\- GitHub Actions

\- Python

\- FastAPI

\- Streamlit

\- PostgreSQL

\- MLflow

\- Centralized logging



The deployment architecture separates application services, data storage, machine learning components, and development tooling.



\---



## 2. Deployment Objectives



The main deployment objectives are:



1\. Provide reproducible application environments.

2\. Package application components using containers.

3\. Automate software testing through CI/CD.

4\. Separate configuration from application code.

5\. Support PostgreSQL-backed analytics.

6\. Support FastAPI deployment.

7\. Support Streamlit dashboard deployment.

8\. Provide centralized application logging.

9\. Support MLflow experiment tracking.

10\. Provide a foundation for scalable deployment.



\---



## 3. DevOps Architecture



The SmartRetail-X DevOps architecture can be represented as:



```text

Developer

&#x20;   |

&#x20;   v

Git Repository

&#x20;   |

&#x20;   v

GitHub

&#x20;   |

&#x20;   v

GitHub Actions

&#x20;   |

&#x20;   +----------------------+

&#x20;   |                      |

&#x20;   v                      v

Ruff / MyPy             Pytest

&#x20;   |                      |

&#x20;   +----------+-----------+

&#x20;              |

&#x20;              v

&#x20;       CI Quality Gate

&#x20;              |

&#x20;              v

&#x20;       Docker Build

&#x20;              |

&#x20;              v

&#x20;       Application

&#x20;       Deployment

&#x20;              |

&#x20;      +-------+-------+

&#x20;      |               |

&#x20;      v               v

&#x20;   FastAPI        Streamlit

&#x20;      |               |

&#x20;      +-------+-------+

&#x20;              |

&#x20;              v

&#x20;         PostgreSQL



This architecture separates source control, automated validation, application services, and data storage.



4\. Deployment Components



The primary deployment components are:



Component	Purpose

FastAPI	REST API service

Streamlit	Interactive dashboard

PostgreSQL	Analytical database

MLflow	ML experiment and model tracking

Docker	Application containerization

GitHub Actions	CI/CD automation

Git	Version control

Logging	Runtime monitoring

5\. Source Code Management



Git is used for source-code version control.



The project repository is hosted on GitHub.



Repository:



https://github.com/bprabhasbprabhas6-sudo/SmartRetail-X



The primary branch is:



main



Git provides:



Version history

Change tracking

Collaboration

Branch management

Rollback capability

Release traceability

6\. Git Development Workflow



The standard development workflow is:



Create or Modify Code

&#x20;       |

&#x20;       v

Run Local Tests

&#x20;       |

&#x20;       v

Run Ruff

&#x20;       |

&#x20;       v

Run MyPy

&#x20;       |

&#x20;       v

Review Git Diff

&#x20;       |

&#x20;       v

Commit

&#x20;       |

&#x20;       v

Push to GitHub

&#x20;       |

&#x20;       v

GitHub Actions



This workflow helps identify issues before deployment.



7\. Git Repository Structure



The repository contains the following major areas:



SmartRetail-X/

├── app/

├── src/

├── data/

├── models/

├── notebooks/

├── sql/

├── tests/

├── configs/

├── scripts/

├── docs/

├── docker/

├── logs/

├── README.md

└── pyproject.toml



This structure separates application code, machine learning logic, data processing, tests, configuration, documentation, and deployment resources.



8\. Docker Containerization



Docker is used to package application components into reproducible environments.



Containerization provides:



Consistent runtime environments

Dependency isolation

Easier deployment

Reproducibility

Portability

Simplified service management



The project contains a dedicated:



docker/



directory for container-related configuration.



9\. Container Architecture



A deployment environment can contain multiple services.



Docker Environment

&#x20;       |

&#x20;       +----------------+

&#x20;       |                |

&#x20;       v                v

&#x20;    FastAPI         Streamlit

&#x20;       |                |

&#x20;       +-------+--------+

&#x20;               |

&#x20;               v

&#x20;          PostgreSQL

&#x20;               |

&#x20;               v

&#x20;          MLflow



The exact service configuration can be adjusted according to deployment requirements.



10\. FastAPI Deployment



FastAPI provides the REST API layer.



The application can be started locally using:



uvicorn app.api.main:app --host 127.0.0.1 --port 8001



For containerized deployment, the server can listen on:



0.0.0.0



with an exposed application port.



Example:



API Port: 8001



The API provides forecasting, inventory, segmentation, recommendations, anomaly detection, and explainability functionality.



11\. FastAPI Service



The FastAPI application is located at:



app/api/main.py



The API contains routes for:



/api/v1/forecast

/api/v1/inventory/recommendation

/api/v1/customer/segment

/api/v1/recommendations/

/api/v1/anomalies/product

/api/v1/explainability/feature-importance



Operational endpoints include:



/

&#x20;/health

/api/v1/info

12\. Streamlit Deployment



Streamlit provides the interactive analytics dashboard.



The dashboard consumes processed data and machine learning outputs and can also integrate with the FastAPI layer.



The deployment flow is:



User

&#x20;|

&#x20;v

Streamlit Dashboard

&#x20;|

&#x20;+-------------------+

&#x20;|                   |

&#x20;v                   v

Processed Data     FastAPI

&#x20;                    |

&#x20;                    v

&#x20;                ML Services



The dashboard provides business-oriented visualizations for sales, products, forecasting, inventory, customers, recommendations, anomalies, and explainability.



13\. PostgreSQL Deployment



PostgreSQL is the primary analytical database.



The current development database is:



smartretail\_x



The database contains structured schemas including:



raw

staging

analytics

public

ml



The analytics layer contains:



analytics.dim\_date

analytics.dim\_product

analytics.dim\_customer

analytics.fact\_sales

14\. Database Deployment Architecture



The database architecture is:



Application

&#x20;   |

&#x20;   v

FastAPI

&#x20;   |

&#x20;   v

PostgreSQL

&#x20;   |

&#x20;   +------------------+

&#x20;   |                  |

&#x20;   v                  v

Analytics Tables    ML Data



PostgreSQL provides persistent storage independently from application containers.



15\. Database Configuration



Database connection settings should be provided through environment variables rather than hard-coded credentials.



Typical configuration variables may include:



DATABASE\_HOST

DATABASE\_PORT

DATABASE\_NAME

DATABASE\_USER

DATABASE\_PASSWORD



Sensitive credentials should never be committed to Git.



16\. Environment Configuration



Application configuration should be separated from source code.



Environment-specific configuration can be provided using environment variables or environment files.



Typical configuration areas include:



Database connection

API configuration

MLflow tracking

Logging

Application ports

Deployment mode



The repository ignores .env files to reduce the risk of accidentally committing secrets.



17\. Secret Management



Sensitive values must not be stored directly in Python source code.



Examples include:



Database passwords

API keys

Access tokens

Cloud credentials

Authentication secrets



Recommended approaches include:



Environment variables

GitHub Actions secrets

Cloud secret managers

Docker secrets

Deployment-platform secret stores

18\. MLflow Deployment



MLflow is used for machine learning experiment tracking and model management.



The current project configuration uses:



SmartRetail-X Demand Forecasting



as the MLflow experiment name.



The local tracking configuration uses:



sqlite:///C:/Users/dell/Desktop/SmartRetail-X/mlflow.db



in the development environment.



19\. MLflow Architecture



The MLflow workflow is:



Model Training

&#x20;     |

&#x20;     v

MLflow Experiment

&#x20;     |

&#x20;     +----------------+

&#x20;     |                |

&#x20;     v                v

Parameters         Metrics

&#x20;     |                |

&#x20;     +-------+--------+

&#x20;             |

&#x20;             v

&#x20;         Model Artifact



This provides experiment traceability.



20\. Model Tracking



The demand forecasting workflow logs important model information.



Tracked parameters include:



Number of estimators

Learning rate

Maximum depth

Minimum child weight

Subsample

Column sampling

Regularization

Random state

Feature count

Training rows

Testing rows



This information helps reproduce and compare model experiments.



21\. Model Metrics



Forecasting experiments record:



MAE

RMSE

WMAPE



The current log-target XGBoost model recorded:



MAE: 90.17

RMSE: 1527.03

WMAPE: 84.49%



These metrics represent the current documented test-set evaluation and should be re-evaluated when the model or data changes.



22\. ML Model Artifacts



The forecasting model is stored in:



models/xgboost\_demand\_forecast\_log.json



MLflow additionally records the trained model as an MLflow model artifact.



Large model artifacts should be managed carefully in production environments.



23\. Logging Architecture



SmartRetail-X uses centralized application logging.



The configuration is located at:



configs/logging\_config.py



The application logger is:



smartretail



The log file is:



logs/smartretail.log

24\. Log Rotation



The logging system uses a rotating file handler.



Current configuration:



Maximum file size: 5 MB

Backup files: 3



Log rotation prevents the application log from growing indefinitely.



25\. API Monitoring



FastAPI middleware records request information.



The monitoring middleware records:



HTTP method

Request path

Response status

Request duration

Exceptions



Example:



Request started | method=GET | path=/health



Request completed | method=GET | path=/health | status=200 | duration\_ms=...



This information is useful for operational troubleshooting.



26\. CI/CD Architecture



Continuous Integration and Continuous Delivery are implemented using GitHub Actions.



The CI pipeline validates repository changes automatically.



Git Push

&#x20;  |

&#x20;  v

GitHub Actions

&#x20;  |

&#x20;  +----------+----------+

&#x20;  |          |          |

&#x20;  v          v          v

&#x20;Ruff       MyPy       Pytest

&#x20;  |          |          |

&#x20;  +----------+----------+

&#x20;             |

&#x20;             v

&#x20;      Quality Validation

27\. GitHub Actions Workflow



The CI workflow is located under:



.github/workflows/



The workflow is triggered by:



push -> main

pull\_request -> main



This ensures that changes entering the main branch are automatically validated.



28\. CI Environment



The CI pipeline currently uses:



Operating System: Ubuntu

Python Version: 3.13



Required dependencies are installed during the workflow.



This creates a clean environment for testing.



29\. CI Pipeline Steps



The pipeline performs the following steps:



1\. Checkout Repository

2\. Setup Python 3.13

3\. Upgrade pip

4\. Install Dependencies

5\. Create Test Fixtures

6\. Run Ruff

7\. Run MyPy

8\. Run Pytest



A failure in a required validation stage causes the workflow to fail.



30\. CI Dependency Installation



The CI workflow installs dependencies using Python's module-based pip command.



Example:



python -m pip install ...



This provides consistent dependency installation behavior across environments.



31\. Automated Testing in CI



Pytest is executed automatically in CI.



Current local validation result:



38 passed



This confirms that the currently implemented automated test suite passes in the development environment.



The test count may increase as the project evolves.



32\. Static Analysis in CI



Ruff is executed during CI.



Command:



ruff check app src tests



The latest local project-wide validation produced:



All checks passed!



Static analysis helps maintain consistent Python code quality.



33\. Type Checking in CI



MyPy is executed during CI.



Command:



mypy app src --ignore-missing-imports



The latest validation produced:



Success: no issues found in 35 source files



This helps identify potential type-related problems before deployment.



34\. CI Quality Gate



The CI pipeline acts as a quality gate.



Code Change

&#x20;    |

&#x20;    v

CI Pipeline

&#x20;    |

&#x20;    +---- Ruff ----+

&#x20;    |              |

&#x20;    +---- MyPy ----+

&#x20;    |              |

&#x20;    +---- Pytest --+

&#x20;                   |

&#x20;                   v

&#x20;            Validation Result



Successful validation increases confidence that the change is suitable for further deployment stages.



35\. Docker and CI/CD Integration



Docker can be integrated after CI validation.



The intended workflow is:



Git Push

&#x20;   |

&#x20;   v

Automated Tests

&#x20;   |

&#x20;   v

Static Analysis

&#x20;   |

&#x20;   v

CI Success

&#x20;   |

&#x20;   v

Docker Build

&#x20;   |

&#x20;   v

Container Image

&#x20;   |

&#x20;   v

Deployment



This separates software validation from application packaging.



36\. Deployment Workflow



The general deployment workflow is:



Developer

&#x20;   |

&#x20;   v

Git Commit

&#x20;   |

&#x20;   v

GitHub

&#x20;   |

&#x20;   v

GitHub Actions

&#x20;   |

&#x20;   v

Quality Checks

&#x20;   |

&#x20;   v

Docker Build

&#x20;   |

&#x20;   v

Application Image

&#x20;   |

&#x20;   v

Deployment Environment



This workflow can later be connected to a cloud container registry and deployment platform.



37\. Local Deployment



For local development, the FastAPI service can be started with:



uvicorn app.api.main:app --host 127.0.0.1 --port 8001



The Streamlit dashboard can be started using the project's dashboard entry point with:



streamlit run <dashboard\_file>



The exact dashboard entry point depends on the final dashboard application structure.



38\. Container Deployment



Containerized services can be deployed independently.



A possible deployment arrangement is:



+------------------+

| FastAPI Container|

+------------------+

&#x20;         |

&#x20;         v

+------------------+

| PostgreSQL       |

+------------------+



+------------------+

| Streamlit        |

| Container        |

+------------------+



+------------------+

| MLflow           |

| Service          |

+------------------+



This architecture supports independent service management.



39\. Docker Compose



Docker Compose can be used to coordinate multiple services during local or development deployment.



A typical service set may include:



api

dashboard

postgres

mlflow



Docker Compose provides:



Service orchestration

Network configuration

Environment variables

Volume management

Dependency relationships

40\. Persistent Storage



Stateful services require persistent storage.



PostgreSQL should use persistent storage so that database contents survive container restarts.



MLflow tracking data should also use persistent storage when required.



Example:



Container

&#x20;   |

&#x20;   v

Persistent Volume

&#x20;   |

&#x20;   v

Stored Data

41\. Network Architecture



Containerized services can communicate through an internal Docker network.



Example:



&#x20;                Docker Network

&#x20;                      |

&#x20;       +--------------+--------------+

&#x20;       |              |              |

&#x20;       v              v              v

&#x20;     API         PostgreSQL       MLflow

&#x20;       |

&#x20;       v

&#x20;  Dashboard



Internal service names can be used instead of hard-coded host addresses.



42\. Production Configuration



Production deployment should use configuration appropriate to the deployment environment.



Important production settings include:



Database host

Database port

Database credentials

API host

API port

Logging level

MLflow tracking URI

Model paths

Allowed origins

Authentication configuration



Development configuration should not automatically be reused in production.



43\. API Production Deployment



For production, FastAPI should listen on an externally accessible interface when appropriate.



Example:



uvicorn app.api.main:app --host 0.0.0.0 --port 8001



A production deployment may place FastAPI behind:



Reverse proxy

Load balancer

API gateway

Container platform

44\. Streamlit Production Deployment



The Streamlit dashboard can be deployed using:



Docker

Streamlit-compatible hosting

Cloud platforms

Virtual machines

Container orchestration platforms



The dashboard should connect to the production API and appropriate data services through environment-based configuration.



45\. Database Production Deployment



A production PostgreSQL deployment should provide:



Persistent storage

Authentication

Backup strategy

Monitoring

Connection pooling

Access control

Encryption where required

Recovery procedures



The current local PostgreSQL environment is primarily a development and project-validation environment.



46\. Backup Strategy



Production data should be backed up regularly.



Potential backup layers include:



PostgreSQL

&#x20;   |

&#x20;   +--> Daily Backup

&#x20;   |

&#x20;   +--> Weekly Backup

&#x20;   |

&#x20;   +--> Disaster Recovery Copy



Backup frequency should be selected according to business requirements.



47\. Database Migration Strategy



Database schema changes should be version controlled.



The project contains:



sql/schema/

sql/migrations/



Database changes should be applied in a controlled order.



Example:



Migration 001

&#x20;     |

&#x20;     v

Migration 002

&#x20;     |

&#x20;     v

Migration 003

&#x20;     |

&#x20;     v

Current Schema



This reduces the risk of inconsistent database environments.



48\. Security Architecture



Deployment security should follow the principle of least privilege.



Important controls include:



Strong database authentication

Secret management

Restricted database access

HTTPS

API authentication

Network restrictions

Dependency updates

Secure container configuration

Access logging



Security configuration should be strengthened before exposing the platform publicly.



49\. HTTPS



Production APIs should use HTTPS.



A typical architecture is:



Client

&#x20; |

&#x20; v

HTTPS

&#x20; |

&#x20; v

Reverse Proxy / Load Balancer

&#x20; |

&#x20; v

FastAPI



HTTPS protects data transmitted between clients and the application.



50\. Dependency Management



Application dependencies should be version controlled and reproducible.



Important dependency categories include:



Data processing

Machine learning

API

Dashboard

Database

Testing

Code quality

MLflow



The project uses:



pyproject.toml



for project configuration and dependency-related management.



51\. Dependency Security



Dependencies should be periodically reviewed for:



Security vulnerabilities

Compatibility issues

Unsupported versions

Breaking changes



Future CI improvements can include automated dependency vulnerability scanning.



52\. Container Security



Production containers should follow secure container practices.



Recommended controls include:



Minimal base images

Non-root users

Limited permissions

No secrets inside images

Pinned dependencies

Regular image updates

Vulnerability scanning

53\. Monitoring Strategy



The current monitoring foundation includes centralized logging and API request timing.



Future production monitoring can include:



CPU usage

Memory usage

API latency

Error rates

Request throughput

Database performance

Model performance

Data drift

Forecast accuracy

54\. Model Monitoring



Machine learning monitoring should track:



Model Predictions

&#x20;      |

&#x20;      v

Actual Demand

&#x20;      |

&#x20;      v

Forecast Error

&#x20;      |

&#x20;      v

Performance Trend



Possible monitored metrics include:



MAE

RMSE

WMAPE

Prediction distribution

Feature drift

Demand distribution changes

55\. Data Drift Monitoring



Data drift can occur when incoming retail data changes over time.



Potential signals include:



Changes in product distribution

Changes in customer behavior

Changes in transaction quantity

Changes in price distribution

Changes in country distribution



Future monitoring can compare current distributions against historical baselines.



56\. Model Retraining



The forecasting model should be periodically retrained as new transaction data becomes available.



A future workflow may be:



New Data

&#x20;  |

&#x20;  v

Data Validation

&#x20;  |

&#x20;  v

Feature Engineering

&#x20;  |

&#x20;  v

Model Training

&#x20;  |

&#x20;  v

Model Evaluation

&#x20;  |

&#x20;  v

Model Comparison

&#x20;  |

&#x20;  v

MLflow Tracking

&#x20;  |

&#x20;  v

Model Approval

&#x20;  |

&#x20;  v

Deployment



This creates a repeatable model lifecycle.



57\. Release Management



Production releases should be version controlled.



A recommended release process is:



Development

&#x20;   |

&#x20;   v

Testing

&#x20;   |

&#x20;   v

CI Validation

&#x20;   |

&#x20;   v

Release Commit

&#x20;   |

&#x20;   v

Container Build

&#x20;   |

&#x20;   v

Deployment



Git tags can be introduced for formal releases.



58\. Rollback Strategy



A deployment system should support rollback when a release introduces a critical issue.



Possible rollback mechanisms include:



Previous Git commit

Previous Docker image

Previous model version

Previous database migration where supported



Example:



Current Release

&#x20;     |

&#x20;     v

Production Issue

&#x20;     |

&#x20;     v

Rollback

&#x20;     |

&#x20;     v

Previous Stable Version

59\. Disaster Recovery



A production deployment should define recovery procedures for:



Database failure

Application failure

Container failure

Model corruption

Configuration errors

Infrastructure failure



Recovery depends on backups, persistent storage, versioned artifacts, and documented deployment procedures.



60\. Scalability



The architecture is designed to support future scaling.



Potential scaling strategies include:



Multiple API replicas

Load balancing

Database optimization

Connection pooling

Background processing

Caching

Batch inference

Cloud storage

Container orchestration

61\. Horizontal Scaling



FastAPI can be scaled horizontally.



&#x20;                Load Balancer

&#x20;                     |

&#x20;         +-----------+-----------+

&#x20;         |           |           |

&#x20;         v           v           v

&#x20;      API-1       API-2       API-3

&#x20;         |           |           |

&#x20;         +-----------+-----------+

&#x20;                     |

&#x20;                     v

&#x20;                 PostgreSQL



This allows multiple application instances to process requests.



62\. Background Processing



Long-running operations should eventually be moved away from synchronous API requests.



Potential background workloads include:



Batch forecasting

Model retraining

Large data processing

Anomaly scanning

Recommendation generation



A future architecture can use a task queue or scheduled processing system.



63\. Caching



Caching can improve application performance for frequently requested information.



Potential cache targets include:



Dashboard KPIs

Product recommendations

Forecast results

Feature-importance data

Frequently accessed analytics queries



Caching strategy should be designed according to data freshness requirements.



64\. Database Optimization



Potential PostgreSQL optimization techniques include:



Indexing

Query optimization

Partitioning

Connection pooling

Materialized views

Aggregation tables

Query monitoring



These techniques become increasingly important as transaction volume grows.



65\. Deployment Observability



A mature deployment should combine:



Logs

&#x20;|

&#x20;+--> Metrics

&#x20;|

&#x20;+--> Traces

&#x20;|

&#x20;+--> Alerts

&#x20;|

&#x20;+--> Dashboards



The current project provides a foundation through structured application logging.



Future observability can expand into centralized metrics and distributed tracing.



66\. Alerting



Future alerting rules may monitor:



API error rates

High API latency

Database failures

Container failures

Model performance degradation

Data-quality failures

Disk usage

Memory usage



Alerts should be connected to appropriate operational channels.



67\. CI/CD Security



The CI/CD pipeline should protect secrets and deployment credentials.



Recommended practices include:



GitHub encrypted secrets

Minimal workflow permissions

Protected branches

Dependency scanning

Code review

No credentials in source files



Deployment credentials should never be printed in CI logs.



68\. Branch Protection



For collaborative development, the main branch can be protected using GitHub repository settings.



Possible rules include:



Pull request requirement

Required CI checks

Review requirement

Direct push restrictions



This can improve release safety for team development.



69\. Current DevOps Status



The current project contains the following DevOps capabilities:



Capability	Status

Git Version Control	Implemented

GitHub Repository	Implemented

GitHub Actions	Implemented

Pytest CI	Implemented

Ruff CI	Implemented

MyPy CI	Implemented

Docker	Implemented

FastAPI	Implemented

Streamlit	Implemented

PostgreSQL	Implemented

MLflow	Implemented

Centralized Logging	Implemented

Database Migrations	Structured

Production HTTPS	Future deployment configuration

Load Testing	Future

Advanced Monitoring	Future

Automated Model Retraining	Future

Cloud Deployment	Future

70\. Current Deployment Limitations



The current implementation has several deployment limitations.



The primary environment is still development-oriented.

Production cloud deployment is not yet standardized.

Production-grade secret management requires additional configuration.

Comprehensive load testing is not yet implemented.

Advanced observability is not yet implemented.

Automated model retraining is not fully operational.

Production database backup automation requires deployment-specific configuration.

Full end-to-end deployment testing can be expanded.

71\. Future DevOps Improvements



Future improvements include:



Cloud deployment

Kubernetes support

Container registry integration

Automated Docker builds

Automated deployment

Infrastructure as Code

Advanced monitoring

Centralized metrics

Distributed tracing

Security scanning

Automated dependency updates

Model monitoring

Automated retraining

Blue-green deployment

Canary deployment

72\. Infrastructure as Code



Future infrastructure can be managed using Infrastructure as Code.



Potential tools include:



Terraform

AWS CloudFormation

Azure Bicep

Pulumi



Infrastructure as Code provides reproducible deployment environments.



73\. Kubernetes Strategy



For larger deployments, Kubernetes could be used to manage:



API Pods

Dashboard Pods

Background Workers



with external services such as:



PostgreSQL

Object Storage

MLflow



Kubernetes can provide:



Service discovery

Scaling

Self-healing

Rolling deployments

Resource management

74\. Container Registry



A future production workflow can publish Docker images to a container registry.



Example:



GitHub

&#x20;  |

&#x20;  v

GitHub Actions

&#x20;  |

&#x20;  v

Docker Build

&#x20;  |

&#x20;  v

Container Registry

&#x20;  |

&#x20;  v

Deployment Platform



Possible registries include:



GitHub Container Registry

Docker Hub

Amazon ECR

Azure Container Registry

Google Artifact Registry

75\. Automated Deployment



A future CD pipeline can automatically deploy successful releases.



Example:



Git Push

&#x20;  |

&#x20;  v

CI Tests

&#x20;  |

&#x20;  v

Docker Build

&#x20;  |

&#x20;  v

Security Scan

&#x20;  |

&#x20;  v

Container Registry

&#x20;  |

&#x20;  v

Production Deployment



Deployment should only proceed after required quality checks succeed.



76\. Blue-Green Deployment



Blue-green deployment can reduce downtime.



&#x20;            Load Balancer

&#x20;                 |

&#x20;         +-------+-------+

&#x20;         |               |

&#x20;      Blue             Green

&#x20;     Current            New

&#x20;     Version           Version



Traffic can be moved to the new environment after validation.



77\. Canary Deployment



Canary deployment gradually exposes a new release to users.



Users

&#x20; |

&#x20; v

Load Balancer

&#x20; |

&#x20; +------> Existing Version

&#x20; |

&#x20; +------> New Version



A small percentage of traffic can be directed to the new release before full rollout.



78\. Deployment Documentation



Deployment procedures should remain synchronized with the source code.



Important documentation areas include:



Installation

Configuration

Docker

Database setup

API startup

Dashboard startup

CI/CD

Monitoring

Troubleshooting

Rollback



This documentation is maintained under:



docs/

79\. Troubleshooting Strategy



Common deployment troubleshooting areas include:



API not starting



Check:



Python environment

Dependencies

Port availability

Configuration

Logs

Database connection failure



Check:



PostgreSQL service

Host

Port

Database name

Credentials

Network connectivity

Dashboard failure



Check:



Streamlit installation

Dashboard entry point

API availability

Data files

Configuration

Container failure



Check:



Docker logs

Environment variables

Port mappings

Image build output

Container status

80\. Deployment Validation Checklist



Before deployment:



\[ ] Source code committed

\[ ] Git status clean

\[ ] Tests passing

\[ ] Ruff passing

\[ ] MyPy passing

\[ ] Configuration verified

\[ ] Secrets configured securely

\[ ] Database available

\[ ] Model artifacts available

\[ ] Docker build successful

\[ ] API health check successful

\[ ] Dashboard validated

\[ ] Logs verified

81\. Production Readiness Checklist



Before public production deployment, additional checks should include:



\[ ] HTTPS enabled

\[ ] Authentication configured

\[ ] Authorization configured

\[ ] Database backups configured

\[ ] Monitoring configured

\[ ] Alerting configured

\[ ] Load testing completed

\[ ] Security scanning completed

\[ ] Container vulnerabilities reviewed

\[ ] Rollback procedure tested

\[ ] Disaster recovery documented

82\. DevOps Reproducibility



The deployment architecture promotes reproducibility through:



Git version control

Python dependency management

Docker containerization

Environment-based configuration

Automated testing

CI/CD

MLflow experiment tracking

Database schema versioning

Documentation



These practices reduce differences between development and deployment environments.



83\. Deployment Data Flow



The complete deployment data flow is:



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

&#x20;       v

PostgreSQL

&#x20;       |

&#x20;       +----------------+

&#x20;       |                |

&#x20;       v                v

Machine Learning     Analytics

&#x20;       |                |

&#x20;       v                v

FastAPI            Streamlit

&#x20;       |                |

&#x20;       +--------+-------+

&#x20;                |

&#x20;                v

&#x20;             Users

84\. End-to-End DevOps Workflow



The complete development-to-deployment workflow is:



Developer

&#x20;   |

&#x20;   v

Local Development

&#x20;   |

&#x20;   v

Unit/API Tests

&#x20;   |

&#x20;   v

Ruff + MyPy

&#x20;   |

&#x20;   v

Git Commit

&#x20;   |

&#x20;   v

GitHub

&#x20;   |

&#x20;   v

GitHub Actions

&#x20;   |

&#x20;   v

Automated Validation

&#x20;   |

&#x20;   v

Docker Build

&#x20;   |

&#x20;   v

Container Registry

&#x20;   |

&#x20;   v

Deployment Environment

&#x20;   |

&#x20;   v

FastAPI + Streamlit

&#x20;   |

&#x20;   v

PostgreSQL + MLflow

&#x20;   |

&#x20;   v

Monitoring

85\. Business Value of DevOps



The DevOps architecture provides several business benefits:



Faster development cycles

More reliable releases

Reproducible environments

Reduced deployment errors

Better application monitoring

Improved maintainability

Faster issue detection

Easier scaling

Better model lifecycle management



These capabilities support the long-term operation of the retail intelligence platform.



86\. Design Principles



The SmartRetail-X deployment architecture follows these principles:



Automate repeatable processes.

Keep configuration separate from code.

Protect secrets.

Test before deployment.

Version application changes.

Containerize deployment environments.

Monitor application behavior.

Track machine learning experiments.

Maintain database versioning.

Design for future scalability.

87\. Technology Stack Summary

Area	Technology

Version Control	Git

Repository	GitHub

CI/CD	GitHub Actions

Containerization	Docker

API	FastAPI

Dashboard	Streamlit

Database	PostgreSQL

ML Tracking	MLflow

Logging	Python Logging

Testing	Pytest

Code Quality	Ruff

Type Checking	MyPy

Language	Python 3.13

88\. Current Project Validation



The current project has successfully validated:



Pytest

38 passed



Ruff

All checks passed



MyPy

Success: no issues found in 35 source files



The project also has working:



FastAPI endpoints

Streamlit dashboard

PostgreSQL database

MLflow tracking

Docker configuration

GitHub Actions CI

Centralized logging

89\. Deployment Limitations and Scope



The current deployment architecture is suitable for development, demonstration, academic evaluation, and continued engineering.



Production deployment requires additional infrastructure-specific configuration.



These requirements may include:



Cloud hosting

HTTPS

Authentication

Production database

Backup systems

Secret management

Monitoring

Alerting

Load testing

Security testing



These items are identified as future deployment improvements rather than hidden assumptions.



90\. Conclusion



SmartRetail-X uses a structured DevOps architecture combining Git, GitHub, GitHub Actions, Docker, FastAPI, Streamlit, PostgreSQL, MLflow, automated testing, static analysis, and centralized logging.



The current implementation provides a strong foundation for reproducible development and automated quality validation.



The deployment architecture separates application services, database infrastructure, machine learning tracking, configuration, and monitoring.



Future improvements can extend the platform toward cloud-native deployment, automated container delivery, advanced observability, model monitoring, infrastructure as code, Kubernetes, and automated production releases.



The overall DevOps strategy supports the project's goal of becoming a maintainable, reproducible, scalable, and production-oriented retail intelligence platform.


