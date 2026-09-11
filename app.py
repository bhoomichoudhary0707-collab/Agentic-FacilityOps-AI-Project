import streamlit as st
import plotly.express as px
import pandas as pd

from agents.energy_agent import EnergyAgent
from agents.maintenance_agent import MaintenanceAgent
from agents.occupancy_agent import OccupancyAgent
from agents.security_agent import SecurityAgent


# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="FacilityOps AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# COLOR TOKENS
# ==========================================
BG = "#0D1420"
SURFACE = "#111B2B"
BORDER = "#202B3D"
TEXT_PRIMARY = "#E4E9F2"
TEXT_MUTED = "#8A98AD"
ACCENT = "#4C8DF5"
GREEN = "#5DCAA5"
AMBER = "#EF9F27"
RED = "#E24B4A"


# ==========================================
# CUSTOM STYLING
# ==========================================
st.markdown(
    f"""
    <style>

    .block-container {{
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }}

    div[data-testid="stMetric"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        padding: 16px 18px;
        border-radius: 12px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED};
        font-size: 13px;
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT_PRIMARY};
    }}

    hr {{
        border-color: {BORDER} !important;
    }}

    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 10px;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {SURFACE};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1rem;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# CHART THEME
# ==========================================
def chart_theme(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font_color=TEXT_PRIMARY,
        title_font_color=TEXT_PRIMARY,
        legend_font_color=TEXT_MUTED,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    fig.update_xaxes(
        gridcolor=BORDER,
        zerolinecolor=BORDER
    )

    fig.update_yaxes(
        gridcolor=BORDER,
        zerolinecolor=BORDER
    )

    return fig


# ==========================================
# SIDEBAR
# ==========================================

NAV_PAGES = [
    "🏠 Overview",
    "⚡ Energy Intelligence",
    "🔧 Maintenance",
    "👥 Occupancy",
    "🛡️ Security",
    "📊 Reports"
]


if "page" not in st.session_state:
    st.session_state.page = NAV_PAGES[0]


with st.sidebar:

    # Simple Streamlit title instead of custom HTML
    st.title("⚡ FacilityOps AI")

    st.caption(
        "AGENTIC BUILDING INTELLIGENCE"
    )

    st.divider()

    st.markdown("### Main menu")

    for nav_item in NAV_PAGES:

        if st.button(
            nav_item,
            key=f"nav_{nav_item}",
            use_container_width=True
        ):

            st.session_state.page = nav_item


    st.divider()

    st.markdown("### Facility")

    facility = st.selectbox(
        "Active Location",
        [
            "Headquarters • Building A",
            "Corporate Office • Building B",
            "University Campus"
        ]
    )


    st.divider()

    st.markdown("### Agent status")

    st.success(
        "🟢 Energy Agent Active"
    )

    st.success(
        "🟢 Maintenance Agent Active"
    )

    st.success(
        "🟢 Occupancy Agent Active"
    )


    st.divider()

    st.markdown("### System status")

    st.success(
        "● All Systems Operational"
    )

    st.caption(
        "Data source: Utility + IoT + Asset Monitoring"
    )


    st.divider()

    st.caption(
        "Signed in as"
    )

    st.write(
        "**Facility Manager**"
    )


page = st.session_state.page


# ==========================================
# LOAD ENERGY DATA
# ==========================================

energy_agent = EnergyAgent(
    "data/energy_data.csv"
)

energy_df = energy_agent.load_data()


# ==========================================
# FACILITY-BASED ENERGY DATA
# ==========================================

energy_df = energy_df.copy()


if facility == "Headquarters • Building A":

    energy_df = energy_df.iloc[:336].copy()

    multiplier = 1.00


elif facility == "Corporate Office • Building B":

    energy_df = energy_df.iloc[:240].copy()

    multiplier = 0.75


elif facility == "University Campus":

    energy_df = energy_df.iloc[:336].copy()

    multiplier = 1.35


energy_df["electricity_kwh"] = (
    energy_df["electricity_kwh"]
    * multiplier
)


energy_df["hvac_usage"] = (
    energy_df["hvac_usage"]
    * multiplier
)


energy_agent.data = energy_df


energy_metrics = (
    energy_agent.analyze_energy()
)


energy_anomalies = (
    energy_agent.detect_energy_anomalies()
)


energy_df = energy_agent.data


energy_accuracy = (
    energy_agent.evaluate_accuracy()
)


energy_recommendations = (
    energy_agent.generate_recommendations()
)


# ==========================================
# LOAD MAINTENANCE DATA
# ==========================================

maintenance_df = pd.read_csv(
    "data/asset_data.csv"
)


# ==========================================
# FACILITY-BASED MAINTENANCE DATA
# ==========================================

maintenance_df = maintenance_df.copy()


if facility == "Headquarters • Building A":

    maintenance_df = (
        maintenance_df.iloc[:5]
        .copy()
    )


elif facility == "Corporate Office • Building B":

    maintenance_df = (
        maintenance_df.iloc[:3]
        .copy()
    )


elif facility == "University Campus":

    maintenance_df = (
        maintenance_df.copy()
    )


maintenance_agent = MaintenanceAgent(
    maintenance_df
)


maintenance_results = (
    maintenance_agent.analyze_assets()
)

# ==========================================
# LOAD SECURITY DATA
# ==========================================

security_agent = SecurityAgent("data/security_data.csv")
security_agent.load_data()

security_df = security_agent.data.copy()

# Facility-based security data
security_df = security_df[
    security_df["facility"] == facility
].copy()

security_agent.data = security_df

security_results = security_agent.analyze_security()
security_alerts = security_agent.get_security_alerts()
security_status = security_agent.get_security_status()
security_insights = security_agent.generate_security_insights()


# ==========================================
# LOAD OCCUPANCY DATA
# ==========================================

occupancy_agent = OccupancyAgent(
    "data/occupancy_data.csv"
)


occupancy_df = (
    occupancy_agent.load_data()
)


# ==========================================
# FACILITY-BASED OCCUPANCY DATA
# ==========================================

occupancy_df = occupancy_df[
    occupancy_df["facility"] == facility
].copy()


occupancy_agent.data = occupancy_df


# ==========================================
# OCCUPANCY ANALYSIS
# ==========================================

occupancy_metrics = (
    occupancy_agent.analyze_occupancy()
)


occupancy_status = (
    occupancy_agent.get_occupancy_status()
)


occupancy_forecast, occupancy_accuracy = (
    occupancy_agent.forecast_occupancy()
)


occupancy_insights = (
    occupancy_agent.generate_insights()
)


# ==========================================
# OVERVIEW PAGE
# ==========================================

if page == "🏠 Overview":

    st.title(
        "Facility Operations Overview"
    )

    st.caption(
        f"Centralized AI-powered building intelligence • {facility}"
    )


    st.divider()


    # --------------------------------------
    # OVERVIEW METRICS
    # --------------------------------------

    alerts = len(
        maintenance_results[
            maintenance_results[
                "maintenance_alert"
            ] == "ALERT"
        ]
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "Energy Records",
            len(energy_df)
        )


    with col2:

        st.metric(
            "Energy Anomalies",
            len(energy_anomalies)
        )


    with col3:

        st.metric(
            "Assets Monitored",
            maintenance_results[
                "asset_id"
            ].nunique()
        )


    with col4:

        st.metric(
            "Maintenance Alerts",
            alerts
        )


    st.divider()


    # --------------------------------------
    # ELECTRICITY TREND
    # --------------------------------------

    st.subheader(
        "📈 Electricity Consumption"
    )


    fig_overview = px.line(
        energy_df,
        x="timestamp",
        y="electricity_kwh",
        title="Electricity Consumption Trend"
    )


    fig_overview.update_layout(
        xaxis_title="Time",
        yaxis_title="Electricity (kWh)"
    )


    fig_overview = chart_theme(
        fig_overview
    )


    st.plotly_chart(
        fig_overview,
        use_container_width=True
    )


    st.divider()


    # --------------------------------------
    # SYSTEM MODULES
    # --------------------------------------

    st.subheader(
        "🤖 Active Intelligence Modules"
    )


    m1, m2, m3 = st.columns(3)


    with m1:

        st.info(
            """
            **⚡ Energy Intelligence**

            Monitors energy consumption,
            detects anomalies and generates
            energy-saving recommendations.
            """
        )


    with m2:

        st.success(
            """
            **🔧 Predictive Maintenance**

            Monitors equipment health,
            calculates health scores and
            generates maintenance alerts.
            """
        )


    with m3:

        st.info(
            """
            **👥 Occupancy Intelligence**

            Monitors occupancy, calculates
            space utilization and forecasts
            facility usage.
            """
        )


# ==========================================
# ENERGY INTELLIGENCE PAGE
# ==========================================

elif page == "⚡ Energy Intelligence":

    st.title(
        "Energy Intelligence"
    )

    st.caption(
        f"AI-powered facility energy monitoring • {facility}"
    )


    st.divider()


    st.subheader(
        "🤖 Energy Agent Overview"
    )


    agent_col1, agent_col2, agent_col3 = (
        st.columns(3)
    )


    with agent_col1:

        st.metric(
            "Records Monitored",
            len(energy_df)
        )


    with agent_col2:

        st.metric(
            "Anomalies Detected",
            len(energy_anomalies)
        )


    with agent_col3:

        st.metric(
            "Agent Status",
            "ACTIVE"
        )


    st.divider()


    st.subheader(
        "Energy Performance"
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        st.metric(
            "Total Energy",
            f"{energy_metrics['total_energy']:.0f} kWh"
        )


    with c2:

        st.metric(
            "Average Usage",
            f"{energy_metrics['average_energy']:.1f} kWh"
        )


    with c3:

        st.metric(
            "Peak Usage",
            f"{energy_metrics['peak_energy']:.1f} kWh"
        )


    with c4:

        st.metric(
            "Model Accuracy",
            f"{energy_accuracy:.1f}%"
        )


    st.divider()


    st.subheader(
        "📈 Energy Consumption Trend"
    )


    fig1 = px.line(
        energy_df,
        x="timestamp",
        y="electricity_kwh",
        title="Hourly Electricity Consumption"
    )


    fig1.update_layout(
        xaxis_title="Time",
        yaxis_title="Electricity (kWh)"
    )


    fig1 = chart_theme(fig1)


    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    st.subheader(
        "🔍 AI Anomaly Detection"
    )


    fig2 = px.scatter(
        energy_df,
        x="occupancy",
        y="electricity_kwh",
        color="prediction",
        hover_data=[
            "timestamp",
            "hvac_usage",
            "temperature_c"
        ],
        title=(
            "Electricity Consumption "
            "vs Facility Occupancy"
        )
    )


    fig2 = chart_theme(fig2)


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    st.divider()


    st.subheader(
        "⚠ Critical Energy Alerts"
    )


    if len(energy_anomalies) > 0:

        st.dataframe(
            energy_anomalies[
                [
                    "timestamp",
                    "electricity_kwh",
                    "hvac_usage",
                    "occupancy",
                    "label",
                    "prediction"
                ]
            ],
            use_container_width=True
        )


    else:

        st.success(
            "No anomalies detected."
        )


    st.divider()


    st.subheader(
        "💡 AI Energy Recommendations"
    )


    for recommendation in (
        energy_recommendations
    ):

        st.info(
            "🤖 " + recommendation
        )


# ==========================================
# MAINTENANCE PAGE
# ==========================================

elif page == "🔧 Maintenance":

    st.title(
        "Predictive Maintenance"
    )

    st.caption(
        f"AI-powered equipment health monitoring • {facility}"
    )


    st.divider()


    st.subheader(
        "🔧 Maintenance Agent Overview"
    )


    total_assets = (
        maintenance_results[
            "asset_id"
        ].nunique()
    )


    critical_assets = len(
        maintenance_results[
            maintenance_results[
                "maintenance_prediction"
            ] == "Immediate Maintenance"
        ]
    )


    maintenance_required = len(
        maintenance_results[
            maintenance_results[
                "maintenance_prediction"
            ] == "Maintenance Required"
        ]
    )


    avg_health = (
        maintenance_results[
            "health_score"
        ].mean()
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        st.metric(
            "Assets Monitored",
            total_assets
        )


    with c2:

        st.metric(
            "Average Health Score",
            f"{avg_health:.1f}/100"
        )


    with c3:

        st.metric(
            "Critical Cases",
            critical_assets
        )


    with c4:

        st.metric(
            "Maintenance Required",
            maintenance_required
        )


    st.divider()


    st.subheader(
        "❤️ Equipment Health Scores"
    )


    fig_health = px.bar(
        maintenance_results,
        x="asset_name",
        y="health_score",
        color="maintenance_prediction",
        hover_data=[
            "temperature_c",
            "vibration",
            "pressure",
            "operating_hours"
        ],
        title="Equipment Health Assessment"
    )


    fig_health.update_layout(
        xaxis_title="Equipment",
        yaxis_title="Health Score (0-100)"
    )


    fig_health = chart_theme(
        fig_health
    )


    st.plotly_chart(
        fig_health,
        use_container_width=True
    )


    st.divider()


    st.subheader(
        "📈 Asset Condition Monitoring"
    )


    fig_condition = px.scatter(
        maintenance_results,
        x="temperature_c",
        y="vibration",
        size="operating_hours",
        color="maintenance_prediction",
        hover_data=[
            "asset_name",
            "pressure",
            "health_score"
        ],
        title="Temperature vs Vibration Analysis"
    )


    fig_condition = chart_theme(
        fig_condition
    )


    st.plotly_chart(
        fig_condition,
        use_container_width=True
    )


    st.divider()


    st.subheader(
        "⚠ Maintenance Alerts"
    )


    alert_data = maintenance_results[
        maintenance_results[
            "maintenance_alert"
        ] == "ALERT"
    ]


    if len(alert_data) > 0:

        st.warning(
            f"{len(alert_data)} asset records "
            "require maintenance attention."
        )


        st.dataframe(
            alert_data[
                [
                    "timestamp",
                    "asset_id",
                    "asset_name",
                    "temperature_c",
                    "vibration",
                    "pressure",
                    "health_score",
                    "maintenance_prediction",
                    "maintenance_alert"
                ]
            ],
            use_container_width=True
        )


    else:

        st.success(
            "No maintenance alerts generated."
        )


    st.divider()


    st.subheader(
        "🗄️ Asset Monitoring Data"
    )


    with st.expander(
        "Click to View Complete Asset Dataset"
    ):

        st.dataframe(
            maintenance_results,
            use_container_width=True
        )


# ==========================================
# OCCUPANCY PAGE
# ==========================================

elif page == "👥 Occupancy":

    st.title(
        "Occupancy Intelligence"
    )

    st.caption(
        f"AI-powered occupancy and space utilization monitoring • {facility}"
    )


    st.divider()


    st.subheader(
        "👥 Occupancy Agent Overview"
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        st.metric(
            "Records Monitored",
            occupancy_metrics[
                "total_records"
            ]
        )


    with c2:

        st.metric(
            "Average Occupancy",
            f"{occupancy_metrics['average_occupancy']:.1f}"
        )


    with c3:

        st.metric(
            "Peak Occupancy",
            occupancy_metrics[
                "peak_occupancy"
            ]
        )


    with c4:

        st.metric(
            "Average Utilization",
            f"{occupancy_metrics['average_utilization']:.1f}%"
        )


    st.divider()


    # ======================================
    # UTILIZATION TREND
    # ======================================

    st.subheader(
        "📊 Space Utilization"
    )


    fig_utilization = px.line(
        occupancy_status,
        x="timestamp",
        y="utilization",
        markers=True,
        title="Space Utilization Over Time"
    )


    fig_utilization.add_hline(
        y=80,
        line_dash="dash",
        annotation_text="High Utilization (80%)"
    )


    fig_utilization.add_hline(
        y=100,
        line_dash="dash",
        annotation_text="Overcrowded (100%)"
    )


    fig_utilization.update_layout(
        xaxis_title="Time",
        yaxis_title="Utilization (%)"
    )


    fig_utilization = chart_theme(
        fig_utilization
    )


    st.plotly_chart(
        fig_utilization,
        use_container_width=True
    )


    st.divider()


    # ======================================
# OCCUPANCY VS CAPACITY
# ======================================

    st.subheader(
    "🏢 Occupancy vs Capacity"
    )


    fig_capacity = px.line(
    occupancy_status,
    x="timestamp",
    y=["occupancy", "capacity"],
    markers=True,
    title="Actual Occupancy Compared with Building Capacity"
    )


    fig_capacity.update_layout(
    xaxis_title="Time",
    yaxis_title="People"
    )


    fig_capacity = chart_theme(
    fig_capacity
    )


    st.plotly_chart(
    fig_capacity,
    use_container_width=True
    )


    # ======================================
    # OCCUPANCY DATA TABLE
    # ======================================

    st.subheader(
        "📋 Occupancy Monitoring Data"
    )


    st.dataframe(
        occupancy_status[
            [
                "timestamp",
                "zone",
                "capacity",
                "occupancy",
                "utilization",
                "status"
            ]
        ],
        use_container_width=True
    )


    st.divider()


    # ======================================
    # FORECAST
    # ======================================

    st.subheader(
        "🔮 Occupancy Forecast"
    )


    forecast_col1, forecast_col2 = (
        st.columns(2)
    )


    with forecast_col1:

        st.metric(
            "Forecast Accuracy",
            f"{occupancy_accuracy:.1f}%"
        )


    with forecast_col2:

        st.metric(
            "Forecast Model",
            "Random Forest"
        )


    fig_forecast = px.line(
        occupancy_forecast,
        x="timestamp",
        y=[
            "occupancy",
            "predicted_occupancy"
        ],
        markers=True,
        title="Actual vs Predicted Occupancy"
    )


    fig_forecast.update_layout(
        xaxis_title="Time",
        yaxis_title="Occupancy"
    )


    fig_forecast = chart_theme(
        fig_forecast
    )


    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )


    st.divider()


    # ======================================
    # INSIGHTS
    # ======================================

    st.subheader(
        "💡 Occupancy Insights"
    )


    for insight in occupancy_insights:

        st.info(
            "🤖 " + insight
        )

    # ==========================================
    # SECURITY INTELLIGENCE
    # ==========================================

elif page == "🛡️ Security":

    st.title("Security Intelligence")
    st.caption(
        f"AI-powered access monitoring and security alerts • {facility}"
    )

    # Security metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Events",
        security_results["total_events"]
    )

    col2.metric(
        "Granted",
        security_results["granted_events"]
    )

    col3.metric(
        "Denied",
        security_results["denied_events"]
    )

    col4.metric(
        "Unauthorized",
        security_results["unauthorized_events"]
    )

    st.divider()

    # Security Event Monitoring
    st.subheader("🛡️ Security Event Monitoring")

    status_counts = (
        security_status["security_status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "security_status",
        "count"
    ]

    fig_security = px.bar(
        status_counts,
        x="security_status",
        y="count",
        title="Security Event Status"
    )

    fig_security.update_layout(
        xaxis_title="Security Status",
        yaxis_title="Number of Events"
    )

    fig_security = chart_theme(fig_security)

    st.plotly_chart(
        fig_security,
        use_container_width=True
    )

    st.divider()

    # Critical Security Alerts
    st.subheader("🚨 Critical Security Alerts")

    if not security_alerts.empty:

        st.warning(
            f"{len(security_alerts)} security events require attention."
        )

        st.dataframe(
            security_alerts[
                [
                    "timestamp",
                    "zone",
                    "access_type",
                    "person_type",
                    "event_type",
                    "access_status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No critical security alerts detected."
        )

    st.divider()

    # AI Security Insights
    st.subheader("🤖 AI Security Insights")

    for insight in security_insights:
        st.info("🛡️ " + insight)

    # Complete Security Data
    with st.expander("View Complete Security Event Data"):

        st.dataframe(
            security_status,
            use_container_width=True,
            hide_index=True
        )


# ==========================================
# REPORTS PAGE
# ==========================================

elif page == "📊 Reports":

    st.title(
        "Facility Reports"
    )

    st.caption(
        f"Facility intelligence summary • {facility}"
    )


    st.divider()


    st.subheader(
        "Current Facility Summary"
    )


    r1, r2, r3, r4 = (
        st.columns(4)
    )


    with r1:

        st.metric(
            "Energy Records",
            len(energy_df)
        )


    with r2:

        st.metric(
            "Assets",
            maintenance_results[
                "asset_id"
            ].nunique()
        )


    with r3:

        st.metric(
            "Occupancy Records",
            occupancy_metrics[
                "total_records"
            ]
        )


    with r4:

        st.metric(
            "Avg Utilization",
            f"{occupancy_metrics['average_utilization']:.1f}%"
        )


    st.divider()


    st.subheader(
        "Facility Status"
    )


    st.success(
        "🟢 Energy Agent operational"
    )

    st.success(
        "🟢 Maintenance Agent operational"
    )

    st.success(
        "🟢 Occupancy Agent operational"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Agentic FacilityOps AI • "
    "Milestones 1, 2 & 3 • "
    "Energy Intelligence + "
    "Predictive Maintenance + "
    "Occupancy Intelligence"
)