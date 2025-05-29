# Script to fix selectbox components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Find and replace the first sort_by selectbox (line ~954)
pattern1 = r'sort_by = st\.selectbox\(\s*"Sort by",\s*sort_options,\s*index=0\s*\)'
replacement1 = 'sort_by = st.selectbox(\n                                "Sort by",\n                                sort_options,\n                                index=0,\n                                key="summary_sort_by"\n                            )'

# Find and replace the first page_size selectbox (line ~964)
pattern2 = r'page_size = st\.selectbox\("Rows per page", \[10, 25, 50, 100\], index=0\)'
replacement2 = 'page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=0, key="summary_page_size")'

# Find and replace the second sort_by selectbox (line ~1484)
pattern3 = r'sort_by = st\.selectbox\(\s*"Sort by",\s*sort_options,\s*index=0\s*\)'
replacement3 = 'sort_by = st.selectbox(\n                                "Sort by",\n                                sort_options,\n                                index=0,\n                                key="explorer_sort_by"\n                            )'

# Find and replace the second page_size selectbox (line ~1494)
pattern4 = r'page_size = st\.selectbox\("Rows per page", \[10, 25, 50, 100\], index=0\)'
replacement4 = 'page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=0, key="explorer_page_size")'

# Apply all replacements
modified_content = content
modified_content = re.sub(pattern1, replacement1, modified_content, count=1)
modified_content = re.sub(pattern2, replacement2, modified_content, count=1)
modified_content = re.sub(pattern3, replacement3, modified_content, count=1)
modified_content = re.sub(pattern4, replacement4, modified_content, count=1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("File updated successfully with unique keys for selectbox components.")
