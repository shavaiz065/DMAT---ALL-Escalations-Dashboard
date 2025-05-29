import os
import shutil

# Define paths
source_file = "EscalationsDashboard.py"
target_file = os.path.join("pages", "01_Escalations_Dashboard.py")

# Copy the file
shutil.copy2(source_file, target_file)

print(f"Successfully copied {source_file} to {target_file}")
print("Multi-page application setup is complete!")
print("You can now run the application with: streamlit run Home.py")
