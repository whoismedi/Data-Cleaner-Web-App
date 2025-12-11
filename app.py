from shiny.express import ui, input, render
from shiny import reactive
import pandas as pd
import io

raw_data = reactive.value(None)
cleaned_data = reactive.value(None)

ui.page_opts(title="Data Cleaner", fillable=True)

with ui.layout_sidebar():
    with ui.sidebar(width=300):
        ui.input_file("file", "Upload CSV file", accept=".csv")
        ui.input_action_button("analyze_btn", "Analyze")

        ui.hr()
        ui.input_selectize("drop_columns", "Remove Columns", choices=[], multiple=True)

        ui.input_select("nan_strategy", "With NaNs:",
                        choices=["No change", "Replace with 0", "Replace with mean", "Replace with median", "Drop rows"])
        
        ui.input_selectize("transform_columns", "Columns to transform", choices=[], multiple=True)
        ui.input_select("transform_strategy", "Transform Strategy:", choices=["No change", "Normalize (0/1)", "Standardize"], selected="No change")
        ui.hr()
        ui.input_action_button("clean_btn", "Clean")

        @render.download(filename="cleaned_data.csv", label="Download Cleaned Data")
        def download_csv():
            df = cleaned_data.get()
            if df is not None:
                with io.BytesIO() as buf: 
                    df.to_csv(buf, index=False, encoding='utf-8')
                    yield buf.getvalue()

        ui.input_action_button("reset_btn", "Reset")
        ui.input_dark_mode()

    with ui.navset_pill():
        with ui.nav_panel("Data"):

            # Triggered by file upload
            @reactive.effect
            @reactive.event(input.file)
            def load_file():
                fileinfo = input.file()
                if not fileinfo:
                    return
                try:
                    df = pd.read_csv(fileinfo[0]["datapath"])
                    raw_data.set(df)
                    cleaned_data.set(df.copy())

                    # Update the selectize input with the columns of the loaded DataFrame and reset the selected columns
                    ui.update_selectize("drop_columns", choices=df.columns.tolist(), selected=[]) 
                    ui.update_select("nan_strategy", selected="No change") # reset the strategy to default
                    ui.update_selectize("transform_columns", choices=df.select_dtypes(include='number').columns.tolist(), selected=[]) # reset the transform columns
                except Exception as e:
                    # show error message in ui
                    ui.notification_show(f"Error loading file: {e}", duration=5, type="error")

                    # reset data to None if file loading fails
                    raw_data.set(None)
                    cleaned_data.set(None)
                    ui.update_selectize("drop_columns", choices=[], selected=[])


            # Reset button
            @reactive.effect
            @reactive.event(input.reset_btn)
            def reset_all():
                df = raw_data.get()
                if df is not None:
                    cleaned_data.set(df.copy())
                    ui.update_selectize("drop_columns", selected=[])
                    ui.update_select("nan_strategy", selected="No change")
                    ui.update_selectize("transform_columns", selected=[])
                    ui.update_select("transform_strategy", selected="No change")

                # in case of no file loaded, reset cleaned_data to None
                else:
                    cleaned_data.set(None) 
                    ui.update_selectize("drop_columns", selected=[])
                    ui.update_select("nan_strategy", selected="No change")
                    ui.update_selectize("transform_columns", selected=[])
                    ui.update_select("transform_strategy", selected="No change")

            # Clean button
            @reactive.effect
            @reactive.event(input.clean_btn)
            def clean_data():
                # always work with a copy of the data so that the original data is not modified
                df = cleaned_data.get() 
                if df is None:
                    df_raw = raw_data.get() 
                    if df_raw is None:
                        return
                    df = df_raw.copy()
                else:
                    df = df.copy()

                cols_to_drop = input.drop_columns()
                if cols_to_drop:
                    existing_cols_to_drop = [col for col in cols_to_drop if col in df.columns] # check whether the columns to drop actually exist
                    if existing_cols_to_drop:
                        df = df.drop(columns=existing_cols_to_drop)
                 
                strategy = input.nan_strategy()
                numeric_cols = df.select_dtypes(include='number').columns # only select numeric columns

                if strategy == "Replace with 0":
                    df[numeric_cols] = df[numeric_cols].fillna(0) # only fill numeric columns
                elif strategy == "Replace with mean":
                    if not df[numeric_cols].empty: # ensures that there are actually numeric columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                elif strategy == "Replace with median":
                    if not df[numeric_cols].empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                elif strategy == "Drop rows":
                    df = df.dropna()

                # Transform
                cols_to_transform = input.transform_columns()
                transform_strategy = input.transform_strategy()

                if transform_strategy == "Normalize (0/1)":
                    if cols_to_transform:
                        for col in cols_to_transform:
                            if col in df.columns:
                                min_val = df[col].min()
                                max_val = df[col].max()
                                if max_val - min_val != 0:
                                    df[col] = (df[col] - min_val) / (max_val - min_val)
                elif transform_strategy == "Standardize":   
                    if cols_to_transform:
                        for col in cols_to_transform:
                            if col in df.columns:
                                mean = df[col].mean()
                                std = df[col].std()
                                if std != 0:
                                    df[col] = (df[col] - mean) / std
                cleaned_data.set(df)

            @render.data_frame
            def preview_cleaned():
                df = cleaned_data.get()
                if df is not None:
                    return df
                df_raw = raw_data.get() # show raw data if cleaned_data is None
                if df_raw is not None:
                    return df_raw 
                return pd.DataFrame() # return empty DataFrame if no data is loaded

                
        with ui.nav_panel("Analysis"):

            # Analyze button
            @render.data_frame
            @reactive.event(input.analyze_btn)
            def missing_summary():
                df = raw_data.get() if cleaned_data is None else cleaned_data.get()
                if df is not None:
                    na_counts = df.isnull().sum()
                    summary = pd.DataFrame({"Column": na_counts.index, "Missing values": na_counts.values,
                                            "Data type": df.dtypes.values, "Nr. of unique values": df.nunique().values})
                    return summary.sort_values(by="Missing values", ascending=False) 
                return pd.DataFrame()
