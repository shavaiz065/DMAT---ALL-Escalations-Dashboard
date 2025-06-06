import streamlit as st

# Set page config
st.set_page_config(
    page_title="DMAT - Deductions Management & Analytics Tool",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for light theme with modern styling
st.markdown("""
<style>
    /* Main theme colors and fonts */
    :root {
        --background-color: #f8f9fa;
        --card-bg: #ffffff;
        --primary-color: #1565c0;
        --text-color: #2c3e50;
        --text-muted: #6c757d;
        --border-color: #e9ecef;
    }

    /* Global styles */
    .stApp {
        background: var(--background-color);
    }

    .main > div {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    p, span, div {
        color: var(--text-color);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    /* Card styles */
    .dashboard-card {
        background: var(--card-bg);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .dashboard-card h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .dashboard-card h4 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .dashboard-card p {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        padding: 1rem;
    }

    /* Headers */
    .stMarkdown h1 {
        font-size: 2.25rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: var(--text-color);
    }

    .stMarkdown h2 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        color: var(--text-color);
    }

    /* Lists */
    ul {
        list-style-type: none;
        padding-left: 0;
        margin: 0;
    }

    li {
        margin-bottom: 0.75rem;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    li:before {
        content: '•';
        color: var(--primary-color);
        font-weight: bold;
    }

    /* Custom button styles */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.75rem 1.25rem;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.875rem;
    }

    .stButton > button:hover {
        background-color: #1976d2;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Streamlit elements customization */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        transition: all 0.2s;
    }

    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:hover {
        border-color: var(--primary-color);
    }

    .stSelectbox > div > div:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(21, 101, 192, 0.1);
    }

    /* Footer */
    footer {
        border-top: 1px solid var(--border-color);
        padding-top: 2rem;
        margin-top: 3rem;
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication status
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Please authenticate first")
    st.stop()

# Welcome
# Main title
st.markdown("<h1 class='main-title'>DMAT Escalations Dashboard</h1>", unsafe_allow_html=True)

# Welcome text
st.markdown("""
    <div style="color: var(--text-muted); margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
        Welcome to the DMAT Escalations Dashboard, a comprehensive tool designed to monitor, analyze, and manage TA and Census escalations. 
        This dashboard provides real-time insights, trend analysis, and detailed reporting capabilities to help teams identify issues, track resolution progress, and improve operational efficiency.
    </div>
""", unsafe_allow_html=True)

# Feature cards in a grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📈 Deductions Escalations</h3>
            <p>Track and manage your deductions escalations efficiently. Monitor status, 
            assign priorities, and follow up on critical cases.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dashboard-card">
            <h3>🔍 Deductions Insights</h3>
            <p>Get detailed insights into your deductions data with powerful analytics 
            and visualizations. Identify patterns and trends.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="dashboard-card">
            <h3>🎯 Deductions Forecasting</h3>
            <p>Predict future deduction trends using advanced analytics. Plan ahead 
            with data-driven forecasting.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="section">
            <h3>Deductions Escalations Dashboard</h3>
            <ul class="feature-list">
            </ul>
        </div>
    """, unsafe_allow_html=True)

# System
# Available Dashboards section
st.markdown("<h2 class='sub-title'>Available Dashboards</h2>", unsafe_allow_html=True)

# Dashboard cards in 2 columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📈 TA & Census Escalations</h3>
            <p>Monitor and analyze Time & Attendance and Census escalations with detailed breakdowns by category, account, and workflow status. 
            Track trends over time and identify patterns to improve process flow.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📊 Deductions Escalations</h3>
            <p>Track deductions-related insights with comprehensive analysis by process, metrics, and workflow. Monitor failed transactions, 
            payment root causes and optimize the collection process.</p>
        </div>
    """, unsafe_allow_html=True)

# Key Features section
st.markdown("<h2 class='sub-title'>Key Features</h2>", unsafe_allow_html=True)

# Features in 2 columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📊 TA & Census Escalations</h3>
            <ul class="feature-list">
                <li>Real-time monitoring of escalation volume and trends</li>
                <li>Interactive breakdown by categories, modes, and accounts</li>
                <li>Advanced anomaly detection with AI-powered insights</li>
                <li>Comprehensive data exploration with custom filters</li>
                <li>Automated recommendations for process improvement</li>
                <li>Export capabilities for reports and presentations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dashboard-card">
            <h3>💰 Deductions Escalations</h3>
            <ul class="feature-list">
                <li>Real-time tracking of deductions assignments and failure rates</li>
                <li>Multi-dimensional analysis by product, metrics, and workflow</li>
                <li>Deep and failure analysis with root cause identification</li>
                <li>Time-based trend analysis with forecasting capabilities</li>
                <li>Customizable data exports with reports functionality</li>
                <li>Data export to multiple formats (CSV, Excel)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <footer>
        2025 DMAT Escalations Dashboard | Version 1.2.0
        <br>
        For support, please contact your system administrator
    </footer>
""", unsafe_allow_html=True)
