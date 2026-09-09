import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

from agents.energy_agent import EnergyAgent
from agents.maintenance_agent import MaintenanceAgent


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
TEXT_MUTED = "#5B6B85"
ACCENT = "#4C8DF5"
ACCENT_SOFT = "#1B2C47"
GREEN = "#5DCAA5"
AMBER = "#EF9F27"
RED = "#E24B4A"

# ==========================================
# CUSTOM STYLING
# ==========================================
st.markdown(f"""
<style>

.block-container {{
    padding-top: 1.25rem;
    padding-bottom: 2rem;
}}

/* metric cards -> flat dark widget cards */
div[data-testid="stMetric"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    padding: 16px 18px;
    border-radius: 12px;
}}
div[data-testid="stMetricLabel"] {{ color: {TEXT_MUTED}; font-size: 13px; }}
div[data-testid="stMetricValue"] {{ color: {TEXT_PRIMARY}; }}

hr {{ border-color: {BORDER} !important; }}

/* alert boxes -> flat cards */
div[data-testid="stAlertContainer"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

/* charts and tables -> wrapped in the same card language */
div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 10px;
}}

/* sidebar container */
section[data-testid="stSidebar"] {{
    background-color: {SURFACE};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .block-container {{
    padding-top: 1rem;
}}

/* decorative accent rail down the left edge of the sidebar */
.side-rail {{
    width: 4px;
    height: 100%;
    min-height: 520px;
    background: {ACCENT_SOFT};
    border-radius: 4px;
}}

.nav-brand {{ display: flex; align-items: center; gap: 10px; padding: 4px 0 14px 0; }}
.nav-brand .logo {{
    width: 30px; height: 30px; border-radius: 8px; background: {ACCENT};
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 600; font-size: 14px;
}}
.nav-brand .title {{ font-size: 14px; font-weight: 600; color: {TEXT_PRIMARY}; margin: 0; }}
.nav-brand .subtitle {{ font-size: 11px; color: {TEXT_MUTED}; margin: 0; }}

.side-card {{
    background: {BG}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 10px 12px; margin-top: 6px;
}}
.side-card .label {{ font-size: 11px; color: {TEXT_MUTED}; margin: 0 0 2px 0; }}
.side-card .value {{ font-size: 20px; font-weight: 600; color: {ACCENT}; margin: 0; }}

/* nav buttons: make them left-aligned, full width list items */
div[data-testid="stSidebar"] div[data-testid="stButton"] button {{
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    border-radius: 8px;
    font-size: 14px;
    padding: 8px 12px;
}}
div[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {{
    background-color: transparent;
    border: 1px solid transparent;
    color: {TEXT_PRIMARY};
}}
div[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {{
    background-color: {ACCENT_SOFT};
    border: 1px solid {ACCENT};
    color: {TEXT_PRIMARY};
}}

</style>
""", unsafe_allow_html=True)


