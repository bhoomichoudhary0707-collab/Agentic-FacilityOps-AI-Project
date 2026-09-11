# Agentic FacilityOps AI

An AI-powered smart facility operations platform that combines energy monitoring, predictive maintenance, occupancy intelligence, and security monitoring into a unified facility management dashboard.

## Overview

Agentic FacilityOps AI is designed to help facility teams monitor operational conditions, identify abnormal patterns, assess equipment health, analyze space utilization, detect security events, and generate actionable insights.

The platform integrates multiple specialized agents into a single **Streamlit dashboard** with support for monitoring different facilities through an **Active Location** selection.

## Key Features

### Energy Intelligence

- Monitor electricity, water, temperature, HVAC, and occupancy data
- Calculate total, average, and peak energy consumption
- Visualize energy consumption trends
- Detect abnormal consumption patterns using **Isolation Forest**
- Generate energy-efficiency recommendations
- Analyze energy consumption against occupancy

### Predictive Maintenance

- Monitor equipment condition and operational parameters
- Analyze temperature, vibration, pressure, and operating hours
- Calculate equipment health scores
- Classify asset condition into:
  - Healthy
  - Monitor Closely
  - Maintenance Required
  - Immediate Maintenance
- Generate maintenance alerts for critical equipment conditions

### Occupancy Intelligence

- Monitor facility occupancy levels
- Calculate space utilization based on occupancy and capacity
- Identify high-utilization and overcrowded conditions
- Compare actual occupancy with building capacity
- Generate occupancy insights
- Forecast occupancy using a **Random Forest Regressor**
- Evaluate forecasting performance using an unseen test dataset

The current simulated occupancy dataset achieves approximately **86% forecast accuracy** on the unseen test portion.

### Security Intelligence

- Monitor facility access events
- Track granted and denied access
- Detect unauthorized access attempts
- Identify events involving unknown persons
- Generate security alerts
- Monitor visitor access events
- Provide security-related insights

## Dashboard

The Streamlit dashboard provides a unified interface for:

- Energy Intelligence
- Predictive Maintenance
- Occupancy Intelligence
- Security Intelligence
- Facility Reports

The **Active Location** feature allows the dashboard to display data for different facilities.

Currently supported facilities include:

- Headquarters • Building A
- Corporate Office • Building B
- University Campus

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Streamlit**
- **Plotly**
- **GitHub**

## Data

The project currently uses simulated facility datasets covering:

Energy and utility consumption
Equipment condition and asset monitoring
Occupancy and facility capacity
Security and access events

These datasets are used to demonstrate the platform's monitoring, analysis, forecasting, alert generation, and insight capabilities.

Future Development

The platform can be further extended with cost optimization, cross-agent orchestration, executive reporting, advanced forecasting, real-time data integration, and enterprise deployment.

##License

This project is licensed under the MIT License.

## Project Structure

```text
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
