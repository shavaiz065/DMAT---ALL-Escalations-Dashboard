# Script to fix plotly_chart components by adding unique keys
import re

file_path = r"c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py"

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Find all plotly_chart occurrences
plotly_chart_pattern = r'st\.plotly_chart\(([\w\d_]+),\s*use_container_width=True\)'
matches = re.finditer(plotly_chart_pattern, content)

# Prepare replacements with unique keys
modified_content = content
counter = 0

for match in re.finditer(plotly_chart_pattern, content):
    counter += 1
    chart_var = match.group(1)
    old_text = match.group(0)
    
    # Create a unique key based on the chart variable name and counter
    new_text = f'st.plotly_chart({chart_var}, use_container_width=True, key="{chart_var}_chart_{counter}")'
    
    # Replace only this occurrence
    modified_content = modified_content.replace(old_text, new_text, 1)

# Save the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print(f"Added unique keys to {counter} plotly_chart components.")