def chart_theme(fig):
    """Apply the dark widget palette to a plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font_color=TEXT_PRIMARY,
        title_font_color=TEXT_PRIMARY,
        legend_font_color=TEXT_MUTED,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def svg_polyline_points(series, width=400, height=140, pad=12, max_points=40):
    """Downsample a real numeric series into 'x,y x,y ...' points for an inline SVG polyline."""
    values = list(series.dropna())
    if len(values) == 0:
        return f"0,{height / 2} {width},{height / 2}"
    if len(values) > max_points:
        step = len(values) / max_points
        values = [values[int(i * step)] for i in range(max_points)]
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    n = len(values)
    points = []
    for i, v in enumerate(values):
        x = (i / (n - 1)) * width if n > 1 else 0
        y = height - pad - ((v - lo) / span) * (height - 2 * pad)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def donut_arc(pct, r=38, cx=50, cy=50):
    """Return stroke-dasharray/offset for one segment of a donut given its percent of 360."""
    circumference = 2 * 3.14159265 * r
    dash = circumference * (pct / 100)
    gap = circumference - dash
    return f"{dash:.1f} {gap:.1f}"


def overview_dashboard_html(energy_records, energy_anom_count, assets_monitored,
                             maintenance_alerts, electricity_series, hvac_pct, other_pct):
    chart_points = svg_polyline_points(electricity_series)
    hvac_dash = donut_arc(hvac_pct)
    other_dash = donut_arc(other_pct)
    other_offset = -1 * (2 * 3.14159265 * 38) * (hvac_pct / 100)

    return f"""
    <style>html,body{{margin:0;padding:0;background:{BG};}}</style>
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:{TEXT_PRIMARY}">
      <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:12px">
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px">
          <p style="font-size:12px;color:{TEXT_MUTED};margin:0 0 6px">Energy records</p>
          <p style="font-size:24px;font-weight:600;margin:0">{energy_records}</p>
        </div>
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px">
          <p style="font-size:12px;color:{TEXT_MUTED};margin:0 0 6px">Energy anomalies</p>
          <p style="font-size:24px;font-weight:600;margin:0;color:{AMBER if energy_anom_count>0 else TEXT_PRIMARY}">{energy_anom_count}</p>
        </div>
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px">
          <p style="font-size:12px;color:{TEXT_MUTED};margin:0 0 6px">Assets monitored</p>
          <p style="font-size:24px;font-weight:600;margin:0">{assets_monitored}</p>
        </div>
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px">
          <p style="font-size:12px;color:{TEXT_MUTED};margin:0 0 6px">Maintenance alerts</p>
          <p style="font-size:24px;font-weight:600;margin:0;color:{RED if maintenance_alerts>0 else GREEN}">{maintenance_alerts}</p>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:2fr 1fr;gap:12px">
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px">
          <p style="font-size:14px;font-weight:600;margin:0 0 10px">Electricity consumption trend</p>
          <svg viewBox="0 0 400 150" style="width:100%;height:150px" preserveAspectRatio="none">
            <line x1="0" y1="30" x2="400" y2="30" stroke="{BORDER}" stroke-width="1"/>
            <line x1="0" y1="70" x2="400" y2="70" stroke="{BORDER}" stroke-width="1"/>
            <line x1="0" y1="110" x2="400" y2="110" stroke="{BORDER}" stroke-width="1"/>
            <polyline fill="none" stroke="{ACCENT}" stroke-width="2" points="{chart_points}"/>
          </svg>
          <p style="font-size:11px;color:{TEXT_MUTED};margin:6px 0 0">Real electricity_kwh series for {facility}</p>
        </div>

        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:16px;display:flex;flex-direction:column;align-items:center">
          <p style="font-size:14px;font-weight:600;margin:0 0 10px;align-self:flex-start">Load split</p>
          <svg viewBox="0 0 100 100" width="110" height="110">
            <circle cx="50" cy="50" r="38" fill="none" stroke="{ACCENT}" stroke-width="14" stroke-dasharray="{hvac_dash}"/>
            <circle cx="50" cy="50" r="38" fill="none" stroke="{GREEN}" stroke-width="14" stroke-dasharray="{other_dash}" stroke-dashoffset="{other_offset:.1f}"/>
          </svg>
          <div style="width:100%;margin-top:12px;display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;justify-content:space-between;font-size:12px">
              <span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{ACCENT};margin-right:6px"></span>HVAC</span>
              <span style="color:{TEXT_MUTED}">{hvac_pct:.1f}%</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px">
              <span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{GREEN};margin-right:6px"></span>Other</span>
              <span style="color:{TEXT_MUTED}">{other_pct:.1f}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """


def system_modules_html():
    return f"""
    <style>html,body{{margin:0;padding:0;background:{BG};}}</style>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
      <div style="background:{SURFACE};border:1px solid {BORDER};border-left:3px solid {ACCENT};border-radius:10px;padding:14px">
        <p style="font-size:14px;font-weight:600;margin:0 0 6px;color:{TEXT_PRIMARY}">⚡ Energy intelligence</p>
        <p style="font-size:13px;color:{TEXT_MUTED};margin:0;line-height:1.5">Monitors energy consumption, detects anomalies, and generates efficiency recommendations.</p>
      </div>
      <div style="background:{SURFACE};border:1px solid {BORDER};border-left:3px solid {GREEN};border-radius:10px;padding:14px">
        <p style="font-size:14px;font-weight:600;margin:0 0 6px;color:{TEXT_PRIMARY}">🔧 Predictive maintenance</p>
        <p style="font-size:13px;color:{TEXT_MUTED};margin:0;line-height:1.5">Monitors asset health, calculates equipment health scores, predicts maintenance requirements, and generates alerts.</p>
      </div>
    </div>
    """


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

    rail_col, nav_col = st.columns([1, 9])

    with rail_col:
        st.markdown('<div class="side-rail"></div>', unsafe_allow_html=True)

    with nav_col:

        st.markdown(f"""
        <div class="nav-brand">
            <div class="logo">F</div>
            <div>
                <p class="title">FacilityOps AI</p>
                <p class="subtitle">AGENTIC BUILDING INTELLIGENCE</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### Main menu")

        for nav_item in NAV_PAGES:
            is_active = st.session_state.page == nav_item
            if st.button(
                nav_item,
                key=f"nav_{nav_item}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.page = nav_item

        st.divider()

        st.markdown("##### Facility")
        facility = st.selectbox(
            "Active Location",
            [
                "Headquarters • Building A",
                "Corporate Office • Building B",
                "University Campus"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown("##### Agent status")
        st.success("🟢 Energy Agent Active")
        st.success("🟢 Maintenance Agent Active")

        st.markdown("##### System status")
        st.success("● All Systems Operational")
        st.caption("Data source: Utility + IoT + Asset Monitoring")

        st.divider()

        st.markdown(f"""
        <div class="side-card">
            <p class="label">Signed in as</p>
            <p class="value" style="font-size:14px;">Facility Manager</p>
        </div>
        """, unsafe_allow_html=True)

page = st.session_state.page

# ==========================================
# LOAD ENERGY DATA
# ==========================================

energy_agent = EnergyAgent("data/energy_data.csv")

energy_df = energy_agent.load_data()


# ==========================================
# FACILITY-BASED DATA SIMULATION
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
    energy_df["electricity_kwh"] * multiplier
)

energy_df["hvac_usage"] = (
    energy_df["hvac_usage"] * multiplier
)

energy_agent.data = energy_df


energy_metrics = energy_agent.analyze_energy()
energy_anomalies = energy_agent.detect_energy_anomalies()
energy_df = energy_agent.data
energy_accuracy = energy_agent.evaluate_accuracy()
energy_recommendations = energy_agent.generate_recommendations()


# ==========================================
# LOAD MAINTENANCE DATA
# ==========================================
maintenance_df = __import__("pandas").read_csv("data/asset_data.csv")

# ==========================================
# FACILITY-BASED MAINTENANCE DATA
# ==========================================

maintenance_df = maintenance_df.copy()

if facility == "Headquarters • Building A":
    maintenance_df = maintenance_df.iloc[:5].copy()

elif facility == "Corporate Office • Building B":
    maintenance_df = maintenance_df.iloc[:3].copy()

elif facility == "University Campus":
    maintenance_df = maintenance_df.copy()

maintenance_agent = MaintenanceAgent(maintenance_df)
maintenance_results = maintenance_agent.analyze_assets()


# ==========================================
# OVERVIEW PAGE
# ==========================================
if page == "🏠 Overview":

    st.title("Facility Operations Overview")
    st.caption(f"Centralized AI-powered building intelligence • {facility}")

    alerts = len(
        maintenance_results[
            maintenance_results["maintenance_alert"] == "ALERT"
        ]
    )

    hvac_total = energy_df["hvac_usage"].sum()
    electricity_total = energy_df["electricity_kwh"].sum()
    hvac_pct = (hvac_total / electricity_total * 100) if electricity_total else 0
    other_pct = 100 - hvac_pct

    components.html(
        overview_dashboard_html(
            energy_records=len(energy_df),
            energy_anom_count=len(energy_anomalies),
            assets_monitored=maintenance_results["asset_id"].nunique(),
            maintenance_alerts=alerts,
            electricity_series=energy_df["electricity_kwh"],
            hvac_pct=hvac_pct,
            other_pct=other_pct,
        ),
        height=380,
        scrolling=False
    )

    st.subheader("System modules")

    components.html(system_modules_html(), height=140, scrolling=False)


# ==========================================
# ENERGY INTELLIGENCE PAGE
# ==========================================
elif page == "⚡ Energy Intelligence":

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

    st.subheader("🤖 Energy Agent Overview")

    agent_col1, agent_col2, agent_col3 = st.columns(3)

    with agent_col1:
        st.metric("Records Monitored", len(energy_df))

    with agent_col2:
        st.metric("Anomalies Detected", len(energy_anomalies))

    with agent_col3:
        st.metric("Agent Status", "ACTIVE")

    st.divider()

    st.subheader("Energy Performance")

    c1, c2, c3, c4 = st.columns(4)

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

    st.subheader("📈 Energy Consumption Trend")

    fig1 = px.line(
        energy_df,
        x="timestamp",
        y="electricity_kwh",
        title="Hourly Electricity Consumption",
        color_discrete_sequence=[ACCENT]
    )
    fig1 = chart_theme(fig1)

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🔍 AI Anomaly Detection")

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
        title="Electricity Consumption vs Facility Occupancy",
        color_discrete_sequence=[ACCENT, RED, AMBER, GREEN]
    )
    fig2 = chart_theme(fig2)

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("⚠ Critical Energy Alerts")

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
        st.success("No anomalies detected.")

    st.divider()

    st.subheader("💡 AI Energy Recommendations")

    for recommendation in energy_recommendations:
        st.info("🤖 " + recommendation)


# ==========================================
# MAINTENANCE PAGE
# ==========================================
elif page == "🔧 Maintenance":

    st.title("Predictive Maintenance")
    st.caption(
        f"AI-powered equipment health monitoring • {facility}"
    )

    st.divider()

    st.subheader("🔧 Maintenance Agent Overview")

    total_assets = maintenance_results["asset_id"].nunique()

    critical_assets = len(
        maintenance_results[
            maintenance_results["maintenance_prediction"]
            == "Immediate Maintenance"
        ]
    )

    maintenance_required = len(
        maintenance_results[
            maintenance_results["maintenance_prediction"]
            == "Maintenance Required"
        ]
    )

    avg_health = maintenance_results["health_score"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Assets Monitored", total_assets)

    with c2:
        st.metric("Average Health Score", f"{avg_health:.1f}/100")

    with c3:
        st.metric("Critical Cases", critical_assets)

    with c4:
        st.metric("Maintenance Required", maintenance_required)

    st.divider()

    st.subheader("❤️ Equipment Health Scores")

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
        title="Equipment Health Assessment",
        color_discrete_sequence=[ACCENT, AMBER, RED, GREEN]
    )

    fig_health.update_layout(
        xaxis_title="Equipment",
        yaxis_title="Health Score (0-100)"
    )
    fig_health = chart_theme(fig_health)

    st.plotly_chart(fig_health, use_container_width=True)

    st.divider()

    st.subheader("📈 Asset Condition Monitoring")

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
        title="Temperature vs Vibration Analysis",
        color_discrete_sequence=[ACCENT, AMBER, RED, GREEN]
    )
    fig_condition = chart_theme(fig_condition)

    st.plotly_chart(fig_condition, use_container_width=True)

    st.divider()

    st.subheader("⚠ Maintenance Alerts")

    alert_data = maintenance_results[
        maintenance_results["maintenance_alert"] == "ALERT"
    ]

    if len(alert_data) > 0:

        st.warning(
            f"{len(alert_data)} asset records require maintenance attention."
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
        st.success("No maintenance alerts generated.")

    st.divider()

    st.subheader("🗄️ Asset Monitoring Data")

    with st.expander("Click to View Complete Asset Dataset"):

        st.dataframe(
            maintenance_results,
            use_container_width=True
        )


# ==========================================
# OTHER MODULES
# ==========================================
else:

    st.title(page)
    st.info(
        "This module will be implemented in a future milestone."
    )


# ==========================================
# FOOTER
# ==========================================
st.divider()

st.caption(
    "Agentic FacilityOps AI • Milestone 1 & 2 • "
    "Energy Intelligence + Predictive Maintenance"
)
