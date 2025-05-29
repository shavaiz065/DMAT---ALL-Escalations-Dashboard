import streamlit as st

# Set page config (must be the first Streamlit command)
st.set_page_config(
    page_title="DMAT - TA/Census Escalations Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': 'https://example.com/bug',
        'About': "# DMAT TA/Census Escalations Dashboard\n\nWelcome to the DMAT TA/Census Escalations Dashboard."
    }
)

# Custom CSS for styling and sidebar modification
st.markdown("""
<style>
    /* General styling */
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom sidebar nav styling */
    [data-testid="stSidebarNav"] {
        padding-top: 0;
    }
    
    /* Custom welcome message styling */
    .welcome-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2E4374;
        padding: 0.75rem 1rem;
        margin: 0;
        background: linear-gradient(to right, rgba(46, 67, 116, 0.1), transparent);
    }
    
    /* Separator styling */
    .sidebar-separator {
        margin: 0.5rem 0;
        border: 0;
        border-top: 1px solid rgba(49, 51, 63, 0.1);
    }
    
    /* Style navigation buttons to look like menu items */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: transparent;
        color: #262730;
        border: none;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
        border-radius: 4px;
        font-weight: normal;
        box-shadow: none;
    }
    
    .stButton > button:hover {
        background-color: rgba(151, 166, 195, 0.1);
        color: #2E4374;
        border: none;
        box-shadow: none;
    }
    
    /* Remove button styling */
    .stButton > button::after {
        display: none;
    }
    
    .stButton > button:active {
        transform: none;
        background-color: rgba(151, 166, 195, 0.2);
        color: #2E4374;
        font-weight: 500;
        border: none;
        box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

import os
import json
import base64
from PIL import Image

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None
    st.session_state["role"] = None

if 'theme' not in st.session_state:
    st.session_state['theme'] = "Default"

# Custom function to create sidebar with welcome message at top
def create_custom_sidebar():
    if st.session_state.get("authenticated"):
        # Add welcome message at the very top
        st.sidebar.markdown(f"<div class='welcome-header'>Welcome, {st.session_state.get('username', 'User')}</div>", unsafe_allow_html=True)
        
        # Add a separator
        st.sidebar.markdown("<hr class='sidebar-separator'>", unsafe_allow_html=True)
        
        # Navigation links
        st.sidebar.page_link("app.py", label="Home", icon="🏠")
        st.sidebar.page_link("pages/01_Escalations_Dashboard.py", label="TA/Census Escalations Dashboard", icon="📈")
        st.sidebar.page_link("pages/02_Deductions_Escalations.py", label="Deductions Escalations", icon="📊")

# File to store credentials
CREDENTIALS_FILE = "credentials.json"

# Load credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as file:
                data = json.load(file)
                if "admin" in data and "DMAT" in data:
                    return data
        except json.JSONDecodeError:
            pass

    default_creds = {
        "admin": {"username": "admin", "password": "dmat123461"},
        "DMAT": {"username": "DMAT", "password": "payactiv123461"}
    }
    save_credentials(default_creds)
    return default_creds

# Save credentials
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

# Define themes
THEMES = {
    "Default": {
        "primary_color": "#1E88E5",
        "background_color": "#FFFFFF",
        "text_color": "#424242",
        "accent_color": "#FFC107",
        "secondary_color": "#4CAF50",
        "font": "sans-serif"
    },
    "Dark": {
        "primary_color": "#2962FF",
        "background_color": "#121212",
        "text_color": "#E0E0E0",
        "accent_color": "#FF6D00",
        "secondary_color": "#00C853",
        "font": "sans-serif"
    },
    "Corporate": {
        "primary_color": "#0D47A1",
        "background_color": "#F5F5F5",
        "text_color": "#212121",
        "accent_color": "#E65100",
        "secondary_color": "#2E7D32",
        "font": "serif"
    }
}

# Apply theme
def apply_theme(theme_name):
    if theme_name not in THEMES:
        theme_name = "Default"
    
    theme = THEMES[theme_name]
    
    # Apply CSS with the selected theme
    st.markdown(f"""
    <style>
        /* Global Styles */
        .stApp {{
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
            font-family: {theme["font"]};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme["primary_color"]};
            font-family: {theme["font"]};
        }}
        
        /* Main title */
        .main-title {{
            color: {theme["primary_color"]};
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
            padding: 1.5rem 1rem;
            border-bottom: 2px solid {theme["accent_color"]};
            background: linear-gradient(90deg, {theme["primary_color"]}10, {theme["primary_color"]}25, {theme["primary_color"]}10);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        
        /* Sub titles */
        .sub-title {{
            color: {theme["primary_color"]};
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {theme["accent_color"]}40;
        }}
        
        /* Dashboard cards */
        .dashboard-card {{
            background: linear-gradient(145deg, {theme["background_color"]}, {theme["primary_color"]}08);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border: 1px solid {theme["primary_color"]}15;
            margin-bottom: 1.5rem;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
            border-color: {theme["primary_color"]}30;
        }}
        
        .dashboard-card-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: {theme["primary_color"]};
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .dashboard-card-description {{
            color: {theme["text_color"]};
            margin-bottom: 1.8rem;
            flex-grow: 1;
            font-size: 1.1rem;
            line-height: 1.6;
        }}
        
        .dashboard-card-link {{
            display: inline-block;
            background-color: {theme["primary_color"]};
            color: white;
            padding: 0.7rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px {theme["primary_color"]}40;
            width: 100%;
        }}
        
        .dashboard-card-link:hover {{
            background-color: {theme["accent_color"]};
            box-shadow: 0 6px 12px {theme["accent_color"]}40;
            transform: translateY(-2px);
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: {theme["primary_color"]};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px {theme["primary_color"]}30;
        }}
        
        .stButton button:hover {{
            background-color: {theme["accent_color"]};
            color: white;
            box-shadow: 0 6px 12px {theme["accent_color"]}30;
            transform: translateY(-2px);
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: {theme["primary_color"]}15;
        }}
        
        /* Section styling */
        .section {{
            background-color: {theme["background_color"]};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid {theme["primary_color"]}15;
        }}
        
        /* Feature list */
        .feature-list {{
            list-style-type: none;
            padding-left: 1rem;
        }}
        
        .feature-list li {{
            position: relative;
            padding-left: 1.8rem;
            margin-bottom: 0.8rem;
            line-height: 1.6;
        }}
        
        .feature-list li:before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: {theme["secondary_color"]};
            font-weight: bold;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 1.5rem;
            margin-top: 3rem;
            border-top: 1px solid {theme["primary_color"]}20;
            color: {theme["text_color"]}99;
            font-size: 0.9rem;
        }}
        
        /* Login form */
        .login-container {{
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            background-color: {theme["background_color"]};
            border: 1px solid {theme["primary_color"]}15;
        }}
        
        /* Logo container */
        .logo-container {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .logo-image {{
            max-width: 200px;
            margin: 0 auto;
        }}
        
        /* Welcome message */
        .welcome-message {{
            background-color: {theme["primary_color"]}10;
            border-left: 4px solid {theme["primary_color"]};
            padding: 1rem;
            margin-bottom: 2rem;
            border-radius: 0 8px 8px 0;
        }}
        
        /* Data tables */
        .dataframe {{
            border-collapse: collapse;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        
        .dataframe th {{
            background-color: {theme["primary_color"]};
            color: white;
            text-align: left;
            padding: 0.8rem;
        }}
        
        .dataframe td {{
            padding: 0.8rem;
            border-top: 1px solid {theme["primary_color"]}15;
        }}
        
        .dataframe tr:nth-child(even) {{
            background-color: {theme["primary_color"]}05;
        }}
        
        .dataframe tr:hover {{
            background-color: {theme["primary_color"]}10;
        }}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 3rem;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0 0;
            color: {theme["text_color"]};
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-bottom: 3px solid transparent;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: transparent;
            color: {theme["primary_color"]};
            border-bottom-color: {theme["primary_color"]};
        }}
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            color: {theme["primary_color"]};
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: 1rem;
            font-weight: 600;
        }}
        
        /* Alerts */
        .stAlert {{
            border-radius: 8px;
            border: none;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        /* Tooltips */
        .tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 200px;
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
            text-align: center;
            border-radius: 6px;
            padding: 0.8rem;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid {theme["primary_color"]}20;
        }}
        
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    """, unsafe_allow_html=True)

# Function to encode image as base64
def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Login function
def login():
    # Apply background
    background_style = get_background_style()
    st.markdown(background_style, unsafe_allow_html=True)
    
    # Center the login form with enhanced professional styling
    st.markdown("""
    <style>
        /* Page container */
        .block-container {
            max-width: 1000px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        
        /* Main container - transparent */
        .login-container {
            background: transparent;
            padding: 2.5rem;
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Title card styling */
        .title-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            padding: 20px 30px;
            margin: 0 auto 30px auto;
            width: 90%;
            max-width: 320px;
            text-align: center;
            border: 1px solid rgba(230, 230, 230, 0.7);
            animation: slideDown 0.5s ease-out;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Title styling - matching login button color */
        .title-text {
            background: linear-gradient(to right, #2E4374, #4B6BFB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0;
            letter-spacing: 0.02em;
        }
        
        /* Label styling */
        .stTextInput > label {
            font-weight: 500;
            color: #2E4374;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            margin-bottom: 5px;
            animation: fadeIn 0.8s ease-out;
        }
        
        /* Input fields styling */
        .stTextInput > div > div > input {
            background-color: white;
            border: 1px solid #E2E8F0;
            padding: 0.9rem 1rem;
            font-size: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease;
            animation: fadeIn 0.8s ease-out;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4B6BFB;
            box-shadow: 0 0 0 3px rgba(75, 107, 251, 0.2);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(to right, #2E4374, #4B6BFB);
            color: white;
            border: none;
            padding: 0.9rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            margin-top: 1.2rem;
            box-shadow: 0 4px 10px rgba(75, 107, 251, 0.2);
            letter-spacing: 0.03em;
            animation: fadeIn 1s ease-out;
        }
        
        .stButton > button:hover {
            background: linear-gradient(to right, #263366, #3A5AE5);
            box-shadow: 0 6px 15px rgba(75, 107, 251, 0.3);
            transform: translateY(-2px);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 3px 8px rgba(75, 107, 251, 0.25);
        }
        
        /* Error message styling */
        .error-message {
            color: #DC2626;
            background-color: rgba(254, 226, 226, 0.7);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            margin-top: 1rem;
            font-size: 0.9rem;
            text-align: center;
            border-left: 3px solid #DC2626;
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }
        
        @keyframes shake {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
            40%, 60% { transform: translate3d(3px, 0, 0); }
        }
        
        /* Password visibility toggle */
        button[data-testid="passwordVisibilityToggle"] {
            color: #4B6BFB;
            opacity: 0.7;
            transition: all 0.2s ease;
        }
        
        button[data-testid="passwordVisibilityToggle"]:hover {
            opacity: 1;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .login-container {
                padding: 2rem 1.5rem;
                margin: 0 1rem;
            }
            
            .title-card {
                width: 100%;
                margin-bottom: 25px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login container
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Professional title card
        st.markdown("""
        <div class="title-card">
            <h2 class="title-text">DMAT TA/Census Escalations Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        # Error message placeholder
        error_placeholder = st.empty()
        
        # Login button
        if st.button("Login"):
            credentials = load_credentials()
            authenticated = False
            
            for role, cred in credentials.items():
                if username.lower() == cred["username"].lower() and password == cred["password"]:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = role
                    authenticated = True
                    st.rerun()
            
            if not authenticated:
                error_placeholder.markdown("""
                <div class="error-message">
                    <strong>Login Failed!</strong> Invalid username or password.
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None
    st.session_state["role"] = None

# Check if user is authenticated
if not st.session_state["authenticated"]:
    login()
else:
    # Apply the current theme
    apply_theme(st.session_state['theme'])
    
    # Create custom sidebar with welcome message at top
    create_custom_sidebar()
    
    # Add settings section to sidebar
    with st.sidebar:
        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Settings section
        st.markdown("### Settings")
        selected_theme = st.selectbox("Select Theme", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state['theme']))
        
        if selected_theme != st.session_state['theme']:
            st.session_state['theme'] = selected_theme
            apply_theme(selected_theme)
            st.rerun()
        
        # Logout button
        st.markdown("")
        if st.button("Logout", key="logout_button"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["role"] = None
            st.rerun()
    
    # Main content
    st.markdown("<h1 class='main-title'>DMAT TA/Census Escalations Dashboard</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="section">
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Welcome to the DMAT TA/Census Escalations Dashboard, a comprehensive tool designed to monitor, analyze, and manage TA and Census escalations. 
            This dashboard provides real-time insights, trend analysis, and detailed reporting capabilities to help teams identify issues, track resolution progress, and improve operational efficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard cards
    st.markdown("<h2 class='sub-title'>Available Dashboards</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div>
                <h3 class="dashboard-card-title">📊 TA & Census Escalations</h3>
                <p class="dashboard-card-description">
                    Monitor and analyze Time & Attendance and Census escalations with detailed breakdowns by category, account, and resolution status. Track trends over time and identify patterns to improve response times.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div>
                <h3 class="dashboard-card-title">💰 Deductions Escalations</h3>
                <p class="dashboard-card-description">
                    Track deduction-related escalations with comprehensive analysis by provider, method, and employer. Monitor failed transactions, analyze root causes, and optimize the deduction process.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 class='sub-title'>Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section">
            <h3>TA & Census Escalations Dashboard</h3>
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
        <div class="section">
            <h3>Deductions Escalations Dashboard</h3>
            <ul class="feature-list">
                <li>Precise tracking of deduction amounts and failure rates</li>
                <li>Multi-dimensional analysis by provider, method, and employer</li>
                <li>Detailed failure analysis with root cause identification</li>
                <li>Time-based trend analysis with forecasting capabilities</li>
                <li>Customizable data explorer with search functionality</li>
                <li>Data export in multiple formats (CSV, Excel)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Removed Getting Started section
    
    # System requirements
    st.markdown("<h2 class='sub-title'>System Information</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section">
            <h3>Technical Specifications</h3>
            <ul class="feature-list">
                <li>Built with Streamlit and Python</li>
                <li>Interactive data visualization with Plotly</li>
                <li>Responsive design for all screen sizes</li>
                <li>Secure authentication system</li>
                <li>Customizable themes and appearance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section">
            <h3>Support Information</h3>
            <ul class="feature-list">
                <li>Version: 1.2.0 (May 2025)</li>
                <li>Last Updated: May 14, 2025</li>
                <li>Developed by: DMAT Development Team</li>
                <li>Contact: sbutt@payactiv.com</li>
                <li>Documentation: Available in Help section</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 0.5rem; font-weight: 500;">DMAT TA/Census Escalations Dashboard</div>
        <div>© Shavaiz Zia Butt | Version 1.2.0 | All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)
