import streamlit as st
import plotly.express as px
from agents.energy_agent import EnergyAgent

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
# CUSTOM STYLING
# ==========================================
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

div[data-testid="stMetric"] {
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:

    st.title("⚡ FacilityOps AI")
    st.caption("AGENTIC BUILDING INTELLIGENCE")

    st.divider()

    st.markdown("### MAIN MENU")

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "⚡ Energy Intelligence",
            "🔧 Maintenance",
            "👥 Occupancy",
            "🛡️ Security",
            "📊 Reports"
        ],
        index=1,
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### FACILITY")

    facility = st.selectbox(
        "Active Location",
        [
            "Headquarters • Building A",
            "Corporate Office • Building B",
            "University Campus"
        ]
    )

    st.divider()

    st.markdown("### AGENT STATUS")

    st.success("🟢 Energy Agent Active")
    st.caption("Monitoring facility operations")

    st.divider()

    st.markdown("### SYSTEM STATUS")
    st.success("● All Systems Operational")

    st.caption("Data Source: Utility + IoT Dataset")

    st.divider()

    st.markdown("### USER")
    st.write("👤 Facility Manager")
    st.caption("Administrator")


# ==========================================
# LOAD ENERGY AGENT
# ==========================================
agent = EnergyAgent("data/energy_data.csv")

df = agent.load_data()

metrics = agent.analyze_energy()

anomalies = agent.detect_energy_anomalies()

# Get updated dataframe containing prediction
df = agent.data

accuracy = agent.evaluate_accuracy()

recommendations = agent.generate_recommendations()


# ==========================================
# HEADER
# ==========================================
col_title, col_status = st.columns([4, 1])

with col_title:
    st.title("Energy Intelligence")
    st.caption(
        f"AI-powered facility energy monitoring • {facility}"
    )

with col_status:
    st.write("")
    st.success("🟢 LIVE")


st.divider()


# ==========================================
# AI AGENT SUMMARY
# ==========================================
st.subheader("🤖 Energy Agent Overview")

agent_col1, agent_col2, agent_col3 = st.columns(3)

with agent_col1:
    st.metric(
        "Records Monitored",
        len(df)
    )

with agent_col2:
    st.metric(
        "Anomalies Detected",
        len(anomalies)
    )

with agent_col3:
    st.metric(
        "Agent Status",
        "ACTIVE"
    )


st.divider()


# ==========================================
# MAIN ENERGY METRICS
# ==========================================
st.subheader("Energy Performance")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Energy",
        f"{metrics['total_energy']:.0f} kWh"
    )

with c2:
    st.metric(
        "Average Usage",
        f"{metrics['average_energy']:.1f} kWh"
    )

with c3:
    st.metric(
        "Peak Usage",
        f"{metrics['peak_energy']:.1f} kWh"
    )

with c4:
    st.metric(
        "Model Accuracy",
        f"{accuracy:.1f}%"
    )


st.divider()


# ==========================================
# ENERGY TREND
# ==========================================
st.subheader("📈 Energy Consumption Trend")

fig1 = px.line(
    df,
    x="timestamp",
    y="electricity_kwh",
    title="Hourly Electricity Consumption"
)

fig1.update_layout(
    xaxis_title="Time",
    yaxis_title="Electricity Consumption (kWh)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==========================================
# ANOMALY VISUALIZATION
# ==========================================
st.subheader("🔍 AI Anomaly Detection")

fig2 = px.scatter(
    df,
    x="occupancy",
    y="electricity_kwh",
    color="prediction",
    hover_data=[
        "timestamp",
        "hvac_usage",
        "temperature_c"
    ],
    title="Electricity Consumption vs Facility Occupancy"
)

fig2.update_layout(
    xaxis_title="Occupancy",
    yaxis_title="Electricity Consumption (kWh)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================================
# ANOMALY TABLE
# ==========================================
st.subheader("⚠ Critical Energy Alerts")

st.caption(
    f"{len(anomalies)} unusual facility consumption patterns were detected by the Energy Agent."
)

if len(anomalies) > 0:

    st.dataframe(
        anomalies[
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
    st.success("No anomalies detected.")


st.divider()


# ==========================================
# AI RECOMMENDATIONS
# ==========================================
st.subheader("💡 AI Energy Recommendations")

for recommendation in recommendations:
    st.info("🤖 " + recommendation)


st.divider()


# ==========================================
# DATA SECTION
# ==========================================
st.subheader("🗄️ Integrated Facility Data")

st.caption(
    "Utility and IoT data processed by the Energy Agent"
)

with st.expander("Click to View Complete Dataset"):

    st.dataframe(
        df[
            [
                "timestamp",
                "electricity_kwh",
                "water_liters",
                "temperature_c",
                "hvac_usage",
                "occupancy",
                "label",
                "prediction"
            ]
        ],
        use_container_width=True
    )


# ==========================================
# FOOTER
# ==========================================
st.divider()

st.caption(
    "Agentic FacilityOps AI • Milestone 1 • Energy Intelligence & Monitoring"
)