# Script to fix multiselect components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Define patterns to match multiselect components without keys
pattern1 = r'status_filter = st\.multiselect\(\s*"Transaction Status",\s*options=status_options,\s*default=\[\]\s*\)'
pattern2 = r'provider_filter = st\.multiselect\(\s*"Provider",\s*options=provider_options,\s*default=default_provider\s*\)'

# Replace with versions that include unique keys
replacement1 = 'status_filter = st.multiselect(\n                            "Transaction Status",\n                            options=status_options,\n                            default=[],\n                            key="explorer_status_filter"\n                        )'
replacement2 = 'provider_filter = st.multiselect(\n                            "Provider",\n                            options=provider_options,\n                            default=default_provider,\n                            key="explorer_provider_filter"\n                        )'

# Perform replacements (only on the first occurrence to avoid multiple replacements)
modified_content = re.sub(pattern1, replacement1, content, count=1)
modified_content = re.sub(pattern2, replacement2, modified_content, count=1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("File updated successfully.")
