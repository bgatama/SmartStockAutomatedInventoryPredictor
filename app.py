from src.data_loader import get_clean_data
from src.demand_analysis import run_demand_analysis
from src.reorder_point import run_reorder_point_analysis
from src.stock_depletion import run_stock_depletion_analysis
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui 
import plotly.express as px


st.set_page_config(layout="wide", page_title="SmartStock Inventory Reorder Predictor", page_icon="📊")

def main():
    create_sidebar()

def create_sidebar():
    with st.sidebar:
        side_bar = option_menu(
            menu_title="Main Menu",
            options=["Dashboard", "Results"],
            icons=["house", "bar-chart"],
            menu_icon="cast",
            styles={
                "nav-link-selected": {"background-color": "#0068c9"}
            }
        )


    uploaded_sales_files, uploaded_inventory_file = upload_data()
    if uploaded_sales_files is None or uploaded_inventory_file is None:
        if side_bar != "Upload Data":
            st.warning("Please upload both Sales History and Inventory Data to view the Dashboard and Results.")
        return
    
    # Load and validate data
    try:
        df_SH, df_IN = get_clean_data(uploaded_sales_files, uploaded_inventory_file)

    except Exception as e:
        st.error(str(e))
        return
    
    df_grouped = run_demand_analysis(df_SH)
    df_merged_IN_demand = run_reorder_point_analysis(df_grouped, df_IN)
    df_merged = run_stock_depletion_analysis(df_grouped, df_IN)

    if side_bar == "Dashboard":
        st.markdown(
            "<h1 style='font-size: 34px;'>Dashboard</h1>",
            unsafe_allow_html=True
        )
        st.write("View your inventory and sales history data to get insights into your stock levels and demand patterns.")
        create_dashboard(df_SH, df_IN)
    elif side_bar == "Results":
        st.markdown(
            "<h1 style= 'font-size: 34px;'>Results</h1>",
            unsafe_allow_html=True
        )
        st.write("View your product demand, stock depletion, and reorder point results to make decisions on whether to reorder now or later.")
        safe, moderate, critical = count_pie_chart_values_stock_depletion(df_merged)
        display_results(df_merged_IN_demand, df_merged, safe, moderate, critical)
        


def upload_data():
    uploaded_sales_file = st.file_uploader("Upload Sales History Data (CSV)", type=["csv"], key="sales_history_uploader")
    uploaded_inventory_file = st.file_uploader("Upload Inventory Data (CSV)", type=["csv"], key="inventory_data_uploader")

    if uploaded_sales_file is not None and uploaded_inventory_file is not None:    
         st.success("Files uploaded successfully! You can now view the results in the Results section.")

    return uploaded_sales_file, uploaded_inventory_file

def create_dashboard(df_SH, df_IN):
    total_units_sold = df_SH["Quantity_Sold"].sum()
    total_current_stock = df_IN["Current_Stock"].sum()
    total_number_of_products = df_IN["Product_Name"].nunique()
    col1, col2, col3 = st.columns(3)

    with col1:
        ui.metric_card(
            title="Total Units Sold",
            content=str(total_units_sold),
            description= "Total quantity of products sold based on the uploaded sales history data.",
            key="card1"
        )
    with col2:
        ui.metric_card(
            title="Total Current Stock",
            content=str(total_current_stock),
            description= "Total quantity of products currently in stock based on the uploaded inventory data.",
            key="card2"
        )
    with col3:
        ui.metric_card(
            title="Total Number of Products",
            content=str(total_number_of_products),
            description= "Total number of unique products based on the uploaded inventory data.",
            key="card3"
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h1 style= 'font-size: 28px;'>Sales History Data</h1>",
            unsafe_allow_html=True
        )
        st.dataframe(df_SH.head(), use_container_width=True)
    with col2:
        st.markdown(
            "<h1 style= 'font-size: 28px;'>Inventory Data</h1>",
            unsafe_allow_html=True
        )
        st.dataframe(df_IN.head(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h1 style= 'font-size:28px;'> Total Quantity Sold</h1>",
            unsafe_allow_html=True
        )
        st.bar_chart(df_IN.groupby("Product_Name")["Current_Stock"].sum(), x_label="Product Name", y_label="Current Stock")
    with col2:
        st.markdown(
            "<h1 style= 'font-size:28px;'> Sales History</h1>",
            unsafe_allow_html=True
        )
        st.bar_chart(df_SH.groupby("Product_ID")["Quantity_Sold"].sum(), x_label="Product ID", y_label="Total Quantity Sold")


    data_figure = px.pie(df_IN, names="Product_Name", values="Supplier_Lead_Time(days)", title="Supply Lead Time Distribution")
    st.plotly_chart(data_figure, use_container_width=True)
    

def display_results(df_merged_IN_demand, df_merged, safe, moderate, critical):
    st.markdown(
        "<h1 style= 'font-size: 28px;'>Product Demand</h1>",
        unsafe_allow_html=True
    )
    st.dataframe(df_merged_IN_demand[["Product_Name", "Average_Daily_Demand", "Sales_Frequency", "Demand_Rate_Per_Active_Day"]].head())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h1 style= 'font-size: 28px;'> Reorder Point</h1>",
            unsafe_allow_html=True
        )
        df_needed_columns = df_merged_IN_demand[["Product_Name", "Reorder_Point", "Reorder_Needed"]]
        df_merged_colored = df_needed_columns.style.map(lambda x: f"background-color: {'#2ecc71' if x == 'No' else '#e74c3c'}", subset=["Reorder_Needed"])
        st.dataframe(df_merged_colored)

    with col2:
        st.markdown(
            "<h1 style= 'font-size: 28px;'> Stock Depletion</h1>",
            unsafe_allow_html=True
        )
        df_needed_columns_2 = df_merged[["Product_Name", "days_until_stock_depletes", "stock_depletion_risk"]]
        df_merged_colored_2 = df_needed_columns_2.style.map(lambda x: f"background-color: {'#2ecc71' if x == 'Safe' else '#f1c40f' if x =='Moderate' else '#e74c3c'}", subset=["stock_depletion_risk"])
        st.dataframe(df_merged_colored_2)

    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h1 style= 'font-size: 20px;'> Stockout Risk (Days until Stockout)</h1>",
            unsafe_allow_html=True

        )
        bar_chart_figure = px.bar(df_merged, x="Product_Name", y="days_until_stock_depletes", labels={"Product_Name": "Product Name", "days_until_stock_depletes": "Days"})
        st.plotly_chart(bar_chart_figure, use_container_width=True)
    with col2:
        labels = ["Safe", "Moderate", "Critical"]
        color_map ={
                "Safe": "#2ecc71",
                "Moderate": "#f1c40f",
                "Critical": "#e74c3c"
            }
          
        values = [safe, moderate, critical]

        data_figure_2 = px.pie(names=labels, values=values, color=labels, color_discrete_map=color_map, title="Stock Depletion Risk Distribution")
        st.plotly_chart(data_figure_2, use_container_width=True)

def count_pie_chart_values_stock_depletion(df_merged):
    safe = (df_merged["stock_depletion_risk"] =="Safe").sum()
    moderate = (df_merged["stock_depletion_risk"] == "Moderate").sum()
    critical = (df_merged["stock_depletion_risk"] == "Critical").sum()
    return safe, moderate, critical


if __name__ == "__main__":
    main()

