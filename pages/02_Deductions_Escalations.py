import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
import os
import sys
from scipy import stats
import json
from io import BytesIO, StringIO

# --- THEME AND SIDEBAR LOGIC ---
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
            padding: 1.2rem;
            border-bottom: 2px solid {theme["accent_color"]};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background: linear-gradient(to right, {theme["primary_color"]}15, {theme["accent_color"]}15);
            border-radius: 8px;
        }}
        
        /* Sub titles */
        .sub-title {{
            color: {theme["primary_color"]};
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 1.2rem;
            margin-bottom: 0.8rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {theme["accent_color"]};
            display: flex;
            align-items: center;
        }}
        
        /* Card Styling */
        .metric-card {{
            background-color: white;
            border-radius: 8px;
            padding: 1.2rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            border-left: 4px solid {theme["primary_color"]};
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {theme["primary_color"]};
            margin-bottom: 0.3rem;
        }}
        
        .metric-label {{
            font-size: 1rem;
            color: {theme["text_color"]}80;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Section styling */
        .dashboard-section {{
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        /* Upload area styling */
        .upload-container {{
            border: 2px dashed {theme["accent_color"]}50;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background-color: {theme["accent_color"]}10;
            transition: all 0.3s ease;
        }}
        
        .upload-container:hover {{
            border-color: {theme["accent_color"]};
            background-color: {theme["accent_color"]}15;
        }}
        
        /* Filter styling */
        .filter-container {{
            background-color: {theme["background_color"]};
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 1rem;
        }}
        
        /* Button styling */
        .stButton>button {{
            background-color: {theme["primary_color"]};
            color: white;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            border: none;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: {theme["primary_color"]}cc;
            transform: translateY(-2px);
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
        }}
        
        /* Welcome header */
        .welcome-header {{
            font-size: 1.2rem;
            font-weight: 600;
            color: {theme["primary_color"]};
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {theme["accent_color"]};
        }}
        
        /* Insights styling */
        .insight-item {{
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.8rem;
            background-color: {theme["background_color"]};
            border-radius: 8px;
            border-left: 3px solid {theme["secondary_color"]};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .insight-icon {{
            margin-right: 0.75rem;
            color: {theme["secondary_color"]};
            font-size: 1.2rem;
        }}
        
        .insight-content {{
            flex-grow: 1;
        }}
        
        /* Table styling */
        .dataframe {{
            border-collapse: collapse;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .dataframe th {{
            background-color: {theme["primary_color"]};
            color: white;
            text-transform: uppercase;
            font-size: 0.85rem;
            padding: 0.75rem 1rem;
            letter-spacing: 0.5px;
        }}
        
        .dataframe td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .dataframe tr:hover {{
            background-color: {theme["accent_color"]}10;
        }}
    </style>
    """, unsafe_allow_html=True)

# Create session state for user preferences if not exists
if 'theme' not in st.session_state:
    st.session_state['theme'] = "Default"

# Check authentication status
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Please log in from the Home page to access this dashboard.")
    st.stop()

# Create a minimal sidebar with just welcome message
with st.sidebar:
    # Welcome Message (always at the very top)
    st.markdown(f"<div class='welcome-header'>Welcome, {st.session_state.get('username', 'User')}</div>", unsafe_allow_html=True)
    
    # Add a separator
    st.markdown("<hr class='sidebar-separator'>", unsafe_allow_html=True)

# Apply the current theme
apply_theme(st.session_state['theme'])

# Initialize session state for storing the dataframe
if 'deductions_df' not in st.session_state:
    st.session_state['deductions_df'] = None
    st.session_state['file_processed'] = False

def process_uploaded_file(uploaded_file):
    """Process the uploaded file and return a cleaned dataframe"""
    try:
        # Read the file
        if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            df = pd.read_csv(uploaded_file)
        
        # Store original columns before any processing
        original_columns = df.columns.tolist()
        
        # First, clean up the column names (just trim whitespace, no title case conversion)
        df.columns = df.columns.str.strip()
        cleaned_columns = df.columns.tolist()
        
        # Define expected columns with possible variations (exact matches)
        column_mapping = {
            "Environment": ["Environment"],
            "Deduction Submission Date": ["Deduction Submission Date"],
            "BranchID": ["BranchID"],
            "Employer": ["Employer"],
            "DepartmentName": ["DepartmentName"],
            "Pay Day": ["Pay Day"],
            "Provider": ["Provider"],
            "Method": ["Method"],
            "Transactions": ["Transactions"],
            "Amount": ["Amount"],
            "Failed Amount": ["Failed Amount"],
            "Failed Department": ["Failed Department"],
            "Status": ["Status"],
            "Escalated To": ["Escalated To"],
            "Successful via Automation": ["Successful via Automation"],
            "Reason": ["Reason"],
            "Remarks": ["Remarks"],
            "Mode": ["Mode"],
            "Task Link / Email Subject": ["Task Link / Email Subject"]
        }
        
        # Create a mapping of cleaned column names to original names
        original_name_map = {col.strip(): col for col in original_columns}
        
        # Map actual columns to expected columns
        column_mapping_inv = {}
        mapped_columns = set()
        
        # First pass: exact matches
        for expected_col, possible_cols in column_mapping.items():
            for col in possible_cols:
                if col in df.columns:
                    column_mapping_inv[col] = expected_col
                    mapped_columns.add(col)
                    break
        
        # Second pass: case-insensitive matches for any remaining columns
        remaining_columns = [col for col in df.columns if col not in mapped_columns]
        
        for col in remaining_columns:
            col_lower = col.lower().replace(" ", "").replace("_", "").replace("-", "")
            for expected_col in column_mapping.keys():
                expected_col_lower = expected_col.lower().replace(" ", "").replace("_", "").replace("-", "")
                if col_lower == expected_col_lower:
                    column_mapping_inv[col] = expected_col
                    mapped_columns.add(col)
                    break
        
        # Rename columns to standard names
        if column_mapping_inv:
            df = df.rename(columns=column_mapping_inv)
        
        # Check for missing expected columns
        missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
        if missing_columns:
            st.warning(f"Warning: The following columns could not be mapped: {', '.join(missing_columns)}")
            st.info(f"Available columns: {', '.join(original_columns)}")
        
        # Convert numeric columns
        numeric_columns = ["Amount", "Failed Amount", "Transactions"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = convert_to_numeric(df[col])
        
        # Convert date columns
        date_columns = ["Deduction Submission Date", "Pay Day"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def convert_to_numeric(series):
    """Convert a series to numeric, handling currency symbols and commas"""
    if series is None:
        return pd.Series()
    
    # If series is already numeric, return as is
    if pd.api.types.is_numeric_dtype(series):
        return series
    
    # Convert series to string type first
    series = series.astype(str)
    
    # Remove currency symbols, commas, and spaces
    series = series.str.replace('$', '')
    series = series.str.replace(',', '')
    series = series.str.strip()
    
    # Convert to numeric, invalid values become NaN
    return pd.to_numeric(series, errors='coerce').fillna(0)

def safe_sum(series, default=0):
    """Safely sum a series, handling None and NaN values"""
    if series is None or series.empty or not pd.api.types.is_numeric_dtype(series):
        return default
    return series.sum()

def format_amount_with_millions(amount):
    """Format amount to show both full value and abbreviated value"""
    full_amount = f"${amount:,.2f}"
    billions = amount / 1_000_000_000
    millions = amount / 1_000_000
    
    if billions >= 1:
        return f"{full_amount}\n${billions:.2f}B"
    elif millions >= 1:
        return f"{full_amount}\n${millions:.2f}M"
    else:
        return full_amount

def format_metric_html(label, main_value, sub_value=None, delta=None, color='#0066cc'):
    """Format a metric with main value and optional sub-value using HTML"""
    html = f"""
    <div style='padding: 1rem; border-radius: 0.5rem;'>
        <div style='color: #666; font-size: 1rem;'>{label}</div>
        <div style='color: {color}; font-size: 1.5rem; margin-top: 0.5rem;'>{main_value}</div>
    """
    if sub_value:
        html += f"<div style='color: #666; font-size: 0.9rem;'>{sub_value}</div>"
    if delta:
        html += f"<div style='color: #666; font-size: 0.8rem; margin-top: 0.5rem;'>{delta}</div>"
    html += "</div>"
    return html

def display_metrics(df):
    """Display key metrics from the dataframe"""
    if df is None or df.empty:
        st.warning("No data available to display metrics.")
        return
    
    # Add custom CSS
    st.markdown("""
    <style>
    .metric-container {
        padding: 1rem;
        border-radius: 0.5rem;
        background: white;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 0.25rem;
    }
    .metric-abbrev {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2196F3;
        margin-left: 0.5rem;
    }
    .metric-delta {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Safely calculate metrics with default values
    total_deductions = safe_sum(df.get('Amount'))
    total_failed = safe_sum(df.get('Failed Amount'))
    total_transactions = len(df)
    avg_deduction = total_deductions / total_transactions if total_transactions > 0 else 0
    success_rate = ((total_transactions - (df['Failed Amount'] > 0).sum()) / total_transactions * 100) if total_transactions > 0 else 0
    failure_rate = 100 - success_rate
    
    # Create metrics layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Total Deductions</div>
            <div>
                <span class='metric-value'>${total_deductions:,.2f}</span>
                <span class='metric-abbrev'>${total_deductions/1_000_000:.1f}M</span>
            </div>
            <div class='metric-delta'>vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Success Rate</div>
            <div class='metric-value'>{success_rate:.1f}%</div>
            <div class='metric-delta'>vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Avg. Deduction</div>
            <div class='metric-value'>${avg_deduction:,.2f}</div>
            <div class='metric-delta'>vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Failed Amount</div>
            <div>
                <span class='metric-value'>${total_failed:,.2f}</span>
                <span class='metric-abbrev'>${total_failed/1_000_000:.1f}M</span>
            </div>
            <div class='metric-delta'>vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add transactions and failure rate below
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Transactions</div>
            <div class='metric-value'>{total_transactions}</div>
            <div class='metric-delta'>vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write(f"""
        <div class='metric-container'>
            <div class='metric-label'>Failure Rate</div>
            <div class='metric-value'>{failure_rate:.1f}%</div>
            <div class='metric-delta'>+ {failure_rate:.1f}% vs previous period</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='main-title'>📊 Deductions Escalations Dashboard</h1>", unsafe_allow_html=True)

    # Move file upload to sidebar
    with st.sidebar:
        st.markdown("<h3 class='sub-title'>📁 Upload Deductions Report</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Excel or CSV file",
            type=['xlsx', 'csv'],
            help="Upload your deductions escalations report in Excel (.xlsx) or CSV format"
        )

        if uploaded_file is not None:
            try:
                df = process_uploaded_file(uploaded_file)
                st.session_state['deductions_df'] = df
                st.session_state['file_processed'] = True
                st.success("File processed successfully!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.session_state['deductions_df'] = None
                st.session_state['file_processed'] = False

    # Display dashboard content if data is available
    if st.session_state['file_processed'] and st.session_state['deductions_df'] is not None:
        df = st.session_state['deductions_df']
        
        # Add tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Transaction Explorer", "📈 Advanced Analytics"])
        
        # Initialize session state for tab navigation
        if 'selected_provider' not in st.session_state:
            st.session_state.selected_provider = None
            st.session_state.force_explorer_refresh = False
        
        def navigate_to_explorer(provider=None):
            st.session_state.selected_provider = provider
            st.session_state.force_explorer_refresh = True
            # Store the current tab to return to after explorer
            st.session_state.previous_tab = "📊 Overview"
        
        with tab1:
            st.markdown("<div class='dashboard-section'>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-title'>📊 Deductions Overview</h3>", unsafe_allow_html=True)
            
            # Add a summary card at the top
            if 'Deduction Submission Date' in df.columns:
                earliest_date = df['Deduction Submission Date'].min().date()
                latest_date = df['Deduction Submission Date'].max().date()
                date_range = (latest_date - earliest_date).days
                
                # Summary info card
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #4285f4;">
                    <p style="margin-bottom: 0.5rem; font-size: 0.9rem; color: #555;">Dataset Summary</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
                        <div style="flex: 1;">
                            <div style="font-size: 0.85rem; color: #666;">Date Range</div>
                            <div style="font-weight: 600;">{earliest_date} to {latest_date} ({date_range} days)</div>
                        </div>
                        <div style="flex: 1;">
                            <div style="font-size: 0.85rem; color: #666;">Total Records</div>
                            <div style="font-weight: 600;">{len(df):,}</div>
                        </div>
                        <div style="flex: 1;">
                            <div style="font-size: 0.85rem; color: #666;">Unique Providers</div>
                            <div style="font-weight: 600;">{df['Provider'].nunique() if 'Provider' in df.columns else 'N/A'}</div>
                        </div>
                        <div style="flex: 1;">
                            <div style="font-size: 0.85rem; color: #666;">Unique Employers</div>
                            <div style="font-weight: 600;">{df['Employer'].nunique() if 'Employer' in df.columns else 'N/A'}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced date range filter with quick select buttons
            st.markdown("<h4 class='sub-title'>📅 Date Range Filter</h4>", unsafe_allow_html=True)
            if 'Deduction Submission Date' in df.columns:
                min_date = df['Deduction Submission Date'].min().date()
                max_date = df['Deduction Submission Date'].max().date()
                
                # Add quick filter buttons
                quick_filter_col1, quick_filter_col2, quick_filter_col3, quick_filter_col4 = st.columns(4)
                with quick_filter_col1:
                    last_30_days = st.button("Last 30 Days", key="last_30")
                with quick_filter_col2:
                    last_90_days = st.button("Last Quarter", key="last_90")
                with quick_filter_col3:
                    last_180_days = st.button("Last 6 Months", key="last_180")
                with quick_filter_col4:
                    all_time = st.button("All Time", key="all_time")
                
                # Handle quick filter selections
                if 'date_filter_range' not in st.session_state:
                    st.session_state['date_filter_range'] = 'custom'
                
                # Set date range based on quick filter buttons
                today = datetime.datetime.now().date()
                if last_30_days:
                    start_date = max((today - datetime.timedelta(days=30)), min_date)
                    end_date = min(today, max_date)
                    st.session_state['date_filter_range'] = '30d'
                elif last_90_days:
                    start_date = max((today - datetime.timedelta(days=90)), min_date)
                    end_date = min(today, max_date)
                    st.session_state['date_filter_range'] = '90d'
                elif last_180_days:
                    start_date = max((today - datetime.timedelta(days=180)), min_date)
                    end_date = min(today, max_date)
                    st.session_state['date_filter_range'] = '180d'
                elif all_time:
                    start_date = min_date
                    end_date = max_date
                    st.session_state['date_filter_range'] = 'all'
                else:
                    # Use custom range or default values
                    if 'start_date' not in st.session_state or 'end_date' not in st.session_state:
                        start_date = min_date
                        end_date = max_date
                    else:
                        start_date = st.session_state.get('start_date', min_date)
                        end_date = st.session_state.get('end_date', max_date)
                
                # Display calendar pickers in columns
                st.markdown("<p style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>Custom Date Range:</p>", unsafe_allow_html=True)
                
                # Display calendar pickers in columns
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Start Date",
                        min_value=min_date,
                        max_value=max_date,
                        value=start_date,
                        key="start_date"
                    )
                with col2:
                    end_date = st.date_input(
                        "End Date",
                        min_value=min_date,
                        max_value=max_date,
                        value=end_date,
                        key="end_date"
                    )
                
                # Filter data by date range
                date_mask = (
                    (df['Deduction Submission Date'].dt.date >= start_date) & 
                    (df['Deduction Submission Date'].dt.date <= end_date)
                )
                filtered_df = df[date_mask].copy()
                
                # Show the active date range
                st.markdown(f"<div style='background-color: #e8f4f8; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0;'><strong>Active Filter:</strong> {start_date} to {end_date} ({(end_date - start_date).days + 1} days)</div>", unsafe_allow_html=True)
                
                # Display key metrics with filtered data
                st.markdown("<h4 class='sub-title'>🔑 Key Metrics</h4>", unsafe_allow_html=True)
            else:
                filtered_df = df.copy()
                st.warning("No date column found for filtering")
                
                # Display key metrics with unfiltered data
                st.markdown("<h4 class='sub-title'>🔑 Key Metrics</h4>", unsafe_allow_html=True)
            
            # Calculate current metrics for comparison
            total_deductions = filtered_df['Amount'].sum() if 'Amount' in filtered_df.columns else 0
            avg_deduction = filtered_df['Amount'].mean() if 'Amount' in filtered_df.columns else 0
            total_failed = filtered_df['Failed Amount'].sum() if 'Failed Amount' in filtered_df.columns else 0
            failure_rate = (total_failed / total_deductions * 100) if total_deductions > 0 else 0
            total_transactions = len(filtered_df)
            success_count = filtered_df[filtered_df['Status'] == 'Successful'].shape[0] if 'Status' in filtered_df.columns else 0
            success_rate = (success_count / total_transactions * 100) if total_transactions > 0 else 0
            
            # Calculate metrics for previous period (if possible)
            if 'Deduction Submission Date' in filtered_df.columns:
                current_range_days = (end_date - start_date).days + 1
                prev_end_date = start_date - datetime.timedelta(days=1)
                prev_start_date = prev_end_date - datetime.timedelta(days=current_range_days)
                
                prev_mask = (
                    (df['Deduction Submission Date'].dt.date >= prev_start_date) & 
                    (df['Deduction Submission Date'].dt.date <= prev_end_date)
                )
                prev_period_df = df[prev_mask].copy()
                
                # Previous period metrics
                prev_total = prev_period_df['Amount'].sum() if 'Amount' in prev_period_df.columns and not prev_period_df.empty else 0
                prev_avg = prev_period_df['Amount'].mean() if 'Amount' in prev_period_df.columns and not prev_period_df.empty else 0
                prev_failed = prev_period_df['Failed Amount'].sum() if 'Failed Amount' in prev_period_df.columns and not prev_period_df.empty else 0
                prev_failure_rate = (prev_failed / prev_total * 100) if prev_total > 0 else 0
                prev_transactions = len(prev_period_df) if not prev_period_df.empty else 0
                
                # Calculate percent changes
                total_change_pct = ((total_deductions - prev_total) / prev_total * 100) if prev_total > 0 else 0
                avg_change_pct = ((avg_deduction - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0
                failed_change_pct = ((total_failed - prev_failed) / prev_failed * 100) if prev_failed > 0 else 0
                failure_rate_change = failure_rate - prev_failure_rate
                transaction_change_pct = ((total_transactions - prev_transactions) / prev_transactions * 100) if prev_transactions > 0 else 0
            else:
                total_change_pct = 0
                avg_change_pct = 0
                failed_change_pct = 0
                failure_rate_change = 0
                transaction_change_pct = 0
            
            # Create a more visually appealing metrics display
            metric_col1, metric_col2, metric_col3 = st.columns([1,1,1])
            
            with metric_col1:
                # Total Deductions Card
                trend_color = "#4CAF50" if total_change_pct >= 0 else "#F44336"
                trend_icon = "↑" if total_change_pct >= 0 else "↓"
                trend_display = f"{trend_icon} {abs(total_change_pct):.1f}%" if total_change_pct != 0 else "--"
                
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #1E88E5;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Total Deductions</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #1E88E5;">
                                <span>${total_deductions:,.2f}</span>
                                <span style="font-size: 1rem; margin-left: 0.5rem; opacity: 0.7;">(${total_deductions/1_000_000:.1f}M)</span>
                            </div>
                        </div>
                        <div style="background-color: rgba(30, 136, 229, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #1E88E5;">💰</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <span style="color: {trend_color};">{trend_display}</span> vs previous period
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
                # Transaction Count Card
                trend_color = "#4CAF50" if transaction_change_pct >= 0 else "#F44336"
                trend_icon = "↑" if transaction_change_pct >= 0 else "↓"
                trend_display = f"{trend_icon} {abs(transaction_change_pct):.1f}%" if transaction_change_pct != 0 else "--"
                
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #9C27B0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Transactions</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #9C27B0;">{total_transactions:,}</div>
                        </div>
                        <div style="background-color: rgba(156, 39, 176, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #9C27B0;">📊</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <span style="color: {trend_color};">{trend_display}</span> vs previous period
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            
            with metric_col2:
                # Success Rate Card
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #4CAF50;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Success Rate</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #4CAF50;">{success_rate:.1f}%</div>
                        </div>
                        <div style="background-color: rgba(76, 175, 80, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #4CAF50;">✅</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <div style="height: 5px; background-color: #f0f0f0; border-radius: 3px; margin-top: 0.3rem;">
                            <div style="height: 100%; width: {success_rate}%; background-color: #4CAF50; border-radius: 3px;"></div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
                # Failure Rate Card
                trend_color = "#4CAF50" if failure_rate_change <= 0 else "#F44336"  # For failure rate, lower is better
                trend_icon = "↓" if failure_rate_change <= 0 else "↑"
                trend_display = f"{trend_icon} {abs(failure_rate_change):.1f}%" if failure_rate_change != 0 else "--"
                
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #F44336;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Failure Rate</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #F44336;">{failure_rate:.1f}%</div>
                        </div>
                        <div style="background-color: rgba(244, 67, 54, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #F44336;">❌</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <span style="color: {trend_color};">{trend_display}</span> vs previous period
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            
            with metric_col3:
                # Average Deduction Card
                trend_color = "#4CAF50" if avg_change_pct >= 0 else "#F44336"
                trend_icon = "↑" if avg_change_pct >= 0 else "↓"
                trend_display = f"{trend_icon} {abs(avg_change_pct):.1f}%" if avg_change_pct != 0 else "--"
                
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #FF9800;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Avg. Deduction</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #FF9800;">
                                <span>${avg_deduction:,.2f}</span>
                                <span style="font-size: 1rem; margin-left: 0.5rem; opacity: 0.7;">(${avg_deduction/1_000:.1f}K)</span>
                            </div>
                        </div>
                        <div style="background-color: rgba(255, 152, 0, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #FF9800;">📏</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <span style="color: {trend_color};">{trend_display}</span> vs previous period
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
                # Failed Amount Card
                trend_color = "#4CAF50" if failed_change_pct <= 0 else "#F44336"  # For failed amount, lower is better
                trend_icon = "↓" if failed_change_pct <= 0 else "↑"
                trend_display = f"{trend_icon} {abs(failed_change_pct):.1f}%" if failed_change_pct != 0 else "--"
                
                html_content = f"""
                <div style="background-color: white; border-radius: 8px; padding: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem; border-left: 4px solid #E91E63;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Failed Amount</div>
                            <div style="font-size: 1.6rem; font-weight: 700; color: #E91E63;">
                                <span>${total_failed:,.2f}</span>
                                <span style="font-size: 1rem; margin-left: 0.5rem; opacity: 0.7;">(${total_failed/1_000_000:.1f}M)</span>
                            </div>
                        </div>
                        <div style="background-color: rgba(233, 30, 99, 0.1); padding: 0.5rem; border-radius: 50%; height: 40px; width: 40px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #E91E63;">⚠️</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #f0f0f0; font-size: 0.85rem;">
                        <span style="color: {trend_color};">{trend_display}</span> vs previous period
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            
            # First row of charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 class='sub-title'>📈 Deductions Trend Analysis</h4>", unsafe_allow_html=True)
                if 'Deduction Submission Date' in filtered_df.columns and 'Amount' in filtered_df.columns:
                    # Daily, weekly, monthly aggregation
                    freq = st.radio("View by:", ["Daily", "Weekly", "Monthly"], horizontal=True, key="trend_freq_radio")
                    freq_map = {"Daily": "D", "Weekly": "W-Mon", "Monthly": "M"}
            
            # Time series analysis
            time_series = filtered_df.groupby(
                pd.Grouper(key='Deduction Submission Date', freq=freq_map[freq])
            )['Amount'].sum().reset_index()
            
            # Calculate moving average based on frequency
            window = 4 if freq == "Monthly" else (2 if freq == "Weekly" else 7)
            
            # Create visualization
            fig = px.area(
                time_series, 
                x='Deduction Submission Date', 
                y='Amount',
                title=f'{freq} Deductions Trend',
                labels={'Amount': 'Total Amount ($)', 'Deduction Submission Date': 'Date'}
            )
            
            # Add moving average
            ma = time_series['Amount'].rolling(window=window, min_periods=1).mean()
            
            fig.add_scatter(
                x=time_series['Deduction Submission Date'],
                y=ma,
                mode='lines',
                name=f'{window}-point Moving Average',
                line=dict(color='red', width=2)
            )
            
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Amount ($)',
                hovermode='x unified'
            )
                
            st.plotly_chart(fig, use_container_width=True, key="trend_analysis_chart")
            
            # Second row of charts
            st.markdown("<h4 class='sub-title'>🏢 Top Employers by Deduction Amount</h4>", unsafe_allow_html=True)
            if 'Employer' in filtered_df.columns and 'Amount' in filtered_df.columns:
                top_employers = filtered_df.groupby('Employer')['Amount'].sum().nlargest(10).reset_index()
                
                fig = px.bar(
                    top_employers,
                    x='Amount',
                    y='Employer',
                    orientation='h',
                    title='Top 10 Employers by Deduction Amount',
                    labels={'Amount': 'Total Amount ($)', 'Employer': ''},
                    color='Amount',
                    color_continuous_scale='Viridis'
                )
                
                fig.update_layout(
                    xaxis_title='Total Amount ($)',
                    yaxis={'categoryorder': 'total ascending'},
                    height=500,
                    coloraxis_showscale=False
                )
                
                st.plotly_chart(fig, use_container_width=True, key="top_employers_chart")
                
                # Top 10 Employers by Escalations Count
                st.markdown("<h4 class='sub-title'>🔄 Top Employers by Escalations Count</h4>", unsafe_allow_html=True)
                if 'Employer' in filtered_df.columns:
                    # Count escalations per employer
                    escalations_by_employer = filtered_df.groupby('Employer').size().nlargest(10).reset_index()
                    escalations_by_employer.columns = ['Employer', 'Escalations Count']
                    
                    # Create horizontal bar chart for escalations count
                    fig_escalations = px.bar(
                        escalations_by_employer,
                        x='Escalations Count',
                        y='Employer',
                        orientation='h',
                        title='Top 10 Employers by Number of Escalations',
                        labels={'Escalations Count': 'Number of Escalations', 'Employer': ''},
                        color='Escalations Count',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig_escalations.update_layout(
                        xaxis_title='Number of Escalations',
                        yaxis={'categoryorder': 'total ascending'},
                        height=500,
                        coloraxis_showscale=False
                    )
                    
                    st.plotly_chart(fig_escalations, use_container_width=True, key="top_employers_escalations_chart")
                
                # Escalations by Method
                st.markdown("<h4 class='sub-title'>📬 Escalations by Method</h4>", unsafe_allow_html=True)
                if 'Method' in filtered_df.columns:
                    # Count escalations by method
                    method_counts = filtered_df['Method'].value_counts().reset_index()
                    method_counts.columns = ['Method', 'Count']
                    
                    # Calculate percentages
                    total_count = method_counts['Count'].sum()
                    method_counts['Percentage'] = (method_counts['Count'] / total_count * 100).round(1)
                    
                    # Create pie chart for method distribution
                    fig_methods = px.pie(
                        method_counts,
                        values='Count',
                        names='Method',
                        title='Distribution of Escalation Methods',
                        hole=0.4,  # Makes it a donut chart
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    # Update hover information to show both count and percentage
                    fig_methods.update_traces(
                        hovertemplate="<b>%{label}</b><br>" +
                                      "Count: %{value}<br>" +
                                      "Percentage: %{percent:.1%}<extra></extra>"
                    )
                    
                    fig_methods.update_layout(
                        height=400,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    # Display the visualization in two columns: chart and metrics
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.plotly_chart(fig_methods, use_container_width=True, key="method_distribution_chart")
                    
                    with col2:
                        st.markdown("### Method Breakdown")
                        # Create a clean metrics display
                        for _, row in method_counts.iterrows():
                            st.markdown(f"""
                            <div style="padding: 10px; margin-bottom: 10px; background-color: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 0.9rem; color: #666;">{row['Method']}</div>
                                <div style="font-size: 1.2rem; font-weight: bold; color: #1E88E5;">{row['Count']:,}</div>
                                <div style="font-size: 0.8rem; color: #666;">{row['Percentage']}% of total</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Breakdown by Provider
                st.markdown("<h4 class='sub-title'>🏢 Breakdown by Provider</h4>", unsafe_allow_html=True)
                if 'Provider' in filtered_df.columns:
                    # Count escalations by provider
                    provider_counts = filtered_df['Provider'].value_counts().reset_index()
                    provider_counts.columns = ['Provider', 'Count']
                    
                    # Calculate percentages
                    total_count = provider_counts['Count'].sum()
                    provider_counts['Percentage'] = (provider_counts['Count'] / total_count * 100).round(1)
                    
                    # Create pie chart for provider distribution
                    fig_providers = px.pie(
                        provider_counts,
                        values='Count',
                        names='Provider',
                        title='Distribution of Escalations by Provider',
                        hole=0.4,  # Makes it a donut chart
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    
                    # Update hover information
                    fig_providers.update_traces(
                        hovertemplate="<b>%{label}</b><br>" +
                                      "Count: %{value}<br>" +
                                      "Percentage: %{percent:.1%}<extra></extra>"
                    )
                    
                    fig_providers.update_layout(
                        height=400,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    # Display the visualization in two columns: chart and metrics
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.plotly_chart(fig_providers, use_container_width=True, key="provider_distribution_chart")
                    
                    with col2:
                        st.markdown("### Provider Breakdown")
                        # Create a clean metrics display
                        for _, row in provider_counts.iterrows():
                            st.markdown(f"""
                            <div style="padding: 10px; margin-bottom: 10px; background-color: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                <div style="font-size: 0.9rem; color: #666;">{row['Provider']}</div>
                                <div style="font-size: 1.2rem; font-weight: bold; color: #1E88E5;">{row['Count']:,}</div>
                                <div style="font-size: 0.8rem; color: #666;">{row['Percentage']}% of total</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            # Removed Provider Performance section - moved to Transaction Explorer tab
        
        with tab2:
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='dashboard-section'>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-title'>🔍 Transaction Explorer</h3>", unsafe_allow_html=True)
            
            # Check if we need to refresh the explorer view
            if st.session_state.get('force_explorer_refresh', False):
                st.session_state.force_explorer_refresh = False
                st.experimental_rerun()
            
            # Check if we have a provider filter from the Overview tab
            if st.session_state.selected_provider:
                st.info(f"Showing transactions for provider: {st.session_state.selected_provider}")
                if st.button("Clear filter"):
                    st.session_state.selected_provider = None
                    st.experimental_rerun()
                    
            # Display transaction explorer content
            if df.empty:
                st.warning("No transaction data available. Please upload a file first.")
                return
            
            # Transaction Explorer content starts here (Provider Analysis section removed)
                
            # Add filters
            st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
            st.markdown("<h4 class='sub-title'>🔎 Filters</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_options = df['Status'].unique() if 'Status' in df.columns else []
                status_filter = st.multiselect(
                    "Status",
                    options=status_options,
                    default=[]
                )
            
            with col2:
                provider_options = df['Provider'].unique() if 'Provider' in df.columns else []
                # If we have a selected provider from the Overview tab, use it as the default
                default_provider = [st.session_state.selected_provider] if st.session_state.selected_provider else []
                provider_filter = st.multiselect(
                    "Provider",
                    options=provider_options,
                    default=default_provider
                )
            
            with col3:
                min_amt = float(df['Amount'].min()) if 'Amount' in df.columns else 0
                max_amt = float(df['Amount'].max()) if 'Amount' in df.columns else 1000
                min_amount, max_amount = st.slider(
                    "Deduction Amount Range",
                    min_value=min_amt,
                    max_value=max_amt,
                    value=(min_amt, max_amt)
                )
            
            # Apply filters
            filtered_data = df.copy()
            if status_filter:
                filtered_data = filtered_data[filtered_data['Status'].isin(status_filter)]
            if provider_filter:
                filtered_data = filtered_data[filtered_data['Provider'].isin(provider_filter)]
            if 'Amount' in filtered_data.columns:
                filtered_data = filtered_data[
                    (filtered_data['Amount'] >= min_amount) & 
                    (filtered_data['Amount'] <= max_amount)
                ]
            
            # Show metrics for the filtered data
            if not filtered_data.empty:
                st.metric("Total Transactions", len(filtered_data))
                st.metric("Total Amount", f"${filtered_data['Amount'].sum():,.2f}" if 'Amount' in filtered_data.columns else "N/A")
            
            # Sorting options
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<h4 class='sub-title'>⏱️ Sort & Pagination</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                sort_by = st.selectbox(
                    "Sort by",
                    ['Deduction Submission Date', 'Amount', 'Status', 'Provider'],
                    index=0
                )
            
            with col2:
                sort_order = st.radio("Sort order", ["Descending", "Ascending"], horizontal=True)
            
            filtered_data = filtered_data.sort_values(
                by=sort_by,
                ascending=(sort_order == "Ascending"),
                na_position='last'
            )
            
            # Display data table with pagination
            if not filtered_data.empty:
                page_size = 10
                total_pages = (len(filtered_data) // page_size) + (1 if len(filtered_data) % page_size > 0 else 0)
                page_number = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1)
                start_idx = (page_number - 1) * page_size
                end_idx = start_idx + page_size
                
                # Display the current page of data
                st.dataframe(
                    filtered_data.iloc[start_idx:end_idx],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add export button
                csv = filtered_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Export Filtered Data",
                    data=csv,
                    file_name=f"deductions_export_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv',
                    key='download_csv',
                    use_container_width=True
                )
            else:
                st.warning("No data matches the selected filters.")
            
            # Clear the selected provider after displaying
            if st.session_state.selected_provider:
                st.session_state.selected_provider = None
        
        with tab3:
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='dashboard-section'>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-title'>📈 Advanced Analytics</h3>", unsafe_allow_html=True)
            
            # Performance Metrics
            st.markdown("<h4 class='sub-title'>⚡ Performance Metrics</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Success rate by provider
                if all(col in df.columns for col in ['Provider', 'Status', 'Amount']):
                    provider_perf = df.groupby('Provider').agg(
                        total_amount=('Amount', 'sum'),
                        success_rate=('Status', lambda x: (x == 'Successful').mean() * 100),
                        avg_amount=('Amount', 'mean')
                    ).reset_index()
                    
                    st.metric("Top Performing Provider", 
                             provider_perf.nlargest(1, 'total_amount')['Provider'].values[0] if not provider_perf.empty else "N/A",
                             f"${provider_perf['total_amount'].max():,.2f}" if not provider_perf.empty else "$0.00")
            
            with col2:
                if not provider_perf.empty:
                    avg_success_rate = provider_perf['success_rate'].mean()
                    st.metric("Average Success Rate", f"{avg_success_rate:.1f}%")
            
            with col3:
                if 'Failed Amount' in df.columns:
                    recovery_rate = (1 - (df['Failed Amount'].sum() / df['Amount'].sum())) * 100
                    st.metric("Recovery Rate", f"{recovery_rate:.1f}%")
            
            # Time-based analysis
            st.markdown("<h4 class='sub-title'>⏰ Time-Based Analysis</h4>", unsafe_allow_html=True)
            
            if 'Deduction Submission Date' in df.columns and 'Amount' in df.columns:
                # Weekly patterns
                df['DayOfWeek'] = df['Deduction Submission Date'].dt.day_name()
                df['Hour'] = df['Deduction Submission Date'].dt.hour
                
                # Day of week analysis
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekly_pattern = df.groupby('DayOfWeek')['Amount'].sum().reindex(day_order).reset_index()
                
                fig_weekly = px.bar(
                    weekly_pattern,
                    x='DayOfWeek',
                    y='Amount',
                    title='Deduction Amount by Day of Week',
                    labels={'Amount': 'Total Amount ($)', 'DayOfWeek': 'Day of Week'},
                    template='plotly_white'
                )
                
                # Hourly pattern
                hourly_pattern = df.groupby('Hour')['Amount'].sum().reset_index()
                
                fig_hourly = px.line(
                    hourly_pattern,
                    x='Hour',
                    y='Amount',
                    title='Deduction Amount by Hour of Day',
                    labels={'Amount': 'Total Amount ($)', 'Hour': 'Hour of Day'},
                    template='plotly_white',
                    markers=True
                )
                
                # Display charts
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig_weekly, use_container_width=True)
                with col2:
                    st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Provider Performance
            st.markdown("<h4 class='sub-title'>🏆 Provider Performance</h4>", unsafe_allow_html=True)
            
            if all(col in df.columns for col in ['Provider', 'Status', 'Amount']):
                # Top 10 providers by amount
                top_providers = df.groupby('Provider').agg(
                    total_amount=('Amount', 'sum'),
                    success_rate=('Status', lambda x: (x == 'Successful').mean() * 100),
                    avg_amount=('Amount', 'mean'),
                    count=('Amount', 'count')
                ).nlargest(10, 'total_amount').reset_index()
                
                # Create a bar chart with success rate as line
                fig_providers = go.Figure()
                
                # Bar chart for total amount
                fig_providers.add_trace(
                    go.Bar(
                        x=top_providers['Provider'],
                        y=top_providers['total_amount'],
                        name='Total Amount',
                        marker_color='#1f77b4'
                    )
                )
                
                # Line chart for success rate (secondary y-axis)
                fig_providers.add_trace(
                    go.Scatter(
                        x=top_providers['Provider'],
                        y=top_providers['success_rate'],
                        name='Success Rate %',
                        yaxis='y2',
                        line=dict(color='#ff7f0e', width=2)
                    )
                )
                
                # Update layout for dual y-axes
                fig_providers.update_layout(
                    title='Top 10 Providers by Deduction Amount',
                    xaxis_title='Provider',
                    yaxis_title='Total Amount ($)',
                    yaxis2=dict(
                        title='Success Rate (%)',
                        overlaying='y',
                        side='right',
                        range=[0, 100]  # Percentage range
                    ),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    template='plotly_white'
                )
                
                st.plotly_chart(fig_providers, use_container_width=True)
                
                # Show provider performance table
                st.markdown("**Provider Performance Metrics**")
                st.dataframe(
                    top_providers.rename(columns={
                        'total_amount': 'Total Amount ($)',
                        'success_rate': 'Success Rate (%)',
                        'avg_amount': 'Avg. Amount ($)',
                        'count': 'Transaction Count'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            # Time Series Analysis Section
            st.markdown("<h4 class='sub-title'>📊 Time Series Analysis</h4>", unsafe_allow_html=True)
            
            if 'Deduction Submission Date' in df.columns and 'Amount' in df.columns:
                # Resample data by week
                time_series = df.set_index('Deduction Submission Date')['Amount'].resample('W').sum().reset_index()
                
                # Calculate moving averages
                time_series['7D_MA'] = time_series['Amount'].rolling(window=4, min_periods=1).mean()
                time_series['30D_MA'] = time_series['Amount'].rolling(window=12, min_periods=1).mean()
                
                # Create the time series chart
                fig = go.Figure()
                
                # Add actual values
                fig.add_trace(go.Scatter(
                    x=time_series['Deduction Submission Date'],
                    y=time_series['Amount'],
                    mode='lines+markers',
                    name='Weekly Total',
                    line=dict(color='#1f77b4')
                ))
                
                # Add moving averages
                fig.add_trace(go.Scatter(
                    x=time_series['Deduction Submission Date'],
                    y=time_series['7D_MA'],
                    mode='lines',
                    name='4-Week Moving Avg',
                    line=dict(color='#ff7f0e', dash='dash')
                ))
                
                fig.add_trace(go.Scatter(
                    x=time_series['Deduction Submission Date'],
                    y=time_series['30D_MA'],
                    mode='lines',
                    name='12-Week Moving Avg',
                    line=dict(color='#2ca02c', dash='dot')
                ))
                
                fig.update_layout(
                    title='Deduction Amounts Over Time with Moving Averages',
                    xaxis_title='Date',
                    yaxis_title='Amount ($)',
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Anomaly Detection
                st.markdown("### Anomaly Detection")
                
                # Simple Z-score based anomaly detection
                time_series['zscore'] = (time_series['Amount'] - time_series['Amount'].mean()) / time_series['Amount'].std()
                anomalies = time_series[abs(time_series['zscore']) > 2]
                
                if not anomalies.empty:
                    st.warning(f"⚠️ Detected {len(anomalies)} potential anomalies in the data")
                    
                    # Create anomaly chart
                    anomaly_fig = go.Figure()
                    
                    # Add normal points
                    normal = time_series[abs(time_series['zscore']) <= 2]
                    anomaly_fig.add_trace(go.Scatter(
                        x=normal['Deduction Submission Date'],
                        y=normal['Amount'],
                        mode='markers',
                        name='Normal',
                        marker=dict(color='blue')
                    ))
                    
                    # Add anomalies
                    anomaly_fig.add_trace(go.Scatter(
                        x=anomalies['Deduction Submission Date'],
                        y=anomalies['Amount'],
                        mode='markers',
                        name='Anomaly',
                        marker=dict(color='red', size=10, line=dict(width=2, color='DarkRed'))
                    ))
                    
                    anomaly_fig.update_layout(
                        title='Detected Anomalies in Deduction Amounts',
                        xaxis_title='Date',
                        yaxis_title='Amount ($)',
                        height=400
                    )
                    
                    st.plotly_chart(anomaly_fig, use_container_width=True)
                    
                    # Show anomaly details
                    with st.expander("View Anomaly Details"):
                        anomaly_display = anomalies[['Deduction Submission Date', 'Amount', 'zscore']].copy()
                        anomaly_display['Deviation'] = (anomaly_display['zscore'].abs() * 100).round(2).astype(str) + '% from mean'
                        anomaly_display = anomaly_display.rename(columns={
                            'Deduction Submission Date': 'Date',
                            'Amount': 'Deduction Amount',
                            'zscore': 'Z-Score'
                        })
                        st.dataframe(anomaly_display, hide_index=True, use_container_width=True)
                else:
                    st.success("✅ No significant anomalies detected in the data")
            
            # Correlation Analysis
            st.markdown("### Correlation Analysis")
            
            # Add key points for understanding correlations
            st.markdown("""
            #### Understanding Correlations:
            - **Strong Positive (0.7 to 1.0)**: As one variable increases, the other increases strongly
            - **Moderate Positive (0.3 to 0.7)**: As one variable increases, the other tends to increase moderately
            - **Weak Positive (0 to 0.3)**: Variables have a slight tendency to move together
            - **Weak Negative (0 to -0.3)**: Variables have a slight tendency to move in opposite directions
            - **Moderate Negative (-0.3 to -0.7)**: As one variable increases, the other tends to decrease moderately
            - **Strong Negative (-0.7 to -1.0)**: As one variable increases, the other decreases strongly
            """)
            
            if len(df.select_dtypes(include=['number']).columns) > 1:
                # Select numeric columns for correlation, excluding BranchID and Hour
                numeric_cols = [col for col in df.select_dtypes(include=['number']).columns if col not in ['BranchID', 'Hour']]
                
                if len(numeric_cols) >= 2:
                    # Calculate correlation matrix
                    corr = df[numeric_cols].corr()
                    
                    # Create heatmap
                    fig = px.imshow(
                        corr,
                        text_auto=True,
                        aspect="auto",
                        color_continuous_scale='RdBu',
                        zmin=-1,
                        zmax=1,
                        title='Correlation Matrix of Numeric Variables'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add explanation of the correlation matrix
                    st.markdown("""
                    #### Understanding the Correlation Matrix:
                    The correlation matrix above shows how different numeric variables in your data are related to each other:
                    
                    - Each cell shows the correlation between two variables (ranging from -1 to 1)
                    - **Blue colors** indicate **positive correlations** (variables move in the same direction)
                    - **Red colors** indicate **negative correlations** (variables move in opposite directions)
                    - **Darker colors** mean **stronger relationships**
                    - **Lighter colors** mean **weaker relationships**
                    - The diagonal shows correlations of variables with themselves (always 1.0)
                    """)
                    
                    # Find strongest correlations for examples
                    corr_unstack = corr.unstack()
                    corr_unstack = corr_unstack[corr_unstack != 1.0]  # Remove self-correlations
                    corr_unstack = corr_unstack.dropna()
                    
                    # Get strongest positive and negative correlations
                    strongest_pos = corr_unstack[corr_unstack > 0].nlargest(1)
                    strongest_neg = corr_unstack[corr_unstack < 0].nsmallest(1)
                    
                    examples = []
                    
                    if not strongest_pos.empty:
                        var1, var2 = strongest_pos.index[0]
                        corr_value = strongest_pos.values[0]
                        strength = "strongly" if abs(corr_value) > 0.7 else "moderately" if abs(corr_value) > 0.3 else "slightly"
                        examples.append(f"- **Strong Positive Correlation**: When {var1} increases, {var2} also tends to increase {strength} (correlation: {corr_value:.2f})")
                    
                    if not strongest_neg.empty:
                        var1, var2 = strongest_neg.index[0]
                        corr_value = strongest_neg.values[0]
                        strength = "strongly" if abs(corr_value) > 0.7 else "moderately" if abs(corr_value) > 0.3 else "slightly"
                        examples.append(f"- **Strong Negative Correlation**: When {var1} increases, {var2} tends to decrease {strength} (correlation: {corr_value:.2f})")
                    
                    if examples:
                        st.markdown("**Key Insights from Your Data:**")
                        st.markdown("\n".join(examples))
                    
                    # Show top correlations
                    st.markdown("#### Top Correlations")
                    
                    # Get upper triangle of correlation matrix
                    corr = corr.mask(np.triu(np.ones_like(corr, dtype=bool)))
                    
                    # Unstack and sort correlations
                    corr_pairs = corr.unstack().sort_values(ascending=False)
                    
                    # Create a DataFrame of correlations
                    corr_df = pd.DataFrame(corr_pairs, columns=['Correlation']).reset_index()
                    corr_df = corr_df[corr_df['Correlation'] != 1]  # Remove self-correlations
                    corr_df = corr_df.dropna()
                    
                    if not corr_df.empty:
                        top_correlations = corr_df.head(10)
                        
                        # Create a bar chart of top correlations
                        fig = px.bar(
                            top_correlations,
                            x='Correlation',
                            y=top_correlations['level_0'] + ' & ' + top_correlations['level_1'],
                            orientation='h',
                            title='Top Variable Correlations',
                            labels={'Correlation': 'Correlation Coefficient', 'y': 'Variable Pairs'}
                        )
                        
                        fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
                        st.plotly_chart(fig, use_container_width=True, key="correlation_chart")
                    else:
                        st.info("No significant correlations found between numeric variables.")
                else:
                    st.warning("Need at least two numeric columns for correlation analysis.")
            else:
                st.warning("Not enough numeric data for correlation analysis.")
            
            # Advanced Filtering
            st.markdown("### Advanced Data Exploration")
            
            # Dynamic filters
            st.markdown("#### Apply Filters")
            
            filter_cols = st.columns(3)
            filters = {}
            
            # Get unique values for filtering
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Add categorical filters
            for i, col in enumerate(categorical_cols[:3]):  # Show first 3 categorical columns
                with filter_cols[i % 3]:
                    unique_vals = df[col].unique().tolist()
                    if len(unique_vals) > 1:  # Only show if there's more than one unique value
                        selected = st.multiselect(f"Filter by {col}", options=unique_vals, key=f"filter_{col}")
                        if selected:
                            filters[col] = selected
            
            # Add numeric range filters
            st.markdown("#### Numeric Ranges")
            range_cols = st.columns(2)
            
            for i, col in enumerate(numeric_cols[:4]):  # Show first 4 numeric columns
                with range_cols[i % 2]:
                    min_val = float(df[col].min())
                    max_val = float(df[col].max())
                    
                    # Create a range slider
                    values = st.slider(
                        f"{col} Range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        key=f"range_{col}"
                    )
                    
                    filters[f"{col}_min"] = values[0]
                    filters[f"{col}_max"] = values[1]
            
            # Apply filters
            filtered_df = df.copy()
            
            # Apply categorical filters
            for col, values in filters.items():
                if col in categorical_cols:
                    filtered_df = filtered_df[filtered_df[col].isin(values)]
                elif col.endswith('_min') and col.replace('_min', '') in numeric_cols:
                    col_name = col.replace('_min', '')
                    filtered_df = filtered_df[filtered_df[col_name] >= values]
                elif col.endswith('_max') and col.replace('_max', '') in numeric_cols:
                    col_name = col.replace('_max', '')
                    filtered_df = filtered_df[filtered_df[col_name] <= values]
            
            # Show filtered data
            st.markdown(f"#### Filtered Data ({len(filtered_df)} rows)")
            st.dataframe(filtered_df, use_container_width=True)
            
            # Export filtered data
            st.download_button(
                label="Download Filtered Data (CSV)",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_deductions.csv',
                mime='text/csv',
                key='download_filtered_data'
            )

if __name__ == "__main__":
    main()
