import re

file_path = r'c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py'

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Fix radio buttons that are causing the errors
content = re.sub(
    r'sort_order = st\.radio\("Order", \["Descending", "Ascending"\], horizontal=True\)',
    r'sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True, key="summary_sort_order")',
    content, count=1
)

content = re.sub(
    r'sort_order = st\.radio\("Order", \["Descending", "Ascending"\], horizontal=True\)',
    r'sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True, key="explorer_sort_order")',
    content, count=1
)

# Add keys to other Streamlit elements that might cause issues in the future
# Radio buttons
content = re.sub(
    r'(st\.radio\([^,]+)(?!\s*,\s*key=)(\))',
    r'\1, key="radio_\2"',
    content
)

# Multiselect
content = re.sub(
    r'(st\.multiselect\([^,]+)(?!\s*,\s*key=)(\))',
    r'\1, key="multiselect_\2"',
    content
)

# Selectbox
content = re.sub(
    r'(st\.selectbox\([^,]+)(?!\s*,\s*key=)(\))',
    r'\1, key="selectbox_\2"',
    content
)

# Slider
content = re.sub(
    r'(st\.slider\([^,]+)(?!\s*,\s*key=)(\))',
    r'\1, key="slider_\2"',
    content
)

# Date Input
content = re.sub(
    r'(st\.date_input\([^,]+)(?!\s*,\s*key=)(\))',
    r'\1, key="date_input_\2"',
    content
)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Fixed all Streamlit elements by adding unique keys")
