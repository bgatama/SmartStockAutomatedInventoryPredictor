import pandas as pd

# Define expected columns for both datasets
expected_columns_inventory_data = ["Product_Name", "Product_ID", "Current_Stock", "Supplier_Lead_Time(days)", "Safety_Stock"]
expected_columns_sales_history = ["Date", "Product_ID", "Quantity_Sold"]


# Main function to load and validate data, returning cleaned DataFrames
def get_clean_data(uploaded_sales_file, uploaded_inventory_file):
    df_SH, df_IN = load_data(uploaded_sales_file, uploaded_inventory_file)
    validate_expected_columns(df_SH, df_IN)
    df_SH, df_IN = validate_numeric_values(df_SH, df_IN)
    df_SH = validate_date(df_SH)

    return df_SH, df_IN


# Data loading functions for Sales History and Inventory Data
def load_sales_history_sample(uploaded_sales_file):
    try:
        return pd.read_csv(uploaded_sales_file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: Sales_History_Sample.csv not found.") 
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("Error: Sales_History_Sample.csv is empty.")
    

def load_inventory_data_sample(uploaded_inventory_file):
    try:
        return pd.read_csv(uploaded_inventory_file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: Inventory_Data_Sample.csv not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("Error: Inventory_Data_Sample.csv is empty.")


# Main function to load both datasets assigned to variables
def load_data(uploaded_sales_file, uploaded_inventory_file):
    df_SH = load_sales_history_sample(uploaded_sales_file)
    df_IN = load_inventory_data_sample(uploaded_inventory_file)

    return df_SH, df_IN


# Ensure that the loaded data contains the expected columns, and if not, raise an error
def validate_expected_columns(df_SH, df_IN):
    list_of_missing_columns_IN = []
    list_of_missing_columns_SH = []

    
   
    for col in expected_columns_inventory_data:
        if col not in df_IN.columns:
            list_of_missing_columns_IN.append(col)
            
    for col in expected_columns_sales_history:
        if col not in df_SH.columns:
            list_of_missing_columns_SH.append(col)
        
    if list_of_missing_columns_IN:
        raise ValueError(f"Error: Missing columns in Inventory Data: {list_of_missing_columns_IN}")

    if list_of_missing_columns_SH:
        raise ValueError(f"Error: Missing columns in Sales History Data: {list_of_missing_columns_SH}")


# Validate that numeric columns contain valid numeric values and are non-negative, and if not, raise an error
def validate_numeric_values(df_SH, df_IN):

    numeric_columns_IN = ["Current_Stock","Supplier_Lead_Time(days)","Safety_Stock"]
    numeric_columns_SH = ["Quantity_Sold"]



    for col in numeric_columns_IN:
        df_IN[col] = pd.to_numeric(df_IN[col], errors='coerce')

        if df_IN[col].isnull().any():
            raise ValueError(f"Error: Non-numeric values found in column '{col}' of inventory data after coercion.")
        if (df_IN[col] < 0).any():
            raise ValueError(f"Error: Non-positive values found in column '{col}' of inventory data.")

    for col in numeric_columns_SH:
        df_SH[col] = pd.to_numeric(df_SH[col], errors='coerce')

        if df_SH[col].isnull().any():
            raise ValueError(f"Error: Non-numeric values found in column '{col}' of sales history data after coercion.")
        if (df_SH[col] < 0).any():
            raise ValueError(f"Error: Non-positive values found in column '{col}' of sales history data.")
    
    return df_SH, df_IN

def validate_date(df_SH):

    try:
        if df_SH['Date'].isna().any():
            raise ValueError(f"Error: Missing values found in column 'Date' of sales history data.")
        
                    
        converted_column = pd.to_datetime(df_SH['Date'], errors='coerce')
        invalid_rows = converted_column.isna() & df_SH['Date'].notna()

        if invalid_rows.any():
            raise ValueError(f"Error: Invalid date formats found in column 'Date' of sales history data.")

        df_SH['Date'] = converted_column
        return df_SH

    except KeyError:
        raise ValueError("Error: 'Date' column is missing from sales history data.")

