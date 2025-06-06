import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import math

# Page configuration
st.set_page_config(
    page_title="Deductions Insights",
    page_icon="💰",
    layout="wide"
)

# Increase pandas styler limit
pd.set_option('styler.render.max_elements', 1000000)

def process_deductions_file(uploaded_file):
    """Process the uploaded deductions file and return a cleaned dataframe"""
    try:
        # Read the file with BranchID as string
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, dtype={'BranchID': str})
        else:
            df = pd.read_csv(uploaded_file, dtype={'BranchID': str})
        
        # Expected columns
        expected_columns = [
            'Environment', 'Deduction Submission Date', 'BranchID', 'Employer',
            'DepartmentName', 'Pay Day', 'Provider', 'Method', 'Transactions',
            'Amount', 'Failed Amount', 'Failed Department', 'Status',
            'Escalated To', 'Successful via Automation', 'Reason', 'Remarks',
            'Task Link / Email Subject'
        ]
        
        # Check if all required columns are present
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return None
        
        # Fill NaN values
        df['DepartmentName'] = df['DepartmentName'].fillna('Not Specified')
        df['Employer'] = df['Employer'].fillna('Not Specified')
        df['Status'] = df['Status'].fillna('Not Specified')
        df['BranchID'] = df['BranchID'].fillna('').astype(str)  # Convert BranchID to string and empty string for NaN
        
        # Convert date columns to datetime
        date_columns = ['Deduction Submission Date', 'Pay Day']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['Amount', 'Failed Amount', 'Transactions']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)  # Replace NaN with 0 for numeric columns
        
        return df
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def display_employer_details(df, selected_employer):
    """Display detailed analysis for a selected employer"""
    employer_data = df[df['Employer'] == selected_employer]
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Deductions", f"${employer_data['Amount'].sum():,.2f}")
    with col2:
        st.metric("Total Transactions", f"{employer_data['Transactions'].sum():,}")
    with col3:
        success_rate = (employer_data[employer_data['Status'] == 'Successful']['Amount'].sum() / 
                       employer_data['Amount'].sum() * 100)
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col4:
        st.metric("Unique Departments", f"{employer_data['DepartmentName'].nunique():,}")
    
    # Department breakdown
    st.subheader("Department Breakdown")
    dept_metrics = employer_data.groupby('DepartmentName').agg({
        'Amount': 'sum',
        'Transactions': 'sum',
        'Failed Amount': 'sum'
    }).reset_index()
    dept_metrics['Success Rate'] = ((dept_metrics['Amount'] - dept_metrics['Failed Amount']) / 
                                  dept_metrics['Amount'] * 100)
    st.dataframe(
        dept_metrics.sort_values('Amount', ascending=False).style.format({
            'Amount': '${:,.2f}',
            'Failed Amount': '${:,.2f}',
            'Transactions': '{:,}',
            'Success Rate': '{:.1f}%'
        }),
        use_container_width=True
    )
    
    # Timeline visualization
    st.subheader("Deductions Timeline")
    timeline_data = employer_data.groupby('Deduction Submission Date').agg({
        'Amount': 'sum',
        'Transactions': 'sum'
    }).reset_index()
    
    fig = px.line(timeline_data, 
                  x='Deduction Submission Date', 
                  y=['Amount', 'Transactions'],
                  title=f"Deductions Timeline for {selected_employer}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Pay periods
    st.subheader("Pay Period Analysis")
    pay_period_data = employer_data.groupby('Pay Day').agg({
        'Amount': 'sum',
        'Transactions': 'sum'
    }).reset_index()
    st.dataframe(
        pay_period_data.sort_values('Pay Day', ascending=False).style.format({
            'Amount': '${:,.2f}',
            'Transactions': '{:,}'
        }),
        use_container_width=True
    )

def main():
    st.title("Deductions Insights")
    
    # Sidebar configuration
    st.sidebar.title("Upload Data")
    
    # File uploader in sidebar
    uploaded_file = st.sidebar.file_uploader(
        "Upload Deductions File",
        type=['csv', 'xlsx'],
        help="Upload a CSV or Excel file containing deductions data"
    )
    
    # Add a divider in sidebar
    if uploaded_file:
        st.sidebar.markdown("---")
    
    if uploaded_file is not None:
        df = process_deductions_file(uploaded_file)
        
        if df is not None:
            st.success("File uploaded and processed successfully!")
            
            # Filters
            st.sidebar.header("Filters")
            
            # Environment filter
            environments = ['All'] + sorted(df['Environment'].unique().tolist())
            selected_environment = st.sidebar.selectbox("Environment", environments)
            
            # Separate start and end date filters
            min_date = df['Deduction Submission Date'].min().date()
            max_date = df['Deduction Submission Date'].max().date()
            
            start_date = st.sidebar.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )
            
            end_date = st.sidebar.date_input(
                "End Date",
                value=max_date,
                min_value=start_date,
                max_value=max_date
            )
            
            # Employer filter
            employers = ['All'] + sorted(df['Employer'].unique().tolist())
            selected_employer = st.sidebar.selectbox("Employer", employers)
            
            # Department filter
            departments = ['All'] + sorted(df['DepartmentName'].unique().tolist())
            selected_department = st.sidebar.selectbox("Department", departments)
            
            # Status filter
            statuses = ['All'] + sorted(df['Status'].unique().tolist())
            selected_status = st.sidebar.selectbox("Status", statuses)
            
            # Apply filters
            filtered_df = df.copy()
            
            # Environment filter
            if selected_environment != 'All':
                filtered_df = filtered_df[filtered_df['Environment'] == selected_environment]
            
            # Date filter
            filtered_df = filtered_df[
                (filtered_df['Deduction Submission Date'].dt.date >= start_date) &
                (filtered_df['Deduction Submission Date'].dt.date <= end_date)
            ]
            
            if selected_employer != 'All':
                filtered_df = filtered_df[filtered_df['Employer'] == selected_employer]
            
            if selected_department != 'All':
                filtered_df = filtered_df[filtered_df['DepartmentName'] == selected_department]
            
            if selected_status != 'All':
                filtered_df = filtered_df[filtered_df['Status'] == selected_status]
            
            # Calculate total and environment-wise deductions
            total_deductions = filtered_df['Amount'].sum()
            env_deductions = filtered_df.groupby('Environment')['Amount'].sum()
            
            # Display employer statistics with custom styling
            st.markdown("""
            <div style='padding: 1rem; border-radius: 10px; background: linear-gradient(to right, #1e3c72, #2a5298);'>
                <h2 style='color: white; margin-bottom: 1rem; font-size: 1.8rem;'>
                    📊 Employer Statistics Overview
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Add some spacing
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create columns dynamically based on environments plus one for total
            num_cols = len(env_deductions) + 1
            cols = st.columns(num_cols)
            
            # Custom CSS for metric containers
            metric_style = """
            <style>
                [data-testid="stMetricValue"] {
                    font-size: 1.2rem !important;
                    color: #0066cc;
                    font-weight: bold;
                    white-space: nowrap;
                    overflow: visible !important;
                }
                [data-testid="stMetricLabel"] {
                    font-size: 1rem;
                    color: #666;
                    white-space: nowrap;
                    overflow: visible !important;
                }
                div[data-testid="stMetricLabel"] > div {
                    width: 100% !important;
                    overflow: visible !important;
                }
                div[data-testid="stMetricValue"] > div {
                    width: 100% !important;
                    overflow: visible !important;
                }
                div[data-testid="metric-container"] {
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    height: 100%;
                    width: 100%;
                    overflow: visible !important;
                }
            </style>
            """
            st.markdown(metric_style, unsafe_allow_html=True)
            
            def format_amount_with_millions(amount):
                """Format amount with both full value and millions in brackets"""
                full_amount = f"${amount:,.2f}"
                millions = amount / 1_000_000
                if millions >= 1:
                    return f"{full_amount} [${millions:.1f}M]"
                else:
                    return full_amount
            
            # Display total deductions in first column with icon
            with cols[0]:
                st.metric(
                    "💰 Total Deductions",
                    format_amount_with_millions(total_deductions)
                )
            
            # Environment icons mapping
            env_icons = {
                'MyMo': '🌟',
                'UKG': '⭐',
                'Canada Live!': '🍁',
                'OnePath': '🔷',
                'UKG Canada': '🌐'
            }
            
            # Display environment-wise deductions with icons and styling
            for idx, (env, amount) in enumerate(env_deductions.items(), 1):
                with cols[idx]:
                    st.metric(
                        f"{env_icons.get(env, '🔹')} {env}",
                        format_amount_with_millions(amount)
                    )

            # Calculate employer statistics
            employer_stats = filtered_df.groupby('Employer').agg({
                'Amount': 'sum',
                'Failed Amount': 'sum',
                'Transactions': 'sum'
            }).reset_index()
            
            # Calculate success rate and total amount
            employer_stats['Success Rate'] = ((employer_stats['Amount'] - employer_stats['Failed Amount']) / employer_stats['Amount'] * 100).fillna(0)
            employer_stats['Total Amount'] = employer_stats['Amount']
            
            # Calculate total deductions across all employers
            total_deductions = filtered_df['Amount'].sum()  # Use original Amount from filtered_df
            
            # Calculate contribution percentage
            employer_stats['Contribution %'] = (employer_stats['Amount'] / total_deductions * 100)
            
            # Sort by Total Amount descending
            employer_stats = employer_stats.sort_values('Total Amount', ascending=False)
            
            # Display total deductions
            st.markdown(f"### Total Deductions: ${total_deductions:,.2f}")
            
            # Display top 10 employers by deduction amount
            st.markdown("#### Top 10 Employers by Deduction Amount")
            
            # Format the display columns
            display_stats = employer_stats.head(10).copy()
            display_stats['Total Amount'] = display_stats['Total Amount'].apply(lambda x: f"${x:,.2f}")
            display_stats['Amount'] = display_stats['Amount'].apply(lambda x: f"${x:,.2f}")
            display_stats['Failed Amount'] = display_stats['Failed Amount'].apply(lambda x: f"${x:,.2f}")
            display_stats['Success Rate'] = display_stats['Success Rate'].apply(lambda x: f"{x:.1f}%")
            display_stats['Contribution %'] = display_stats['Contribution %'].apply(lambda x: f"{x:.1f}%")
            display_stats['Transactions'] = display_stats['Transactions'].apply(lambda x: f"{int(x):,}")
            
            st.dataframe(
                display_stats,
                column_config={
                    'Employer': 'Employer Name',
                    'Total Amount': 'Total Deductions',
                    'Amount': 'Successful Amount',
                    'Failed Amount': 'Failed Amount',
                    'Transactions': 'Total Transactions',
                    'Success Rate': 'Success Rate',
                    'Contribution %': 'Contribution %'
                },
                use_container_width=True
            )
            
            # Add pie chart using the exact percentages from the table
            st.markdown("#### Top 10 Employers Contribution Distribution")
            
            # Create pie chart data with exact percentages
            pie_data = employer_stats.head(10)[['Employer', 'Contribution %']].copy()
            
            # Create a constant value of 100 to force plotly to use our percentages directly
            total = 100
            pie_data['Display Value'] = pie_data['Contribution %'] / pie_data['Contribution %'].sum() * total
            
            # Create pie chart using our calculated display values
            contribution_fig = px.pie(
                pie_data,
                values='Display Value',
                names='Employer',
                title=''
            )
            
            # Update hover template to show original contribution percentage
            contribution_fig.update_traces(
                textinfo='text',  # Use custom text
                text=pie_data['Contribution %'].apply(lambda x: f'{x:.1f}%'),  # Show exact table percentage
                hovertemplate="<b>%{label}</b><br>" +
                              "Contribution: %{text}"
            )
            
            # Update layout
            contribution_fig.update_layout(
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(contribution_fig, use_container_width=True)
            
            # Create a bar chart for top 10 employers
            fig = px.bar(
                employer_stats.head(10),
                x='Employer',
                y='Amount',
                title='Top 10 Employers by Deduction Amount',
                labels={'Amount': 'Total Deductions ($)', 'Employer': 'Employer Name'},
                color='Success Rate',
                color_continuous_scale='RdYlGn'  # Red to Yellow to Green scale
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecasting Section
            st.markdown("### Deductions Forecast Analysis")
            
            # Function to determine pay period type
            def analyze_pay_period(dates):
                # Convert to datetime if not already
                dates = pd.to_datetime(dates)
                
                # Calculate differences between consecutive dates
                diff_days = dates.diff().dt.days.dropna()
                
                # Get the most common difference
                most_common_diff = diff_days.mode().iloc[0]
                
                # Determine pay period type
                if most_common_diff <= 7:
                    return 'Weekly', most_common_diff
                elif most_common_diff <= 14:
                    return 'Bi-Weekly', most_common_diff
                elif most_common_diff <= 16:
                    return 'Semi-Monthly', most_common_diff
                else:
                    return 'Monthly', most_common_diff
            
            # Group by employer and analyze pay periods
            employer_forecasts = []
            
            for employer in employer_stats.head(10)['Employer']:
                employer_data = filtered_df[filtered_df['Employer'] == employer].copy()
                
                # Sort by submission date
                employer_data = employer_data.sort_values('Deduction Submission Date')
                
                # Analyze pay period
                pay_period_type, days_between = analyze_pay_period(employer_data['Pay Day'])
                
                # Calculate average transactions per pay period
                avg_transactions = len(employer_data) / len(employer_data['Pay Day'].unique())
                
                # Sort submissions by date to analyze patterns
                submissions = employer_data.sort_values('Deduction Submission Date')
                submissions = submissions.groupby('Deduction Submission Date')['Amount'].sum().reset_index()
                
                # Store pattern info for display
                pattern_info = []
                
                if len(submissions) >= 4:
                    # Get all submissions for analysis
                    dates = submissions['Deduction Submission Date'].dt.strftime('%Y-%m-%d').tolist()
                    amounts = submissions['Amount'].tolist()
                    
                    # Add recent submissions to pattern info
                    for d, a in list(zip(dates, amounts))[-4:]:
                        pattern_info.append(f"{d}: ${a:,.2f}")
                    
                    # Sort amounts to find distinct ranges
                    sorted_amounts = sorted(amounts)
                    
                    # Find median to separate high/low amounts
                    median = sorted_amounts[len(sorted_amounts)//2]
                    
                    # Group into high/low amounts
                    low_amounts = [a for a in amounts if a <= median]
                    high_amounts = [a for a in amounts if a > median]
                    
                    # Calculate averages
                    low_avg = sum(low_amounts) / len(low_amounts) if low_amounts else 0
                    high_avg = sum(high_amounts) / len(high_amounts) if high_amounts else 0
                    
                    # If we have clear separation between high and low amounts
                    if high_avg > low_avg * 10:  # High amounts at least 10x larger than low
                        last_amount = amounts[-1]
                        if last_amount > median:
                            expected_amount = low_avg  # Last was high, next should be low
                        else:
                            expected_amount = high_avg  # Last was low, next should be high
                    else:
                        # No clear high/low pattern, use weighted average
                        weights = [0.4, 0.3, 0.2, 0.1]  # Most recent has highest weight
                        expected_amount = sum(amt * w for amt, w in zip(reversed(amounts[-4:]), weights))
                else:
                    pattern_info.append("Not enough history to analyze pattern")
                    expected_amount = submissions['Amount'].iloc[-1]
                # Get last submission date
                last_submission = pd.to_datetime(employer_data['Deduction Submission Date'].max())
                last_payday = pd.to_datetime(employer_data['Pay Day'].max())
                
                # Calculate next expected dates
                next_payday = last_payday + pd.Timedelta(days=days_between)
                next_submission = last_submission + pd.Timedelta(days=days_between)
                
                employer_forecasts.append({
                    'Employer': employer,
                    'Pay Period Type': pay_period_type,
                    'Avg Transactions': round(avg_transactions),
                    'Expected Amount': expected_amount,
                    'Next Expected Payday': next_payday,
                    'Next Expected Submission': next_submission
                })
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame(employer_forecasts)
            
            # Format dates and amounts
            forecast_df['Next Expected Payday'] = forecast_df['Next Expected Payday'].dt.strftime('%Y-%m-%d')
            forecast_df['Next Expected Submission'] = forecast_df['Next Expected Submission'].dt.strftime('%Y-%m-%d')
            forecast_df['Expected Amount'] = forecast_df['Expected Amount'].apply(lambda x: f'${x:,.2f}')
            
            # Display forecast table with clear separation
            st.markdown("---")
            st.header("Deductions Forecast Analysis")
            st.markdown("Based on historical submission patterns for top employers:")
            
            # Create two columns for better layout
            forecast_col1, forecast_col2 = st.columns([3, 1])
            
            with forecast_col1:
                st.dataframe(
                    forecast_df,
                    column_config={
                        'Employer': 'Employer',
                        'Pay Period Type': 'Pay Period',
                        'Avg Transactions': 'Avg Transactions per Period',
                        'Expected Amount': 'Expected Amount (Based on Trend)',
                        'Next Expected Payday': 'Next Expected Payday',
                        'Next Expected Submission': 'Next Expected Submission'
                    },
                    use_container_width=True
                )
            
            with forecast_col2:
                st.info("📅 Recent Submissions:\n" + "\n".join(pattern_info))
            
            st.markdown("---")
            
            # Display employer contribution analysis
            st.header("Employer Contribution Analysis")
            total_records = len(filtered_df)
            st.write(f"Total records: {total_records:,}")
            
            # Pagination controls
            records_per_page = 1000
            total_pages = math.ceil(total_records / records_per_page)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                current_page = st.selectbox(
                    "Page",
                    options=range(1, total_pages + 1),
                    format_func=lambda x: f"Page {x} of {total_pages}"
                )
            
            # Calculate start and end indices for current page
            start_idx = (current_page - 1) * records_per_page
            end_idx = min(start_idx + records_per_page, total_records)
            
            # Format the dataframe for display
            display_df = filtered_df.sort_values('Deduction Submission Date', ascending=False)
            page_df = display_df.iloc[start_idx:end_idx]
            
            # Apply styling with formatted columns
            styled_df = page_df.style.format({
                'Deduction Submission Date': lambda x: x.strftime('%Y-%m-%d'),
                'Pay Day': lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else '',
                'Amount': '${:,.2f}',
                'Failed Amount': '${:,.2f}',
                'Transactions': '{:,}'
            })
            
            # Display page information
            st.write(f"Showing records {start_idx + 1:,} to {end_idx:,}")
            
            # Display the paginated dataframe
            st.dataframe(styled_df, use_container_width=True)
            
            # Display employer details if specific employer is selected
            if selected_employer != 'All':
                st.markdown("---")
                st.header(f"Detailed Analysis for {selected_employer}")
                display_employer_details(filtered_df, selected_employer)

if __name__ == "__main__":
    main()
