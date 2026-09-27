# Agentic FacilityOps AI

An AI-powered smart facility operations platform that combines energy intelligence, predictive maintenance, occupancy analytics, security monitoring, cost optimization, and role-based facility access into a unified management dashboard.

## Overview

Agentic FacilityOps AI is designed to help facility teams monitor operational conditions, identify abnormal patterns, assess equipment health, analyze space utilization, detect security events, and identify potential cost-saving opportunities.

The platform uses specialized AI agents for different facility operations and integrates their outputs through a centralized **Streamlit dashboard**.

The system supports monitoring multiple facilities through an **Active Location** selection and provides **role-based access** for different facility users.

## 🚀 Live Demo

👉 **[Open the FacilityOps AI Dashboard](https://agentic-facilityops-ai-project-b8qjmnw4puqmle7ijyzfsm.streamlit.app/)**

Explore the live dashboard with role-based access, energy intelligence, predictive maintenance, occupancy analytics, security monitoring, and cost optimization.

## Key Features

### 🔐 Role-Based Login & Access

The platform provides a login system with two user roles:

#### 👨‍💼 Facility Manager

Facility Managers have access to the complete facility intelligence dashboard, including:

- 🏠 Overview
- ⚡ Energy Intelligence
- 🔧 Predictive Maintenance
- 👥 Occupancy Intelligence
- 🛡️ Security Intelligence
- 💰 Cost Optimization
- 📊 Facility Reports

#### 👷 Operator

Operators have access to operational monitoring features:

- 🏠 Overview
- ⚡ Energy Intelligence
- 🔧 Predictive Maintenance
- 👥 Occupancy Intelligence
- 🛡️ Security Intelligence

Cost Optimization and Facility Reports are restricted from the Operator view.

The current authentication system is designed as a **prototype/demo login system** using role-based session state in Streamlit.

### ⚡ Energy Intelligence

- Monitor electricity, water, temperature, HVAC usage, and occupancy
- Calculate total, average, and peak energy consumption
- Visualize energy consumption trends
- Detect abnormal consumption patterns using **Isolation Forest**
- Identify potential energy wastage
- Generate energy-efficiency recommendations
- Analyze energy consumption in relation to occupancy

### 🔧 Predictive Maintenance

- Monitor equipment operating conditions
- Analyze temperature, vibration, pressure, and operating hours
- Calculate equipment health scores
- Classify equipment condition as:
  - Healthy
  - Monitor Closely
  - Maintenance Required
  - Immediate Maintenance
- Generate maintenance alerts for critical equipment conditions
- Support proactive maintenance planning

### 👥 Occupancy Intelligence

- Monitor occupancy levels across facilities
- Calculate space utilization using occupancy and capacity
- Identify high-utilization and overcrowded conditions
- Compare actual occupancy with facility capacity
- Generate occupancy-related insights
- Forecast occupancy using a **Random Forest Regressor**
- Evaluate forecasting performance using an unseen test dataset

The current simulated occupancy dataset achieves approximately **86% forecast accuracy** on the unseen test portion.

### 🛡️ Security Intelligence

- Monitor facility access events
- Track granted and denied access
- Detect unauthorized access attempts
- Identify events involving unknown persons
- Generate security alerts
- Monitor visitor access events
- Provide security-related insights

### 💰 Cost Optimization

- Estimate operational energy costs
- Estimate maintenance-related costs
- Identify potential energy savings
- Estimate potential maintenance savings
- Analyze facility space utilization for resource optimization
- Generate cost-saving recommendations
- Combine information from Energy, Maintenance, and Occupancy agents

The Cost Optimization Agent demonstrates **cross-agent intelligence** by using outputs from multiple operational agents to generate higher-level cost insights.

> Cost figures and savings estimates are based on simulated operational data and illustrative assumptions for demonstration purposes.

## Dashboard

The application provides a unified Streamlit dashboard containing:

- 🏠 Overview
- ⚡ Energy Intelligence
- 🔧 Predictive Maintenance
- 👥 Occupancy Intelligence
- 🛡️ Security Intelligence
- 💰 Cost Optimization
- 📊 Facility Reports

### Active Location

The dashboard supports multiple simulated facilities:

- Headquarters • Building A
- Corporate Office • Building B
- University Campus

Selecting an active location filters the relevant operational data and updates the corresponding agent insights.

## System Architecture

```text
                 Facility Data
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
 Energy Agent   Maintenance Agent   Occupancy Agent
       │              │              │
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
              Cost Optimization Agent
                      │
                      ▼
             Facility Intelligence
                      │
                      ▼
             Streamlit Dashboard
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Security Agent          Executive Insights
