# Script to fix the syntax error in the Deductions Dashboard file
file_path = r'c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py'

# Read the file line by line
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Fix the line with syntax error
for i in range(len(lines)):
    if 'Amount Range ($, key=' in lines[i]:
        lines[i] = '                            "Amount Range ($)",\n'

# Write the corrected content back
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("Syntax error fixed successfully")
