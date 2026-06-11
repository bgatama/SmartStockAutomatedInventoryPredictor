## SmartStock Automated Inventory Predictor

## Description:

- This program allows business owners to upload their sales history CSV file and there inventory data CSV file to get an insight of how each product in the inventory of the business is performing.

## Features:
- Demand Analysis
- Stock Depletion Analysis
- Getting Reorder Point
- Stockout Risk Analysis

## Requirements:
- Python 3.10+
- pip

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Technologies Used:
- Python
- Pandas (pip install pandas)
- Streamlit (pip install streamlit)
- Plotly (pip install Plotly)

## Project Structure(main folders and main files):
    
```text
    SmartStock Automated Inventory Predictor/
    |
    |
    |── data/
    |    |─Inventory_Data_Sample.csv
    |    |─Sales_History_Sample.csv
    |
    |
    |──src/
    |    |─__init__.py
    |    |─data_loader.py
    |    |─demand_analysis.py
    |    |─reorder_point.py
    |    |─stock_depletion.py
    |
    |
    |──app.py
    |──README.md
    |──requirements.txt
```

## Live Demo:
    .....

## Screenshots:
    ......

## About the Project:
    ## Different file types and what they do:
        There is 5 main files in this whole project, 4 of these files perform the backend calculations while the remaining file displays the UI elements of the project using streamlit plus other libraries.

            ## files under the src folder(these are the files that perform the backend calculations):
                - data_loader.py: This file loads the CSV file ensuring that the CSV file is converted to a dataframe. This file has several functions which ensure that the loaded CSV file doesn't have any missing columns, values, Nan Values etc. It ensures that the loaded CSV file doesn't miss anything that may cause calculation problems later on in other operations i.e demand analysis, stock depletion and getting reorder point.

                - demand_analysis.py: This file does the demand analysis operation from the loaded dataframe it ensures that the dataframe is grouped by the product id, so that each calculation in the demand analysis section can be done accurately. The operations perfomed in demand analysis may include: getting sales frequency, average daily demand, demand rate per active day, calculating the observation period and adding the sales days.

                - reorder_point.py: This file simply calculates the reorder point and flags whether reorder is needed by output either "Yes" or "No". The calculation for getting reorder point is: (Average Daily Demand * Supplier Lead Time) + Safety Stock

                - stock_depletion.py: This file merges demand analysis and inventory data, validating that the merging wasnt faulty. The main operations of this file is that it calculates stock depletion, obtains how many days that the stock will deplete and lastly it classifys the stock depletion risk based on the amount of days left until the stock depletes(The classifications include: Critical, Moderate and Safe)
            

            ## app.py file:
                - app.py: This file displays the UI element of this whole project. It creates the interactable interface allowing the user to upload the desired CSV files and view statistical data, that show how the business stock/inventory levels are performing. It primarily displays the results needed to observe the business operations.
            

        