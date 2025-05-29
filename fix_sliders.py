# Script to fix slider components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Add key to the first slider at around line 674
pattern1 = r'min_amount, max_amount = st\.slider\(\s*"Amount Range \(\$\)",\s*min_value=min_amt,\s*max_value=max_amt,\s*value=\(min_amt, max_amt\),\s*format="\$%.2f"\s*\)'
replacement1 = 'min_amount, max_amount = st.slider(\n                            "Amount Range ($)",\n                            min_value=min_amt,\n                            max_value=max_amt,\n                            value=(min_amt, max_amt),\n                            format="$%.2f",\n                            key="overview_amount_slider"\n                        )'

# Add key to the second slider at around line 1201
pattern2 = r'min_amount, max_amount = st\.slider\(\s*"Amount Range \(\$\)",\s*min_value=min_amt,\s*max_value=max_amt,\s*value=\(min_amt, max_amt\),\s*format="\$%.2f"\s*\)'
replacement2 = 'min_amount, max_amount = st.slider(\n                            "Amount Range ($)",\n                            min_value=min_amt,\n                            max_value=max_amt,\n                            value=(min_amt, max_amt),\n                            format="$%.2f",\n                            key="explorer_amount_slider"\n                        )'

# Add key to the third slider at around line 1901 if needed
pattern3 = r'values = st\.slider\(\s*f"{col} Range",\s*min_value=min_val,\s*max_value=max_val,\s*value=\(min_val, max_val\)'
replacement3 = 'values = st.slider(\n                        f"{col} Range",\n                        min_value=min_val,\n                        max_value=max_val,\n                        value=(min_val, max_val),\n                        key=f"range_slider_{col}"\n                    )'

# Perform the first replacement
modified_content = re.sub(pattern1, replacement1, content, count=1)

# Perform the second replacement on the already modified content
modified_content = re.sub(pattern2, replacement2, modified_content, count=1)

# Perform the third replacement if needed
modified_content = re.sub(pattern3, replacement3, modified_content, count=1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("File updated successfully.")
