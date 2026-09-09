# Agentic FacilityOps AI

An AI-powered smart facility operations platform designed to monitor facility resources, detect abnormal patterns, analyze equipment health, and provide intelligent recommendations for efficient facility operations.

---

## Project Overview

Agentic FacilityOps AI is a smart facility management platform that uses AI-based agents to analyze operational data and generate useful insights.

The project is being developed incrementally through multiple milestones. The current implementation includes:

- **Milestone 1: Energy Intelligence and Monitoring**
- **Milestone 2: Predictive Maintenance**

The platform integrates both agents into a single Streamlit application and supports facility-based monitoring through an **Active Location** selection.

---

# Milestone 1: Energy Intelligence and Monitoring

Milestone 1 focuses on monitoring and analyzing facility energy consumption.

The system integrates facility utility and IoT-related data and uses an Energy Agent to analyze consumption patterns, detect anomalies, and generate energy-efficiency recommendations.

## Features Implemented

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
4. Detects abnormal consumption patterns
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

# Milestone 2: Predictive Maintenance

Milestone 2 extends the platform with an AI-based **Maintenance Agent** for monitoring equipment health and identifying assets that may require maintenance.

The Maintenance Agent analyzes asset condition parameters and assigns a health score to each monitored asset.

## Features Implemented

- Asset health monitoring
- Equipment condition analysis
- Health score calculation
- Temperature-based condition checking
- Vibration-based condition checking
- Pressure-based condition checking
- Operating-hours monitoring
- Maintenance status classification
- Maintenance alerts
- Facility-based asset monitoring
- Integration with the existing Streamlit dashboard

---

## Maintenance Agent

The Maintenance Agent performs the following process:

1. Loads the asset monitoring dataset
2. Initializes the health score for each asset
3. Checks equipment parameters against predefined thresholds
4. Reduces the health score when critical conditions are detected
5. Determines the maintenance status of each asset
6. Generates maintenance alerts for critical cases
7. Displays the results through the Streamlit dashboard

### Asset Health Categories

Assets are categorized into:

- `Healthy`
- `Monitor Closely`
- `Maintenance Required`
- `Immediate Maintenance`

### Maintenance Flow

```text
Asset Data
    ↓
Parameter Analysis
    ↓
Health Score Calculation
    ↓
Maintenance Classification
    ↓
Maintenance Alert
