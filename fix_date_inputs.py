# Script to fix date_input components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Define patterns for the date_input components and their replacements
replacements = [
    # First set of date inputs (around line 363)
    (r'start_date = st\.date_input\(\s*"From Date",\s*value=min_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'start_date = st.date_input(\n                                "From Date",\n                                value=min_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="overview_start_date"\n                            )'),
    
    (r'end_date = st\.date_input\(\s*"To Date",\s*value=max_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'end_date = st.date_input(\n                                "To Date",\n                                value=max_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="overview_end_date"\n                            )'),
    
    # Second set of date inputs (around line 689)
    (r'start_date = st\.date_input\(\s*"From Date",\s*value=min_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'start_date = st.date_input(\n                                "From Date",\n                                value=min_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="summary_start_date"\n                            )'),
    
    (r'end_date = st\.date_input\(\s*"To Date",\s*value=max_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'end_date = st.date_input(\n                                "To Date",\n                                value=max_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="summary_end_date"\n                            )'),
    
    # Third set of date inputs (around line 1217)
    (r'start_date = st\.date_input\(\s*"From Date",\s*value=min_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'start_date = st.date_input(\n                                "From Date",\n                                value=min_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="explorer_start_date"\n                            )'),
    
    (r'end_date = st\.date_input\(\s*"To Date",\s*value=max_date,\s*min_value=min_date,\s*max_value=max_date\s*\)',
     'end_date = st.date_input(\n                                "To Date",\n                                value=max_date,\n                                min_value=min_date,\n                                max_value=max_date,\n                                key="explorer_end_date"\n                            )'),
]

# Apply all replacements
modified_content = content
for pattern, replacement in replacements:
    modified_content = re.sub(pattern, replacement, modified_content, count=1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("File updated successfully with unique keys for date_input components.")
