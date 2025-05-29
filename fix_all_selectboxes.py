# Script to fix all remaining selectbox components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Fix the specific selectbox at line 1483
selectbox_pattern = r'sort_by = st\.selectbox\(\s*"Sort transactions by",\s*options=available_columns,\s*index=0 if available_columns else 0\s*\)'
replacement = 'sort_by = st.selectbox(\n                                "Sort transactions by",\n                                options=available_columns,\n                                index=0 if available_columns else 0,\n                                key="explorer_transactions_sort_by"\n                            )'

modified_content = re.sub(selectbox_pattern, replacement, content, count=1)

# Find all other selectbox patterns that don't have a key parameter
matches = re.finditer(r'(\w+)\s*=\s*st\.selectbox\((.*?)\)', modified_content, re.DOTALL)

counter = 0
for match in matches:
    var_name = match.group(1)
    params = match.group(2)
    
    # Check if this selectbox already has a key parameter
    if not re.search(r'key\s*=', params):
        counter += 1
        # Add a unique key parameter
        old_text = f"{var_name} = st.selectbox({params})"
        if params.strip().endswith(')'):  # If params already ends with ')'
            new_params = params[:-1] + f', key="{var_name}_auto_key_{counter}")'
        else:
            new_params = params + f', key="{var_name}_auto_key_{counter}"'
        new_text = f"{var_name} = st.selectbox({new_params})"
        modified_content = modified_content.replace(old_text, new_text, 1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"Fixed the specific selectbox and added keys to {counter} other selectbox components.")
