# Database Design

## Overview

EstimateFlex is an engineering effort estimation platform designed to estimate workload, duration and cost for technical studies, calculations, engineering projects, automation initiatives and technical deliverables.

The database is implemented using SQLite and follows a normalized relational model based on business entities and engineering estimation concepts.

---

# Estimation Philosophy

EstimateFlex is built around four engineering dimensions:

- Volume
- Complexity
- Risk
- Productivity

These dimensions are combined to estimate:

- Effort
- Duration
- Cost

The platform also supports:

- Scenario simulation
- Historical benchmarking
- Machine Learning prediction
- Performance monitoring

---

# Main Business Entities

- UserProfile
- Project
- ProjectEstimationContext
- Deliverable
- DeliverableType
- Scenario
- EstimationResult
- HistoricalProject
- ActualProjectResult
- ReviewMetrics
- Dataset
- MLModel
- PredictionResult

---

# USER_PROFILE

Represents a person, role or team used for estimation.

Examples:

- Junior Engineer
- Senior Engineer
- Engineering Team
- Flexibility Expert
- Data Analyst

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| name | TEXT |
| description | TEXT |
| hourly_rate | REAL |
| productivity_factor | REAL |
| quality_factor | REAL |
| review_factor | REAL |
| risk_tolerance | REAL |
| experience_level | INTEGER |
| created_at | DATETIME |
| updated_at | DATETIME |

---

# PROJECT

Represents an engineering project to estimate.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| profile_id | INTEGER FK |
| name | TEXT |
| customer | TEXT |
| description | TEXT |
| project_type | TEXT |
| status | TEXT |
| start_date | DATE |
| created_at | DATETIME |
| updated_at | DATETIME |

---

# PROJECT_ESTIMATION_CONTEXT

Stores the engineering estimation context used by the estimation engine.

The context contains the four key estimation dimensions:

- Volume
- Complexity
- Risk
- Productivity

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| project_id | INTEGER FK |
| deliverable_count | INTEGER |
| analysis_count | INTEGER |
| calculation_count | INTEGER |
| document_count | INTEGER |
| interface_count | INTEGER |
| meeting_count | INTEGER |
| review_count | INTEGER |
| technical_complexity | INTEGER |
| regulatory_complexity | INTEGER |
| calculation_complexity | INTEGER |
| data_complexity | INTEGER |
| integration_complexity | INTEGER |
| requirements_stability | INTEGER |
| planning_risk | INTEGER |
| technical_risk | INTEGER |
| customer_risk | INTEGER |
| automation_level | INTEGER |
| reuse_level | INTEGER |
| created_at | DATETIME |
| updated_at | DATETIME |

---

# DELIVERABLE_TYPE

Catalog of deliverable categories.

## Default Deliverable Types

| Code | Name |
|--------|--------|
| ANALYSIS | Analysis |
| CALCULATION | Calculation Note |
| REPORT | Report |
| PYTHON_TOOL | Python Tool |
| DASHBOARD | Dashboard |
| DOCUMENTATION | Documentation |
| AUDIT | Audit |
| TRAINING | Training |

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| code | TEXT |
| name | TEXT |
| description | TEXT |

---

# DELIVERABLE

Represents a deliverable produced by the project.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| project_id | INTEGER FK |
| deliverable_type_id | INTEGER FK |
| name | TEXT |
| quantity | INTEGER |
| complexity | INTEGER |
| review_required | BOOLEAN |
| estimated_weight | REAL |

---

# SCENARIO

Represents a simulation scenario applied to a project.

Examples:

- Optimistic
- Nominal
- Pessimistic
- Custom

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| project_id | INTEGER FK |
| name | TEXT |
| productivity_modifier | REAL |
| complexity_modifier | REAL |
| risk_modifier | REAL |
| cost_modifier | REAL |
| comment | TEXT |
| created_at | DATETIME |

---

# ESTIMATION_RESULT

Stores estimation engine results.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| project_id | INTEGER FK |
| scenario_id | INTEGER FK |
| estimated_hours | REAL |
| estimated_days | REAL |
| estimated_cost | REAL |
| confidence_level | REAL |
| generated_at | DATETIME |

---

# HISTORICAL_PROJECT

Stores completed projects used for benchmarking and model training.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| profile_id | INTEGER FK |
| project_name | TEXT |
| customer | TEXT |
| project_type | TEXT |
| completion_date | DATE |
| imported_at | DATETIME |

---

# ACTUAL_PROJECT_RESULT

Stores actual measured project execution values.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| historical_project_id | INTEGER FK |
| actual_hours | REAL |
| actual_days | REAL |
| actual_cost | REAL |
| actual_productivity | REAL |
| measured_at | DATETIME |

---

# REVIEW_METRICS

Stores estimation performance indicators.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| historical_project_id | INTEGER FK |
| estimation_error | REAL |
| productivity_index | REAL |
| variance | REAL |
| quality_score | REAL |
| calculated_at | DATETIME |

---

# DATASET

Stores Machine Learning training datasets.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| dataset_name | TEXT |
| record_count | INTEGER |
| version | TEXT |
| created_at | DATETIME |

---

# ML_MODEL

Stores trained Machine Learning models.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| dataset_id | INTEGER FK |
| model_name | TEXT |
| algorithm | TEXT |
| version | TEXT |
| score | REAL |
| trained_at | DATETIME |

---

# PREDICTION_RESULT

Stores Machine Learning prediction results.

## Fields

| Field | Type |
|---------|---------|
| id | INTEGER PK |
| project_id | INTEGER FK |
| model_id | INTEGER FK |
| predicted_hours | REAL |
| predicted_days | REAL |
| predicted_cost | REAL |
| prediction_score | REAL |
| generated_at | DATETIME |

---

# Database Relationships

```text
UserProfile
 ├── Project
 └── HistoricalProject

Project
 ├── ProjectEstimationContext
 ├── Deliverable
 ├── Scenario
 ├── EstimationResult
 └── PredictionResult

DeliverableType
 └── Deliverable

HistoricalProject
 ├── ActualProjectResult
 └── ReviewMetrics

Dataset
 └── MLModel
         └── PredictionResult
```

---

# Estimation Engine

EstimateFlex uses four engineering dimensions:

- Volume
- Complexity
- Risk
- Productivity

## Primary Formula

Effort = Volume × Complexity × Risk ÷ Productivity

## Derived Metrics

Cost = Effort × Hourly Rate

Duration = Effort ÷ Available Capacity

---

# Design Principles

The database is designed to support:

- Engineering effort estimation
- Scenario simulation
- Historical benchmarking
- Machine Learning training
- Predictive estimation
- Future MLOps capabilities

The model follows normalization principles and favors maintainability, scalability and traceability.