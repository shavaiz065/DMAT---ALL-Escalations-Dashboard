Home.py:import streamlit as st
Home.py:
Home.py:# Set page config (must be the first Streamlit command)
Home.py:st.set_page_config(layout="wide", page_title="DMAT - Escalations Dashboard", page_icon="≡ƒôè")
Home.py:
Home.py:import os
Home.py:import json
Home.py:import base64
Home.py:from PIL import Image
Home.py:
Home.py:# Initialize session state
Home.py:if "authenticated" not in st.session_state:
Home.py:    st.session_state["authenticated"] = False
Home.py:
Home.py:if "username" not in st.session_state:
Home.py:    st.session_state["username"] = None
Home.py:    st.session_state["role"] = None
Home.py:
Home.py:if 'theme' not in st.session_state:
Home.py:    st.session_state['theme'] = "Default"
Home.py:
Home.py:# Import the background image module
Home.py:from assets.background import get_background_style
Home.py:
Home.py:# File to store credentials
Home.py:CREDENTIALS_FILE = "credentials.json"
Home.py:
Home.py:# Load credentials
Home.py:def load_credentials():
Home.py:    if os.path.exists(CREDENTIALS_FILE):
Home.py:        try:
Home.py:            with open(CREDENTIALS_FILE, "r") as file:
Home.py:                data = json.load(file)
Home.py:                if "admin" in data and "DMAT" in data:
Home.py:                    return data
Home.py:        except json.JSONDecodeError:
Home.py:            pass
Home.py:
Home.py:    default_creds = {
Home.py:        "admin": {"username": "admin", "password": "dmat123461"},
Home.py:        "DMAT": {"username": "DMAT", "password": "payactiv123461"}
Home.py:    }
Home.py:    save_credentials(default_creds)
Home.py:    return default_creds
Home.py:
Home.py:# Save credentials
Home.py:def save_credentials(credentials):
Home.py:    with open(CREDENTIALS_FILE, "w") as file:
Home.py:        json.dump(credentials, file, indent=4)
Home.py:
Home.py:# Define themes
Home.py:THEMES = {
Home.py:    "Default": {
Home.py:        "primary_color": "#1E88E5",
Home.py:        "background_color": "#FFFFFF",
Home.py:        "text_color": "#424242",
Home.py:        "accent_color": "#FFC107",
Home.py:        "secondary_color": "#4CAF50",
Home.py:        "font": "sans-serif"
Home.py:    },
Home.py:    "Dark": {
Home.py:        "primary_color": "#2962FF",
Home.py:        "background_color": "#121212",
Home.py:        "text_color": "#E0E0E0",
Home.py:        "accent_color": "#FF6D00",
Home.py:        "secondary_color": "#00C853",
Home.py:        "font": "sans-serif"
Home.py:    },
Home.py:    "Corporate": {
Home.py:        "primary_color": "#0D47A1",
Home.py:        "background_color": "#F5F5F5",
Home.py:        "text_color": "#212121",
Home.py:        "accent_color": "#E65100",
Home.py:        "secondary_color": "#2E7D32",
Home.py:        "font": "serif"
Home.py:    }
Home.py:}
Home.py:
Home.py:# Apply theme
Home.py:def apply_theme(theme_name):
Home.py:    if theme_name not in THEMES:
Home.py:        theme_name = "Default"
Home.py:    
Home.py:    theme = THEMES[theme_name]
Home.py:    
Home.py:    # Apply CSS with the selected theme
Home.py:    st.markdown(f"""
Home.py:    <style>
Home.py:        /* Global Styles */
Home.py:        .stApp {{
Home.py:            background-color: {theme["background_color"]};
Home.py:            color: {theme["text_color"]};
Home.py:            font-family: {theme["font"]};
Home.py:        }}
Home.py:        
Home.py:        /* Headers */
Home.py:        h1, h2, h3, h4, h5, h6 {{
Home.py:            color: {theme["primary_color"]};
Home.py:            font-family: {theme["font"]};
Home.py:        }}
Home.py:        
Home.py:        /* Main title */
Home.py:        .main-title {{
Home.py:            color: {theme["primary_color"]};
Home.py:            font-size: 2.5rem;
Home.py:            font-weight: 700;
Home.py:            margin-bottom: 1.5rem;
Home.py:            text-align: center;
Home.py:            padding: 1.5rem 1rem;
Home.py:            border-bottom: 2px solid {theme["accent_color"]};
Home.py:            background: linear-gradient(90deg, {theme["primary_color"]}10, {theme["primary_color"]}25, {theme["primary_color"]}10);
Home.py:            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
Home.py:        }}
Home.py:        
Home.py:        /* Sub titles */
Home.py:        .sub-title {{
Home.py:            color: {theme["primary_color"]};
Home.py:            font-size: 1.5rem;
Home.py:            font-weight: 600;
Home.py:            margin-top: 1.5rem;
Home.py:            margin-bottom: 1rem;
Home.py:            padding-bottom: 0.5rem;
Home.py:            border-bottom: 1px solid {theme["accent_color"]}40;
Home.py:        }}
Home.py:        
Home.py:        /* Dashboard cards */
Home.py:        .dashboard-card {{
Home.py:            background: linear-gradient(145deg, {theme["background_color"]}, {theme["primary_color"]}08);
Home.py:            border-radius: 12px;
Home.py:            padding: 2rem;
Home.py:            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
Home.py:            transition: transform 0.3s ease, box-shadow 0.3s ease;
Home.py:            height: 100%;
Home.py:            display: flex;
Home.py:            flex-direction: column;
Home.py:            justify-content: space-between;
Home.py:            border: 1px solid {theme["primary_color"]}15;
Home.py:            margin-bottom: 1.5rem;
Home.py:        }}
Home.py:        
Home.py:        .dashboard-card:hover {{
Home.py:            transform: translateY(-5px);
Home.py:            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
Home.py:            border-color: {theme["primary_color"]}30;
Home.py:        }}
Home.py:        
Home.py:        .dashboard-card-title {{
Home.py:            font-size: 1.8rem;
Home.py:            font-weight: 600;
Home.py:            color: {theme["primary_color"]};
Home.py:            margin-bottom: 1.2rem;
Home.py:            display: flex;
Home.py:            align-items: center;
Home.py:            gap: 0.5rem;
Home.py:        }}
Home.py:        
Home.py:        .dashboard-card-description {{
Home.py:            color: {theme["text_color"]};
Home.py:            margin-bottom: 1.8rem;
Home.py:            flex-grow: 1;
Home.py:            font-size: 1.1rem;
Home.py:            line-height: 1.6;
Home.py:        }}
Home.py:        
Home.py:        .dashboard-card-link {{
Home.py:            display: inline-block;
Home.py:            background-color: {theme["primary_color"]};
Home.py:            color: white;
Home.py:            padding: 0.7rem 1.5rem;
Home.py:            border-radius: 8px;
Home.py:            text-decoration: none;
Home.py:            font-weight: 600;
Home.py:            text-align: center;
Home.py:            transition: all 0.3s ease;
Home.py:            box-shadow: 0 4px 8px {theme["primary_color"]}40;
Home.py:            width: 100%;
Home.py:        }}
Home.py:        
Home.py:        .dashboard-card-link:hover {{
Home.py:            background-color: {theme["accent_color"]};
Home.py:            box-shadow: 0 6px 12px {theme["accent_color"]}40;
Home.py:            transform: translateY(-2px);
Home.py:        }}
Home.py:        
Home.py:        /* Buttons */
Home.py:        .stButton button {{
Home.py:            background-color: {theme["primary_color"]};
Home.py:            color: white;
Home.py:            border: none;
Home.py:            border-radius: 8px;
Home.py:            padding: 0.7rem 1.5rem;
Home.py:            font-weight: 600;
Home.py:            transition: all 0.3s ease;
Home.py:            box-shadow: 0 4px 8px {theme["primary_color"]}30;
Home.py:        }}
Home.py:        
Home.py:        .stButton button:hover {{
Home.py:            background-color: {theme["accent_color"]};
Home.py:            color: white;
Home.py:            box-shadow: 0 6px 12px {theme["accent_color"]}30;
Home.py:            transform: translateY(-2px);
Home.py:        }}
Home.py:        
Home.py:        /* Sidebar */
Home.py:        .css-1d391kg {{
Home.py:            background-color: {theme["primary_color"]}15;
Home.py:        }}
Home.py:        
Home.py:        /* Section styling */
Home.py:        .section {{
Home.py:            background-color: {theme["background_color"]};
Home.py:            border-radius: 12px;
Home.py:            padding: 1.5rem;
Home.py:            margin-bottom: 2rem;
Home.py:            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
Home.py:            border: 1px solid {theme["primary_color"]}15;
Home.py:        }}
Home.py:        
Home.py:        /* Feature list */
Home.py:        .feature-list {{
Home.py:            list-style-type: none;
Home.py:            padding-left: 1rem;
Home.py:        }}
Home.py:        
Home.py:        .feature-list li {{
Home.py:            position: relative;
Home.py:            padding-left: 1.5rem;
Home.py:            margin-bottom: 0.8rem;
Home.py:            line-height: 1.6;
Home.py:        }}
Home.py:        
Home.py:        .feature-list li:before {{
Home.py:            content: '├ó┼ôΓÇ£';
Home.py:            position: absolute;
Home.py:            left: 0;
Home.py:            color: {theme["secondary_color"]};
Home.py:            font-weight: bold;
Home.py:        }}
Home.py:        
Home.py:        /* Stats counter */
Home.py:        .stats-container {{
Home.py:            display: flex;
Home.py:            justify-content: space-around;
Home.py:            margin: 2rem 0;
Home.py:            flex-wrap: wrap;
Home.py:        }}
Home.py:        
Home.py:        .stat-item {{
Home.py:            text-align: center;
Home.py:            padding: 1.5rem;
Home.py:            border-radius: 12px;
Home.py:            background: linear-gradient(145deg, {theme["background_color"]}, {theme["primary_color"]}08);
Home.py:            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
Home.py:            margin: 0.5rem;
Home.py:            min-width: 200px;
Home.py:            border: 1px solid {theme["primary_color"]}15;
Home.py:        }}
Home.py:        
Home.py:        .stat-value {{
Home.py:            font-size: 2.5rem;
Home.py:            font-weight: 700;
Home.py:            color: {theme["primary_color"]};
Home.py:            margin-bottom: 0.5rem;
Home.py:        }}
Home.py:        
Home.py:        .stat-label {{
Home.py:            font-size: 1.1rem;
Home.py:            color: {theme["text_color"]};
Home.py:        }}
Home.py:        
Home.py:        /* Footer */
Home.py:        .footer {{
Home.py:            text-align: center;
Home.py:            padding: 2rem 0;
Home.py:            margin-top: 3rem;
Home.py:            border-top: 1px solid {theme["primary_color"]}20;
Home.py:            color: {theme["text_color"]}80;
Home.py:        }}
Home.py:    </style>
Home.py:    """, unsafe_allow_html=True)
Home.py:
Home.py:# Function to encode image as base64
Home.py:def get_base64(image_path):
Home.py:    with open(image_path, "rb") as image_file:
Home.py:        return base64.b64encode(image_file.read()).decode()
Home.py:
Home.py:# Login function
Home.py:def login():
Home.py:    # Initialize authentication
Home.py:    credentials = load_credentials()
Home.py:    
Home.py:    # Hide the default menu and footer
Home.py:    hide_menu_style = """
Home.py:        <style>
Home.py:        #MainMenu {visibility: hidden;}
Home.py:        footer {visibility: hidden;}
Home.py:        </style>
Home.py:    """
Home.py:    st.markdown(hide_menu_style, unsafe_allow_html=True)
Home.py:    
Home.py:    # Create a centered container for the login form
Home.py:    _, center_col, _ = st.columns([1, 2, 1])
Home.py:    
Home.py:    with center_col:
Home.py:        # Add vertical space at the top
Home.py:        st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
Home.py:        
Home.py:        # Display logo on login page
Home.py:        logo_path = os.path.join(os.path.dirname(__file__), "image", "DMAT.Logo.png")
Home.py:        if os.path.exists(logo_path):
Home.py:            try:
Home.py:                logo_img = Image.open(logo_path)
Home.py:                st.image(logo_img, width=200, use_container_width=False)
Home.py:            except Exception as e:
Home.py:                st.error(f"Error displaying logo: {e}")
Home.py:    
Home.py:    st.markdown("""
Home.py:        <style>
Home.py:            /* Professional Enterprise Dashboard Background */
Home.py:            .stApp {
Home.py:                display: flex;
Home.py:                justify-content: center;
Home.py:                align-items: center;
Home.py:                height: 100vh;
Home.py:                background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
Home.py:                position: relative;
Home.py:                overflow: hidden;
Home.py:            }
Home.py:            
Home.py:            /* Subtle enterprise background elements */
Home.py:            .stApp::before {
Home.py:                content: '';
Home.py:                position: absolute;
Home.py:                top: 0;
Home.py:                left: 0;
Home.py:                right: 0;
Home.py:                bottom: 0;
Home.py:                background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%231E88E5' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
Home.py:                opacity: 0.5;
Home.py:            }
Home.py:            
Home.py:            /* Professional Login Container */
Home.py:            .login-container {
Home.py:                width: 450px;
Home.py:                padding: 2.5rem;
Home.py:                border-radius: 12px;
Home.py:                background: white;
Home.py:                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
Home.py:                text-align: center;
Home.py:                margin: 0 auto;
Home.py:                border: 1px solid #e0e0e0;
Home.py:                position: relative;
Home.py:                z-index: 10;
Home.py:            }
Home.py:            
Home.py:            /* Login form container */
Home.py:            .login-form-container {
Home.py:                text-align: center;
Home.py:                margin-bottom: 1.5rem;
Home.py:            }
Home.py:            
Home.py:            /* Style form elements */
Home.py:            div[data-testid="stForm"] {
Home.py:                background: white;
Home.py:                padding: 2rem;
Home.py:                border-radius: 10px;
Home.py:                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
Home.py:                border: 1px solid #e0e0e0;
Home.py:                max-width: 400px;
Home.py:                margin: 0 auto;
Home.py:            }
Home.py:            
Home.py:            /* Data visualization decorative elements */
Home.py:            .login-container::before {
Home.py:                content: '';
Home.py:                position: absolute;
Home.py:                top: -15px;
Home.py:                right: -15px;
Home.py:                width: 80px;
Home.py:                height: 80px;
Home.py:                border-radius: 50%;
Home.py:                background: linear-gradient(45deg, #1E88E5, #4CAF50);
Home.py:                opacity: 0.2;
Home.py:                z-index: -1;
Home.py:            }
Home.py:            
Home.py:            .login-container::after {
Home.py:                content: '';
Home.py:                position: absolute;
Home.py:                bottom: -10px;
Home.py:                left: -10px;
Home.py:                width: 60px;
Home.py:                height: 60px;
Home.py:                border-radius: 50%;
Home.py:                background: linear-gradient(45deg, #FFC107, #F44336);
Home.py:                opacity: 0.2;
Home.py:                z-index: -1;
Home.py:            }
Home.py:            
Home.py:            /* Company Logo */
Home.py:            .company-logo {
Home.py:                font-size: 3.5rem;
Home.py:                color: #1E88E5;
Home.py:                margin-bottom: 0.5rem;
Home.py:                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
Home.py:            }
Home.py:            
Home.py:            /* Title */
Home.py:            .title {
Home.py:                font-size: 28px;
Home.py:                font-weight: 600;
Home.py:                color: #333333;
Home.py:                margin-bottom: 1rem;
Home.py:            }
Home.py:            
Home.py:            /* Subtitle */
Home.py:            .subtitle {
Home.py:                font-size: 16px;
Home.py:                color: #666666;
Home.py:                margin-bottom: 2rem;
Home.py:            }
Home.py:            
Home.py:            /* Input Labels */
Home.py:            .stTextInput label {
Home.py:                font-size: 16px;
Home.py:                font-weight: 500;
Home.py:                color: #333333;
Home.py:            }
Home.py:            
Home.py:            /* Input Fields */
Home.py:            .stTextInput>div>div>input {
Home.py:                font-size: 16px;
Home.py:                padding: 12px 16px;
Home.py:                border-radius: 8px;
Home.py:                border: 1px solid #dddddd;
Home.py:                background: #ffffff;
Home.py:                color: #333333;
Home.py:                transition: all 0.3s ease;
Home.py:            }
Home.py:            
Home.py:            .stTextInput>div>div>input:focus {
Home.py:                border-color: #1E88E5;
Home.py:                box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
Home.py:            }
Home.py:            
Home.py:            .stTextInput>div>div>input::placeholder {
Home.py:                color: #999999;
Home.py:            }
Home.py:            
Home.py:            /* Login Button */
Home.py:            .stButton>button {
Home.py:                width: 100%;
Home.py:                font-size: 16px;
Home.py:                font-weight: 600;
Home.py:                padding: 12px;
Home.py:                border-radius: 8px;
Home.py:                background: #1E88E5;
Home.py:                color: white;
Home.py:                border: none;
Home.py:                margin-top: 1.5rem;
Home.py:                transition: all 0.3s ease;
Home.py:                box-shadow: 0 4px 6px rgba(30, 136, 229, 0.2);
Home.py:            }
Home.py:            
Home.py:            .stButton>button:hover {
Home.py:                background: #1976D2;
Home.py:                box-shadow: 0 6px 10px rgba(30, 136, 229, 0.3);
Home.py:                transform: translateY(-2px);
Home.py:            }
Home.py:            
Home.py:            /* Error Message */
Home.py:            .error-msg {
Home.py:                color: #e53935;
Home.py:                background: #ffebee;
Home.py:                padding: 12px;
Home.py:                border-radius: 8px;
Home.py:                margin-top: 1rem;
Home.py:                font-weight: 500;
Home.py:                border-left: 4px solid #e53935;
Home.py:                text-align: left;
Home.py:            }
Home.py:            
Home.py:            /* Help Text */
Home.py:            .help-text {
Home.py:                margin-top: 1.5rem;
Home.py:                font-size: 14px;
Home.py:                color: #666666;
Home.py:            }
Home.py:            
Home.py:            /* Version Info */
Home.py:            .version-info {
Home.py:                margin-top: 2rem;
Home.py:                font-size: 12px;
Home.py:                color: #999999;
Home.py:            }
Home.py:            
Home.py:            /* Remove Streamlit Branding */
Home.py:            #MainMenu {visibility: hidden;}
Home.py:            footer {visibility: hidden;}
Home.py:            .viewerBadge_container__1QSob {display: none;}
Home.py:        </style>
Home.py:    """, unsafe_allow_html=True)
Home.py:
Home.py:st.markdown("""
Home.py:    <style>
Home.py:        /* Professional Enterprise Dashboard Background */
Home.py:        .stApp {
Home.py:            display: flex;
Home.py:            justify-content: center;
Home.py:            align-items: center;
Home.py:            height: 100vh;
Home.py:            background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
Home.py:            position: relative;
Home.py:            overflow: hidden;
Home.py:        }
Home.py:        
Home.py:        /* Subtle enterprise background elements */
Home.py:        .stApp::before {
Home.py:            content: '';
Home.py:            position: absolute;
Home.py:            top: 0;
Home.py:            left: 0;
Home.py:            right: 0;
Home.py:            bottom: 0;
Home.py:            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%231E88E5' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
Home.py:            opacity: 0.5;
Home.py:        }
Home.py:        
Home.py:        /* Professional Login Container */
Home.py:        .login-container {
Home.py:            width: 450px;
Home.py:            padding: 2.5rem;
Home.py:            border-radius: 12px;
Home.py:            background: white;
Home.py:            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
Home.py:            text-align: center;
Home.py:            margin: 0 auto;
Home.py:            border: 1px solid #e0e0e0;
Home.py:            position: relative;
Home.py:            z-index: 10;
Home.py:        }
Home.py:        
Home.py:        /* Login form container */
Home.py:        .login-form-container {
Home.py:            text-align: center;
Home.py:            margin-bottom: 1.5rem;
Home.py:        }
Home.py:        
Home.py:        /* Style form elements */
Home.py:        div[data-testid="stForm"] {
Home.py:            background: white;
Home.py:            padding: 2rem;
Home.py:            border-radius: 10px;
Home.py:            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
Home.py:            border: 1px solid #e0e0e0;
Home.py:            max-width: 400px;
Home.py:            margin: 0 auto;
Home.py:        }
Home.py:        
Home.py:        /* Data visualization decorative elements */
Home.py:        .login-container::before {
Home.py:            content: '';
Home.py:            position: absolute;
Home.py:            top: -15px;
Home.py:            right: -15px;
Home.py:            width: 80px;
Home.py:            height: 80px;
Home.py:            border-radius: 50%;
Home.py:            background: linear-gradient(45deg, #1E88E5, #4CAF50);
Home.py:            opacity: 0.2;
Home.py:            z-index: -1;
Home.py:        }
Home.py:        
Home.py:        .login-container::after {
Home.py:            content: '';
Home.py:            position: absolute;
Home.py:            bottom: -10px;
Home.py:            left: -10px;
Home.py:            width: 60px;
Home.py:            height: 60px;
Home.py:            border-radius: 50%;
Home.py:            background: linear-gradient(45deg, #FFC107, #F44336);
Home.py:            opacity: 0.2;
Home.py:            z-index: -1;
Home.py:        }
Home.py:        
Home.py:        /* Company Logo */
Home.py:        .company-logo {
Home.py:            font-size: 3.5rem;
Home.py:            color: #1E88E5;
Home.py:            margin-bottom: 0.5rem;
Home.py:            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
Home.py:        }
Home.py:        
Home.py:        /* Title */
Home.py:        .title {
Home.py:            font-size: 28px;
Home.py:            font-weight: 600;
Home.py:            color: #333333;
Home.py:            margin-bottom: 1rem;
Home.py:        }
Home.py:        
Home.py:        /* Subtitle */
Home.py:        .subtitle {
Home.py:            font-size: 16px;
Home.py:            color: #666666;
Home.py:            margin-bottom: 2rem;
Home.py:        }
Home.py:        
Home.py:        /* Input Labels */
Home.py:        .stTextInput label {
Home.py:            font-size: 16px;
Home.py:            font-weight: 500;
Home.py:            color: #333333;
Home.py:        }
Home.py:        
Home.py:        /* Input Fields */
Home.py:        .stTextInput>div>div>input {
Home.py:            font-size: 16px;
Home.py:            padding: 12px 16px;
Home.py:            border-radius: 8px;
Home.py:            border: 1px solid #dddddd;
Home.py:            background: #ffffff;
Home.py:            color: #333333;
Home.py:            transition: all 0.3s ease;
Home.py:        }
Home.py:        
Home.py:        .stTextInput>div>div>input:focus {
Home.py:            border-color: #1E88E5;
Home.py:            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
Home.py:        }
Home.py:        
Home.py:        .stTextInput>div>div>input::placeholder {
Home.py:            color: #999999;
Home.py:        }
Home.py:        
Home.py:        /* Login Button */
Home.py:        .stButton>button {
Home.py:            width: 100%;
Home.py:            font-size: 16px;
Home.py:            font-weight: 600;
Home.py:            padding: 12px;
Home.py:            border-radius: 8px;
Home.py:            background: #1E88E5;
Home.py:            color: white;
Home.py:            border: none;
Home.py:            margin-top: 1.5rem;
Home.py:            transition: all 0.3s ease;
Home.py:            box-shadow: 0 4px 6px rgba(30, 136, 229, 0.2);
Home.py:        }
Home.py:        
Home.py:        .stButton>button:hover {
Home.py:            background: #1976D2;
Home.py:            box-shadow: 0 6px 10px rgba(30, 136, 229, 0.3);
Home.py:            transform: translateY(-2px);
Home.py:        }
Home.py:        
Home.py:        /* Error Message */
Home.py:        .error-msg {
Home.py:            color: #e53935;
Home.py:            background: #ffebee;
Home.py:            padding: 12px;
Home.py:            border-radius: 8px;
Home.py:            margin-top: 1rem;
Home.py:            font-weight: 500;
Home.py:            border-left: 4px solid #e53935;
Home.py:            text-align: left;
Home.py:        }
Home.py:        
Home.py:        /* Help Text */
Home.py:        .help-text {
Home.py:            margin-top: 1.5rem;
Home.py:            font-size: 14px;
Home.py:            color: #666666;
Home.py:        }
Home.py:        
Home.py:        /* Version Info */
Home.py:        .version-info {
Home.py:            margin-top: 2rem;
Home.py:            font-size: 12px;
Home.py:            color: #999999;
Home.py:        }
Home.py:        
Home.py:        /* Remove Streamlit Branding */
Home.py:        #MainMenu {visibility: hidden;}
Home.py:        footer {visibility: hidden;}
Home.py:        .viewerBadge_container__1QSob {display: none;}
Home.py:    </style>
Home.py:""", unsafe_allow_html=True)
Home.py:
Home.py:# Create centered container
Home.py:st.markdown('<div class="login-container">', unsafe_allow_html=True)
Home.py:
Home.py:# Logo and title
Home.py:st.markdown('<div class="company-logo">├░┼╕ΓÇ£┼á</div>', unsafe_allow_html=True)
Home.py:st.markdown("""
Home.py:<div class="login-form-container">
Home.py:    <h2 class="title">DMAT Escalations Dashboard</h2>
Home.py:    <p class="subtitle">Sign in to access your dashboard</p>
Home.py:</div>
Home.py:""", unsafe_allow_html=True)
Home.py:
Home.py:# Create login form with better styling
Home.py:with st.form("login_form", clear_on_submit=False):
Home.py:    username = st.text_input("Username", placeholder="Enter your username")
Home.py:    password = st.text_input("Password", type="password", placeholder="Enter your password")
Home.py:    
Home.py:    # Center the login button
Home.py:    cols = st.columns([1, 2, 1])
Home.py:    with cols[1]:
Home.py:        login_button = st.form_submit_button("Sign In", use_container_width=True)
Home.py:
Home.py:    # Check credentials
Home.py:    valid_login = False
Home.py:    creds = load_credentials()
Home.py:    for role, cred in creds.items():
Home.py:        if username == cred["username"] and password == cred["password"]:
Home.py:            st.session_state["authenticated"] = True
Home.py:            st.session_state["role"] = role
Home.py:            valid_login = True
Home.py:            st.rerun()  # Refresh to show the main dashboard
Home.py:            break
Home.py:
Home.py:        if not valid_login:
Home.py:            st.markdown('<div class="error-msg"><strong>Access Denied</strong><br>The username or password you entered is incorrect. Please try again.</div>', unsafe_allow_html=True)
Home.py:
Home.py:    st.markdown('<p class="help-text">Having trouble signing in? Contact your system administrator.</p>', unsafe_allow_html=True)
Home.py:    st.markdown('<p class="version-info">DMAT Escalations Dashboard v1.2.0</p>', unsafe_allow_html=True)
Home.py:    st.markdown('</div>', unsafe_allow_html=True)
Home.py:
Home.py:# Set page config
Home.py:st.set_page_config(layout="wide", page_title="DMAT - Escalations Dashboard", page_icon="├░┼╕ΓÇ£┼á")
Home.py:
Home.py:# Initialize session state
Home.py:if "authenticated" not in st.session_state:
Home.py:    st.session_state["authenticated"] = False
Home.py:
Home.py:if "username" not in st.session_state:
Home.py:    st.session_state["username"] = None
Home.py:    st.session_state["role"] = None
Home.py:
Home.py:if 'theme' not in st.session_state:
Home.py:    st.session_state['theme'] = "Default"
Home.py:
Home.py:# Initialize authentication
Home.py:credentials = load_credentials()
Home.py:
Home.py:# Load the logo as base64
Home.py:logo_path = os.path.join(os.path.dirname(__file__), "image", "DMAT.Logo.png")
Home.py:LOGO_BASE64 = ""
Home.py:if os.path.exists(logo_path):
Home.py:    try:
Home.py:        LOGO_BASE64 = get_base64(logo_path)
Home.py:    except Exception as e:
Home.py:        st.error(f"Error loading logo: {e}")
Home.py:
Home.py:# Check authentication
Home.py:if not st.session_state["authenticated"]:
Home.py:    login()
Home.py:else:
Home.py:    # Apply the current theme
Home.py:    apply_theme(st.session_state['theme'])
Home.py:    
Home.py:    # Display the logo directly in the page
Home.py:    if os.path.exists(logo_path):
Home.py:        # Create more columns for better centering
Home.py:        col1, col2, col3 = st.columns([1, 1, 1])
Home.py:        with col2:
Home.py:            # Add vertical space before logo
Home.py:            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
Home.py:            # Use Streamlit's image display instead of HTML
Home.py:            try:
Home.py:                logo_img = Image.open(logo_path)
Home.py:                st.image(logo_img, width=300, use_container_width=False)
Home.py:            except Exception as e:
Home.py:                st.error(f"Error displaying logo: {e}")
Home.py:    
Home.py:    # Apply a data analytics background directly
Home.py:    # No need to use logo_base64 for background as we're displaying the logo directly
Home.py:    st.markdown(f"""
Home.py:    <style>
Home.py:    .stApp {{
Home.py:        background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
Home.py:        position: relative;
Home.py:    }}
Home.py:    
Home.py:    /* Professional subtle background pattern */
Home.py:    .stApp::before {{
Home.py:        content: '';
Home.py:        position: absolute;
Home.py:        top: 0;
Home.py:        left: 0;
Home.py:        right: 0;
Home.py:        bottom: 0;
Home.py:        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%231E88E5' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
Home.py:        opacity: 0.5;
Home.py:        z-index: -1;
Home.py:    }}
Home.py:    
Home.py:    /* Subtle pattern background instead of logo watermark */
Home.py:    body::before {{
Home.py:        content: '';
Home.py:        position: fixed;
Home.py:        top: 0;
Home.py:        left: 0;
Home.py:        width: 100%;
Home.py:        height: 100%;
Home.py:        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%231E88E5' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
Home.py:        opacity: 0.5;
Home.py:        z-index: -1;
Home.py:        pointer-events: none;
Home.py:    }}
Home.py:    
Home.py:    /* Add a subtle gradient accent at the top */
Home.py:    .stApp .stHeader {{
Home.py:        position: relative;
Home.py:    }}
Home.py:    
Home.py:    .stApp .stHeader::before {{
Home.py:        content: '';
Home.py:        position: absolute;
Home.py:        top: 0;
Home.py:        left: 0;
Home.py:        right: 0;
Home.py:        height: 4px;
Home.py:        background: linear-gradient(to right, #1E88E5, #4CAF50, #FFC107, #F44336);
Home.py:        z-index: 1000;
Home.py:    }}
Home.py:    
Home.py:    /* Add data visualization styling to cards */
Home.py:    .dashboard-card {{
Home.py:        position: relative;
Home.py:        overflow: hidden;
Home.py:        background: white;
Home.py:        transition: all 0.3s ease;
Home.py:        border: 1px solid rgba(30, 136, 229, 0.2);
Home.py:    }}
Home.py:    
Home.py:    .dashboard-card:hover {{
Home.py:        transform: translateY(-5px);
Home.py:        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
Home.py:        border-color: rgba(30, 136, 229, 0.4);
Home.py:    }}
Home.py:    
Home.py:    /* Add data visualization decorative elements */
Home.py:    .dashboard-card::before {{
Home.py:        content: '';
Home.py:        position: absolute;
Home.py:        top: 0;
Home.py:        right: 0;
Home.py:        width: 100px;
Home.py:        height: 100px;
Home.py:        background-image: 
Home.py:            radial-gradient(circle at 70% 30%, rgba(30, 136, 229, 0.1) 0%, rgba(30, 136, 229, 0.1) 40%, transparent 40%),
Home.py:            radial-gradient(circle at 30% 70%, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.1) 30%, transparent 30%);
Home.py:        background-size: 100px 100px;
Home.py:        background-repeat: no-repeat;
Home.py:        pointer-events: none;
Home.py:        z-index: 0;
Home.py:    }}
Home.py:    
Home.py:    /* Style stat items to look like data cards */
Home.py:    .stat-item {{
Home.py:        position: relative;
Home.py:        overflow: hidden;
Home.py:        background: white;
Home.py:        border: 1px solid rgba(30, 136, 229, 0.2);
Home.py:        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
Home.py:    }}
Home.py:    
Home.py:    .stat-item::after {{
Home.py:        content: '';
Home.py:        position: absolute;
Home.py:        bottom: 0;
Home.py:        left: 0;
Home.py:        right: 0;
Home.py:        height: 3px;
Home.py:        background: linear-gradient(to right, #1E88E5, #4CAF50);
Home.py:    }}
Home.py:    
Home.py:    /* Style sections with data visualization elements */
Home.py:    .section {{
Home.py:        position: relative;
Home.py:        background: white;
Home.py:        border-radius: 12px;
Home.py:        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
Home.py:        border: 1px solid rgba(30, 136, 229, 0.1);
Home.py:        overflow: hidden;
Home.py:    }}
Home.py:    
Home.py:    .section::before {{
Home.py:        content: '';
Home.py:        position: absolute;
Home.py:        top: 0;
Home.py:        left: 0;
Home.py:        right: 0;
Home.py:        height: 4px;
Home.py:        background: linear-gradient(to right, #1E88E5, #4CAF50, #FFC107, #F44336);
Home.py:        z-index: 1;
Home.py:    }}
Home.py:    </style>
Home.py:    """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Theme selector in sidebar
Home.py:    with st.sidebar:
Home.py:        st.title("Settings")
Home.py:        selected_theme = st.selectbox(
Home.py:            "Select Theme",
Home.py:            options=list(THEMES.keys()),
Home.py:            index=list(THEMES.keys()).index(st.session_state['theme'])
Home.py:        )
Home.py:        
Home.py:        if selected_theme != st.session_state['theme']:
Home.py:            st.session_state['theme'] = selected_theme
Home.py:            apply_theme(selected_theme)
Home.py:            st.rerun()
Home.py:        
Home.py:        # Logout button
Home.py:        if st.button("Logout"):
Home.py:            st.session_state["authenticated"] = False
Home.py:            st.session_state["role"] = None
Home.py:            st.rerun()
Home.py:    
Home.py:    # Main content
Home.py:    st.markdown("<h1 class='main-title'>DMAT Escalations Dashboard</h1>", unsafe_allow_html=True)
Home.py:    
Home.py:    # Introduction section with company logo
Home.py:    col_logo, col_intro = st.columns([1, 3])
Home.py:    
Home.py:    with col_logo:
Home.py:        # Display a placeholder logo or icon
Home.py:        st.markdown("""
Home.py:        <div style="text-align: center; padding: 1rem;">
Home.py:            <div style="font-size: 5rem; color: #1E88E5;">├░┼╕ΓÇ£┼á</div>
Home.py:            <div style="font-weight: bold; margin-top: 0.5rem;">DMAT</div>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    with col_intro:
Home.py:        st.markdown("""
Home.py:        <div style="padding: 1rem;">
Home.py:            <h2 style="margin-bottom: 1rem;">Enterprise Escalations Management Platform</h2>
Home.py:            <p style="font-size: 1.1rem; line-height: 1.6;">
Home.py:                Welcome to the DMAT Escalations Dashboard, a comprehensive analytics platform for monitoring and managing escalations across different business domains. This dashboard provides real-time insights, trend analysis, and actionable recommendations to improve service delivery and operational efficiency.
Home.py:            </p>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Stats section
Home.py:    st.markdown("""
Home.py:    <div class="stats-container">
Home.py:        <div class="stat-item">
Home.py:            <div class="stat-value">2</div>
Home.py:            <div class="stat-label">Dashboard Modules</div>
Home.py:        </div>
Home.py:        <div class="stat-item">
Home.py:            <div class="stat-value">100%</div>
Home.py:            <div class="stat-label">Data Visualization</div>
Home.py:        </div>
Home.py:        <div class="stat-item">
Home.py:            <div class="stat-value">24/7</div>
Home.py:            <div class="stat-label">Monitoring</div>
Home.py:        </div>
Home.py:    </div>
Home.py:    """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Dashboard modules section
Home.py:    st.markdown("<h2 class='sub-title'>Dashboard Modules</h2>", unsafe_allow_html=True)
Home.py:    
Home.py:    # Dashboard cards
Home.py:    col1, col2 = st.columns(2)
Home.py:    
Home.py:    with col1:
Home.py:        st.markdown("""
Home.py:        <div class="dashboard-card">
Home.py:            <div class="dashboard-card-title">├░┼╕ΓÇ£┼á TA & Census Escalations</div>
Home.py:            <div class="dashboard-card-description">
Home.py:                Monitor and analyze Time & Attendance and Census escalations with comprehensive analytics. 
Home.py:                Track trends over time, identify patterns by category and account, detect anomalies, 
Home.py:                and generate actionable insights to improve service delivery and reduce escalation volume.
Home.py:            </div>
Home.py:            <a href="/Escalations_Dashboard" target="_self" class="dashboard-card-link">Open Dashboard</a>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    with col2:
Home.py:        st.markdown("""
Home.py:        <div class="dashboard-card">
Home.py:            <div class="dashboard-card-title">├░┼╕ΓÇÖ┬░ Deductions Escalations</div>
Home.py:            <div class="dashboard-card-description">
Home.py:                Track deductions escalations across different environments, providers, and employers with detailed analytics.
Home.py:                Monitor failure rates, analyze transaction trends, identify automation opportunities, and gain insights into 
Home.py:                common failure reasons to improve process efficiency and reduce financial impact.
Home.py:            </div>
Home.py:            <a href="/Deductions_Escalations" target="_self" class="dashboard-card-link">Open Dashboard</a>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Features section
Home.py:    st.markdown("<h2 class='sub-title'>Key Features</h2>", unsafe_allow_html=True)
Home.py:    
Home.py:    # Features in columns
Home.py:    col1, col2 = st.columns(2)
Home.py:    
Home.py:    with col1:
Home.py:        st.markdown("""
Home.py:        <div class="section">
Home.py:            <h3>TA & Census Escalations Dashboard</h3>
Home.py:            <ul class="feature-list">
Home.py:                <li>Real-time monitoring of escalation volume and trends</li>
Home.py:                <li>Interactive breakdown by categories, modes, and accounts</li>
Home.py:                <li>Advanced anomaly detection with AI-powered insights</li>
Home.py:                <li>Comprehensive data exploration with custom filters</li>
Home.py:                <li>Automated recommendations for process improvement</li>
Home.py:                <li>Export capabilities for reports and presentations</li>
Home.py:            </ul>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    with col2:
Home.py:        st.markdown("""
Home.py:        <div class="section">
Home.py:            <h3>Deductions Escalations Dashboard</h3>
Home.py:            <ul class="feature-list">
Home.py:                <li>Precise tracking of deduction amounts and failure rates</li>
Home.py:                <li>Multi-dimensional analysis by provider, method, and employer</li>
Home.py:                <li>Detailed failure analysis with root cause identification</li>
Home.py:                <li>Time-based trend analysis with forecasting capabilities</li>
Home.py:                <li>Customizable data explorer with search functionality</li>
Home.py:                <li>Data export in multiple formats (CSV, Excel)</li>
Home.py:            </ul>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Getting started section
Home.py:    st.markdown("<h2 class='sub-title'>Getting Started</h2>", unsafe_allow_html=True)
Home.py:    
Home.py:    st.markdown("""
Home.py:    <div class="section">
Home.py:        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
Home.py:            Follow these simple steps to start using the DMAT Escalations Dashboard:
Home.py:        </p>
Home.py:        
Home.py:        <ol style="padding-left: 1.5rem; line-height: 1.8;">
Home.py:            <li><strong>Select a dashboard module</strong> from the cards above based on your monitoring needs</li>
Home.py:            <li><strong>Upload your data file</strong> in the appropriate format (CSV or Excel)</li>
Home.py:            <li><strong>Explore the interactive visualizations</strong> to gain insights into your escalation data</li>
Home.py:            <li><strong>Use the filtering capabilities</strong> to focus on specific aspects of the data</li>
Home.py:            <li><strong>Review the automated insights and recommendations</strong> to improve your processes</li>
Home.py:            <li><strong>Export reports or data</strong> for further analysis or presentation</li>
Home.py:        </ol>
Home.py:    </div>
Home.py:    """, unsafe_allow_html=True)
Home.py:    
Home.py:    # System requirements
Home.py:    st.markdown("<h2 class='sub-title'>System Information</h2>", unsafe_allow_html=True)
Home.py:    
Home.py:    col1, col2 = st.columns(2)
Home.py:    
Home.py:    with col1:
Home.py:        st.markdown("""
Home.py:        <div class="section">
Home.py:            <h3>Technical Specifications</h3>
Home.py:            <ul class="feature-list">
Home.py:                <li>Built with Streamlit and Python</li>
Home.py:                <li>Interactive data visualization with Plotly</li>
Home.py:                <li>Responsive design for all screen sizes</li>
Home.py:                <li>Secure authentication system</li>
Home.py:                <li>Customizable themes and appearance</li>
Home.py:            </ul>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    with col2:
Home.py:        st.markdown("""
Home.py:        <div class="section">
Home.py:            <h3>Support Information</h3>
Home.py:            <ul class="feature-list">
Home.py:                <li>Version: 1.2.0 (May 2025)</li>
Home.py:                <li>Last Updated: May 14, 2025</li>
Home.py:                <li>Developed by: DMAT Development Team</li>
Home.py:                <li>Contact: support@dmat-team.com</li>
Home.py:                <li>Documentation: Available in Help section</li>
Home.py:            </ul>
Home.py:        </div>
Home.py:        """, unsafe_allow_html=True)
Home.py:    
Home.py:    # Footer
Home.py:    st.markdown("""
Home.py:    <div class="footer">
Home.py:        <div style="margin-bottom: 0.5rem; font-weight: 500;">DMAT Escalations Dashboard</div>
Home.py:        <div>├é┬⌐ 2025 DMAT Team | Version 1.2.0 | All Rights Reserved</div>
Home.py:    </div>
Home.py:    """, unsafe_allow_html=True)
Home.py:
