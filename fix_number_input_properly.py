# Script to properly fix number_input components by adding unique keys
file_path = r'c:\Users\ShahvaizZiaButt\PycharmProjects\EscalationsDashboard\pages\02_Deductions_Escalations.py'

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Fix the first number_input (incorrectly modified)
content = content.replace(
    'page_number = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1), key="summary_page_number")',
    'page_number = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1, key="summary_page_number")'
)

# Fix the second number_input if it was also incorrectly modified
content = content.replace(
    'page_number = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1), key="explorer_page_number")',
    'page_number = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1, key="explorer_page_number")'
)

# Save the corrected content
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Number input elements fixed correctly")
