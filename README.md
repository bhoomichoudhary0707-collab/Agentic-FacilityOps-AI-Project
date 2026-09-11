# Agentic FacilityOps AI

An AI-powered smart facility operations platform designed to monitor facility resources, detect abnormal patterns, analyze equipment health, monitor occupancy, identify security events, and provide intelligent recommendations for efficient facility operations.

---

## Project Overview

Agentic FacilityOps AI is a smart facility management platform that uses AI-based agents to analyze operational data and generate useful insights.

The project is being developed incrementally through multiple milestones. The current implementation includes:

- **Milestone 1: Energy Intelligence and Monitoring**
- **Milestone 2: Predictive Maintenance**
- **Milestone 3: Occupancy and Security Intelligence**

The platform integrates the implemented agents into a single Streamlit application and supports facility-based monitoring through an **Active Location** selection.

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

Milestone 2 extends the platform with a **Maintenance Agent** for monitoring equipment health and identifying assets that may require maintenance.

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
Milestone 3: Occupancy and Security Intelligence

Milestone 3 extends the platform with Occupancy Intelligence and Security Intelligence for monitoring facility utilization, forecasting occupancy, and identifying security-related events.

Occupancy Intelligence

The Occupancy Agent analyzes facility occupancy data, calculates space utilization, identifies overcrowding, generates occupancy insights, and forecasts occupancy levels.

Features Implemented
Occupancy monitoring
Space utilization analysis
Occupancy vs capacity analysis
High-utilization detection
Overcrowding detection
Occupancy forecasting
Forecast accuracy evaluation
Facility-based occupancy monitoring
Occupancy insights
Streamlit dashboard integration
Occupancy Agent

The Occupancy Agent performs the following process:

Loads the occupancy dataset
Converts timestamps into usable time features
Calculates space utilization
Identifies high-utilization and overcrowded conditions
Analyzes occupancy patterns
Trains a Random Forest regression model
Evaluates predictions using an unseen test set
Generates occupancy forecasts
Produces occupancy-related insights
Occupancy Status

Occupancy records are classified as:

Normal
High Utilization
Overcrowded

Space utilization is calculated using:

Utilization (%) = (Occupancy / Capacity) × 100
Occupancy Forecasting

The Occupancy Agent uses a Random Forest Regressor to forecast occupancy.

The forecasting model uses the following features:

Hour
Day
Month
Day of week
Cyclical hour features
Facility capacity

The dataset is split chronologically to evaluate the model on unseen data:

First 80% → Training Data
Last 20%  → Unseen Test Data

The current simulated dataset achieved approximately 86% forecast accuracy on the unseen test portion.

Note: This result is based on the current simulated dataset and should not be interpreted as real-world production accuracy.

Occupancy Flow
Occupancy Data
      ↓
Space Utilization Calculation
      ↓
Occupancy Analysis
      ↓
Overcrowding Detection
      ↓
Random Forest Forecasting
      ↓
Occupancy Insights
Security Intelligence

The Security Agent monitors facility access events and identifies security-related events requiring attention.

Features Implemented
Security event monitoring
Access event analysis
Granted and denied access tracking
Unauthorized access detection
Visitor access monitoring
Security alert generation
High-risk event identification
Facility-based security monitoring
Security insights
Streamlit dashboard integration
Security Agent

The Security Agent performs the following process:

Loads the security event dataset
Analyzes access events
Tracks granted and denied access
Identifies unauthorized access attempts
Identifies events involving unknown persons
Generates security alerts
Classifies security event status
Generates security-related insights
Displays the results through the Streamlit dashboard
Security Status

Security events can be classified as:

Normal
Security Alert
High Risk

Security alerts are generated for events involving denied access or unknown persons.

Security Flow
Security Event Data
        ↓
Access Event Analysis
        ↓
Risk Identification
        ↓
Security Alert Generation
        ↓
Security Insights
Active Location

The dashboard supports multiple facilities through an Active Location selection.

The current datasets include:

Headquarters • Building A
Corporate Office • Building B
University Campus

The selected facility is used to filter the relevant operational data displayed by the agents.

Dashboard

The Streamlit dashboard integrates the implemented facility intelligence modules into a single application.

Current dashboard sections include:

Energy Intelligence
Predictive Maintenance
Occupancy Intelligence
Security Intelligence
Reports

The dashboard provides metrics, visualizations, alerts, forecasts, and AI-generated insights based on the selected facility.

Datasets

The project currently uses simulated datasets for different facility intelligence modules.

data/
├── energy_data.csv
├── asset_data.csv
├── occupancy_data.csv
└── security_data.csv
Energy Dataset

Contains facility utility and operational parameters used for energy monitoring and anomaly detection.

Asset Dataset

Contains equipment condition parameters used by the Maintenance Agent.

Occupancy Dataset

Contains:

Timestamp
Facility
Zone
Capacity
Occupancy
Security Dataset

Contains:

Timestamp
Facility
Zone
Access type
Person type
Event type
Access status
Technology Stack
Python
Pandas
NumPy
Scikit-learn
Streamlit
Plotly
GitHub
Project Structure
Agentic-FacilityOps-AI/
│
├── .streamlit/
│   └── config.toml
│
├── agents/
│   ├── energy_agent.py
│   ├── maintenance_agent.py
│   ├── occupancy_agent.py
│   └── security_agent.py
│
├── data/
│   ├── energy_data.csv
│   ├── asset_data.csv
│   ├── occupancy_data.csv
│   └── security_data.csv
│
├── utils/
│
├── app.py
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
Current Project Status
Milestone	Status
Milestone 1 – Energy Intelligence	Completed
Milestone 2 – Predictive Maintenance	Completed
Milestone 3 – Occupancy Intelligence	Completed
Milestone 3 – Security Intelligence	Completed
Milestone 4 – Cost Optimization & Enterprise Deployment	Planned
Future Development

Future milestones will extend the platform with additional facility intelligence and optimization capabilities, including cost optimization, cross-agent orchestration, executive-level reporting, and enterprise deployment.

License

This project is licensed under the MIT License.
