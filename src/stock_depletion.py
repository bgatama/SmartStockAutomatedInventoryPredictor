from src.demand_analysis import run_demand_analysis
import pandas as pd
import numpy as np


def run_stock_depletion_analysis(df_grouped, df_IN):
    df_merged = merge_demand_with_inventory(df_grouped, df_IN)
    validate_merging(df_IN, df_merged)
    df_merged = calculate_stock_depletion(df_merged)
    df_merged = classify_stock_depletion_risk(df_merged)

    return df_merged 


# Merging demand analysis + Inventory data
def merge_demand_with_inventory(df_grouped, df_IN):
    if df_grouped["Product_ID"].duplicated().any():
        raise ValueError("Error: Merging resulted in duplicate Product_IDs, it is not aggregated properly. Please check the data and merging logic.")
    else:
        df_merged_IN_demand = df_IN.merge(df_grouped, on="Product_ID", how="left")
        return df_merged_IN_demand


# This function will validate how the merging of the demand analysis and inventory results went. 
def validate_merging(df_IN, df_merged_IN_demand):
   expected_number_of_rows = len(df_IN)

   if len(df_merged_IN_demand) != expected_number_of_rows:
       raise ValueError("Error: Merging resulted in faulty number of rows.")
   elif (df_merged_IN_demand["Average_Daily_Demand"].isna().sum()) > 0:     
       raise ValueError("Error: Merging resulted in Nan values, which is not applicable.")
       
       

# This function calculates the stock depletion, ensuring that when the value is 0 it is properly handled
def calculate_stock_depletion(df_merged_IN_demand):
    df_merged_IN_demand["days_until_stock_depletes"] = np.where(
        df_merged_IN_demand["Average_Daily_Demand"] > 0, 
        df_merged_IN_demand["Current_Stock"] / df_merged_IN_demand["Average_Daily_Demand"],
        np.inf
    )
    return df_merged_IN_demand


# This function basically classifies the risk of stock depletion based on the calculated days until stock depletes.
def classify_stock_depletion_risk(df_merged_IN_demand):
    conditions = [
        (df_merged_IN_demand["days_until_stock_depletes"] < 7) & (df_merged_IN_demand["days_until_stock_depletes"] > 0),
        (df_merged_IN_demand["days_until_stock_depletes"] >= 7) & (df_merged_IN_demand["days_until_stock_depletes"] <= 30),
        (df_merged_IN_demand["days_until_stock_depletes"] >= 30),
    ]
    choices = [
        "Critical",
        "Moderate",
        "Safe"
    ]

    df_merged_IN_demand["stock_depletion_risk"] = np.select(conditions, choices, default="No Demand")

    return df_merged_IN_demand





