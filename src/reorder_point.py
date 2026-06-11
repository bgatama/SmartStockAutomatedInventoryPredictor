from src.demand_analysis import run_demand_analysis
from src.stock_depletion import merge_demand_with_inventory
import pandas as pd
import numpy as np

# Main function to run the reorder point analysis, calling all necessary steps in sequence
def run_reorder_point_analysis(df_grouped, df_IN):
    df_merged_IN_demand = merge_demand_with_inventory(df_grouped, df_IN)
    df_merged_IN_demand = calculate_reorder_point(df_merged_IN_demand)
    df_merged_IN_demand = flag_reorder_needed(df_merged_IN_demand)

    return df_merged_IN_demand

# This functions calculates the reorder point for each product, by: (Average Daily Demand * Supplier Lead Time) + Safety Stock
def calculate_reorder_point(df_merged_IN_demand):
    demand_during_lead_time = df_merged_IN_demand["Average_Daily_Demand"] * df_merged_IN_demand["Supplier_Lead_Time(days)"]
    df_merged_IN_demand["Reorder_Point"] = demand_during_lead_time + df_merged_IN_demand["Safety_Stock"]
    return df_merged_IN_demand

# This function flags whether a reorder is needed based on the calculated reorder point and current stock levels 
def flag_reorder_needed(df_merged_IN_demand):
    df_merged_IN_demand["Reorder_Needed"] = np.where(
        df_merged_IN_demand["Current_Stock"] <= df_merged_IN_demand["Reorder_Point"],
        "Yes",
        "No"
    )
    return df_merged_IN_demand