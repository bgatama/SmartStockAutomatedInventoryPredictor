import pandas as pd

# Main function to run the demand analysis, calling all necessary steps in sequence
def run_demand_analysis(df_SH):
    df_grouped = group_by_product_ID(df_SH)
    df_grouped = add_sales_days(df_grouped, df_SH)
    df_grouped = calculate_observation_period(df_grouped)
    df_grouped = average_daily_demand(df_grouped)
    df_grouped = sales_frequency(df_grouped)
    df_grouped = demand_rate_per_active_day(df_grouped)

    return df_grouped


# This function groups the sales history data by Product_ID, calculating total quantity sold and first/last sale dates
def group_by_product_ID(df_SH):
    df_grouped = df_SH.groupby("Product_ID").agg(
        Total_Quantity_Sold=("Quantity_Sold", "sum"),
        First_Sale_Date=("Date", "min"),
        Last_Sale_Date=("Date", "max")
    ).reset_index()
    return df_grouped

# This function adds a column for the number of sales days per product, counting only days with actual sales, and handles products with no sales by filling NaN with 0.
def add_sales_days(df_grouped, df_SH):
    #Filter rows where sales actually happened
    df_active_sales = df_SH[df_SH["Quantity_Sold"] > 0]

    #Count number of sales days per product
    sales_days_df = df_active_sales.groupby("Product_ID").size().reset_index(name="Sales_Days")

    #Merge with grouped dataframe
    df_grouped = df_grouped.merge(sales_days_df, on="Product_ID", how="left")

    #Handle products with no sales (NaN → 0)
    df_grouped["Sales_Days"] = df_grouped["Sales_Days"].fillna(0).astype(int)

    return df_grouped

# This function calculates the observation period in days for each product, defined as the number of days between the first and last sale date, inclusive. It also checks for any products with non-positive observation periods and raises an error if found.
def calculate_observation_period(df_grouped):
    first_sale_date = df_grouped["First_Sale_Date"]
    last_sale_date = df_grouped["Last_Sale_Date"]
    df_grouped["Observation_Period_Days"] = (last_sale_date - first_sale_date).dt.days + 1
    
    if (df_grouped["Observation_Period_Days"] <= 0).any():
        raise ZeroDivisionError("Error: Observation period days must be greater than zero for all products.")
    return df_grouped 

# This function calculates the sales frequency for each product, defined as the ratio of sales days to observation period days, and adds it as a new column to the dataframe.
def sales_frequency(df_grouped):
    df_grouped["Sales_Frequency"] = df_grouped["Sales_Days"] / df_grouped["Observation_Period_Days"]
    return df_grouped

# This function calculates the average daily demand for each product, by dividing the total quantity sold with the observation period days
def average_daily_demand(df_grouped):
    df_grouped["Average_Daily_Demand"] = df_grouped["Total_Quantity_Sold"]/df_grouped["Observation_Period_Days"]
    return df_grouped

# This function calculates the demand rate per active day for each product, and handles 0 values        
def demand_rate_per_active_day(df_grouped):
    df_grouped["Demand_Rate_Per_Active_Day"] = (
        df_grouped["Total_Quantity_Sold"]/df_grouped["Sales_Days"]
    )

    df_grouped["Demand_Rate_Per_Active_Day"] = df_grouped["Demand_Rate_Per_Active_Day"].replace([float('inf'), float('-inf')], 0)
    df_grouped["Demand_Rate_Per_Active_Day"] = df_grouped["Demand_Rate_Per_Active_Day"].fillna(0)
    
    return df_grouped




#columns present: total_quantity_sold, first_sale_date, last_sale_date, observation_period, Sales_Frequency, Average_Daily_Demand, Demand_Rate_Per_Active_Day