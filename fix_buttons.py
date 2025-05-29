# Script to fix button elements by adding unique keys
file_path = r'c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py'

# Read the file line by line
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Find and fix the button elements
prev_button_fixed = False
next_button_fixed = False

for i in range(len(lines)):
    # Fix the first set of Previous/Next buttons
    if 'if st.button("◀ Previous"' in lines[i] and 'key=' not in lines[i]:
        if not prev_button_fixed:
            lines[i] = lines[i].replace('if st.button("◀ Previous", disabled=(page_number <= 1)):', 
                                      'if st.button("◀ Previous", disabled=(page_number <= 1), key="summary_prev_button"):')
            prev_button_fixed = True
        else:
            lines[i] = lines[i].replace('if st.button("◀ Previous", disabled=(page_number <= 1)):', 
                                      'if st.button("◀ Previous", disabled=(page_number <= 1), key="explorer_prev_button"):')
    
    # Fix the first set of Next buttons
    if 'if st.button("Next ▶"' in lines[i] and 'key=' not in lines[i]:
        if not next_button_fixed:
            lines[i] = lines[i].replace('if st.button("Next ▶", disabled=(page_number >= total_pages)):', 
                                      'if st.button("Next ▶", disabled=(page_number >= total_pages), key="summary_next_button"):')
            next_button_fixed = True
        else:
            lines[i] = lines[i].replace('if st.button("Next ▶", disabled=(page_number >= total_pages)):', 
                                      'if st.button("Next ▶", disabled=(page_number >= total_pages), key="explorer_next_button"):')

# Write the modified content back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("Button elements fixed successfully")
