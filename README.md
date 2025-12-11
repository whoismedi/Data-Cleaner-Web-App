*Data Cleaner Web App where users can upload a CSV file, analyze missing values, remove columns, handle missing data, transform numerical columns, and download the cleaned dataset.*

With this app you can: 

- Upload a .csv file and preview the dataset.
  <img width="736" height="604" alt="Screenshot 2025-12-11 at 12 04 32" src="https://github.com/user-attachments/assets/0b4777fb-d821-4468-9cd2-efb8a0603674" />

- Display dataset statistics after clicking Analyze: Missing values per column (sorted descending).
  <img width="736" height="604" alt="Screenshot 2025-12-11 at 12 05 11" src="https://github.com/user-attachments/assets/c66c61a1-01eb-4a17-a0c1-bc2f5eca13e8" />

- Remove selected columns via a multi-select dropdown.
- Handle missing values in different ways:
No change (default)
Replace with 0
Replace with mean (numeric columns only)
Replace with median (numeric columns only)
Drop rows with missing values
- Transform numerical columns:
Normalize (0–1)
Standardize (mean 0, std 1)
- Apply all modifications in this order:
Remove columns ->
Handle missing values ->
Transform numerical columns
<img width="736" height="604" alt="Screenshot 2025-12-11 at 12 05 46" src="https://github.com/user-attachments/assets/fcdcdcff-2f39-4448-9cfd-a0cc05b2aa60" />

- Download cleaned data as cleaned_data.csv.
- Reset app to original uploaded data.
- Switch do dark mode.

**Run the App Locally**

1. Install dependencies
Make sure you have Python 3.10+ and run:
pip install shiny pandas numpy plotly

2. Install the VS Code Shiny extension for easy local execution.
   
3. For each of the apps create a directory (e.g. cleaner_app) which contains the app script, that
has the name app.py. This is so you can run it most easily directly in VS Code as it
automatically then recognizes the script as an app.

5. Run the app
   shiny run --reload --launch-browser --port=0 app.py

Interaction Notes:
   
If an unsupported file type is uploaded, the app shows:
"Error loading file: error_message" for 5 seconds.
Clean and Reset do nothing until a dataset is uploaded.
If the user downloads without uploading data, the app returns an empty dataframe.


<img width="736" height="604" alt="Screenshot 2025-12-11 at 12 06 31" src="https://github.com/user-attachments/assets/a9082865-accc-4be8-bbf5-d3918eecf484" />





