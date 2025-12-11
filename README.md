*Data Cleaner Web App where users can upload a CSV file, analyze missing values, remove columns, handle missing data, transform numerical columns, and download the cleaned dataset.*

With this app you can: 

- Upload a .csv file and preview the dataset.
- Display dataset statistics after clicking Analyze: Missing values per column (sorted descending).
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
Remove columns
Handle missing values
Transform numerical columns
- Download cleaned data as cleaned_data.csv.
- Reset app to original uploaded data.
- Switch do dark mode.



Run the App Locally

1. Install dependencies
Make sure you have Python 3.10+ and run:
pip install shiny pandas numpy plotly

2. Install the VS Code Shiny extension for easy local execution.

4. Run the app
   shiny run --reload --launch-browser --port=0 app.py

4. Interaction Notes
If an unsupported file type is uploaded, the app shows:
"Error loading file: error_message" for 5 seconds.
Clean and Reset do nothing until a dataset is uploaded.
If the user downloads without uploading data, the app returns an empty dataframe.




