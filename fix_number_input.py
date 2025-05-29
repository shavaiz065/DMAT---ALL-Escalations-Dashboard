# Script to fix number_input components by adding unique keys
file_path = r'c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py'

# Read the file line by line
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Fix the first number_input at line 977
for i in range(len(lines)):
    if 'page_number = st.number_input("Page"' in lines[i] and 'key=' not in lines[i]:
        if i < 1000:  # First occurrence (around line 977)
            lines[i] = lines[i].strip() + ', key="summary_page_number")\n'
        else:  # Second occurrence (around line 1507)
            lines[i] = lines[i].strip() + ', key="explorer_page_number")\n'

# Write the corrected content back
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("Number input elements fixed successfully")
