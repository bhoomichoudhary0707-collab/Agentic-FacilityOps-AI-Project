# Agentic FacilityOps AI

An AI-powered smart facility operations platform designed to monitor facility resources, detect abnormal patterns, and provide intelligent recommendations for efficient operations.

---

## Project Overview

Agentic FacilityOps AI is a smart facility management project that uses AI-based agents to analyze operational data and generate useful insights.

The project is being developed incrementally through multiple milestones. The current implementation includes **Milestone 1: Energy Intelligence and Monitoring**.

---

## Milestone 1: Energy Intelligence and Monitoring

Milestone 1 focuses on monitoring and analyzing facility energy consumption.

The system integrates facility utility and IoT-related data and uses an Energy Agent to analyze consumption patterns, detect anomalies, and generate energy-efficiency recommendations.

### Features Implemented

- Energy consumption monitoring
- Total, average, and peak energy analytics
- Electricity consumption trend visualization
- Energy vs occupancy analysis
- AI-based anomaly detection
- Energy-efficiency recommendations
- Streamlit dashboard
- Validation using labelled simulated data

---

## Energy Agent

The Energy Agent performs the following tasks:

1. Loads the facility dataset
2. Analyzes energy consumption
3. Calculates total, average, and peak energy usage
4. Detects abnormal patterns
5. Evaluates predictions using labelled data
6. Generates energy-efficiency recommendations

---

## Anomaly Detection

The project uses the **Isolation Forest** machine learning algorithm to identify unusual facility consumption patterns.

The following features are used for anomaly detection:

- Electricity consumption
- Water consumption
- Temperature
- HVAC usage
- Occupancy

Each record is classified as:

- `Normal`
- `Anomaly`

---

## Dataset

For the current prototype, the project uses **simulated facility utility and IoT data**.

The dataset contains the following columns:

| Column | Description |
|---|---|
| `timestamp` | Date and time of the reading |
| `electricity_kwh` | Electricity consumption |
| `water_liters` | Water consumption |
| `temperature_c` | Temperature reading |
| `hvac_usage` | HVAC usage |
| `occupancy` | Number of occupants |
| `label` | Ground-truth label used for evaluation |

---

## Dashboard

The Streamlit dashboard provides:

- Key energy metrics
- Total energy consumption
- Average energy usage
- Peak energy usage
- Validation accuracy
- Energy consumption trends
- Energy vs occupancy visualization
- Detected anomalies
- Energy Agent recommendations
- Integrated facility dataset view

---

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

---

