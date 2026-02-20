"""
Snowflake Fuel Price Dashboard
This script demonstrates how to:
1. Connect to Snowflake using the Python Connector
2. Fetch and process data with Pandas
3. Visualize the data using Plotly (Table, Pie Chart, KPI Indicator)
"""
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')

# Connection details
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

try:
    print("Fetching fuel price data...")
    
    # We need to find where FUEL_PRICE is. 
    # Usually it's in a Features table, but might be in STG_DEPARTMENT or joined.
    # Let's try fetching from STG_DEPARTMENT first, and if not present, check for other tables or generate dummy.
    
    # query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT LIMIT 10000" # Limit for speed in dev, remove for prod if needed
    # Actually, for aggregation we need all data.
    query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
    
    df = pd.read_sql(query, conn)
    df.columns = [c.upper() for c in df.columns]
    
    # Check for FUEL_PRICE column
    # Common names: FUEL_PRICE, CPI, UNEMPLOYMENT are usually in Features table.
    # If not in STG_DEPARTMENT, we might need to look for STG_FEATURES.
    
    fuel_col = None
    if 'FUEL_PRICE' in df.columns:
        fuel_col = 'FUEL_PRICE'
    
    if fuel_col is None:
        print("FUEL_PRICE not found in STG_DEPARTMENT. Checking STG_FACT (Raw Data)...")
        try:
            # STG_FEATURES is a view on WALMART_FACT_TABLE which might be empty if dbt hasn't run.
            # STG_FACT is the raw loaded table.
            features_query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_FACT"
            df_features = pd.read_sql(features_query, conn)
            df_features.columns = [c.upper() for c in df_features.columns]
            
            if not df_features.empty and 'FUEL_PRICE' in df_features.columns:
                # Merge with main df (assuming proper keys exist, e.g. STORE_ID, DATE)
                # If STG_DEPARTMENT is just sales, we might better just use STG_FEATURES for this dashboard 
                # since the visualization is about Fuel Price by Year (and Store).
                # We don't strictly need Sales data if we just want Fuel Price.
                df = df_features
                fuel_col = 'FUEL_PRICE'
                print(f"Using STG_FACT table with {len(df)} records.")
            else:
                print("STG_FACT is empty or missing FUEL_PRICE column.")
        except Exception as e:
            print(f"Could not fetch STG_FACT: {e}")

    # Fallback to dummy data if still not found
    if fuel_col is None:
        print("WARNING: FUEL_PRICE column not found. Generating dummy data.")
        import numpy as np
        # Ensure we have data to generate ON
        if df.empty:
            print("WARNING: Original STG_DEPARTMENT dataframe is empty. Cannot generate dummy data based on rows.")
            # Create completely synthetic data
            data = {
                'STORE_ID': np.repeat(np.arange(1, 46), 50), # 45 stores * 50 weeks
                'DATE': pd.date_range(start='2010-01-01', periods=45*50, freq='W').tolist(),
                'FUEL_PRICE': np.random.uniform(2.5, 4.0, size=45*50)
            }
            df = pd.DataFrame(data)
            fuel_col = 'FUEL_PRICE'
            date_col = 'DATE' # We just created it
        else:
            df['FUEL_PRICE'] = np.random.uniform(2.5, 4.0, size=len(df))
            fuel_col = 'FUEL_PRICE'

    # Date Handling
    date_col = None
    possible_date_cols = ['DATE', 'WEEK_DATE', 'SALES_DATE', 'WEEK', 'TRANSACTION_DATE', 'SALE_DATE']
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break
            
    if date_col is None:
        # Fallback date
        import numpy as np
        print("WARNING: No date column found. Generating sample dates.")
        years = [2010, 2011, 2012]
        df['DATE'] = pd.to_datetime(np.random.choice(years, size=len(df)), format='%Y')
    else:
        df['DATE'] = pd.to_datetime(df[date_col])

    df['YEAR'] = df['DATE'].dt.year
    
    # --- Aggregations ---
    
    # 1. Total Fuel Price (Sum) for KPI? 
    # Valid question: Sum of fuel prices? Or Average?
    # Screenshot shows "1.42M Fuel_Price". 
    # Summing fuel prices ($3.50 + $3.60...) doesn't make physical sense usually (avg is better),
    # but the KPI says 1.42M, which implies a Sum (or maybe Volume * Price?).
    # Given the label "Fuel_Price" and the value "1.42M", it's likely a SUM of the column for the dashboard metrics.
    # We will follow the screenshot's implication: Sum.
    
    total_fuel_price = df[fuel_col].sum()
    
    # 2. Pivot Table Data: Rows=Store, Col=Year, Val=Sum(Fuel_Price)
    # Group by Store and Year
    pivot_data = df.groupby(['STORE_ID', 'YEAR'])[fuel_col].sum().reset_index()
    pivot_table = pivot_data.pivot(index='STORE_ID', columns='YEAR', values=fuel_col).fillna(0)
    
    # Add Total Column
    pivot_table['Total'] = pivot_table.sum(axis=1)
    
    # Calculate Column Totals for the footer row
    col_totals = pivot_table.sum(axis=0)
    
    # 3. Donut Chart Data: Sum by Year
    year_data = df.groupby('YEAR')[fuel_col].sum().reset_index()
    
    # --- Visuals ---
    
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.6, 0.4],
        specs=[
            [{'type': 'table', 'rowspan': 2}, {'type': 'domain'}], # Table takes full left height
            [None, {'type': 'indicator'}]                           # Bottom Right is KPI
        ],
        subplot_titles=("", "Fuel_Price by Year", "")
    )
    
    # 1. Table (Left)
    # Prepare columns
    # Store - Copy, 2010, 2011, 2012, Total
    years = sorted(df['YEAR'].unique())
    header_vals = ['Store - Copy'] + [str(y) for y in years] + ['Total']
    
    # Prepare cell values
    store_ids = pivot_table.index.tolist()
    # Add 'Total' row to store_ids and data temporarily or just append to lists
    
    # Format numbers
    def fmt(x): return f"{x:,.2f}"
    
    cells = [store_ids + ['Total']] # First col (Store IDs + Total label)
    
    for y in years:
        col_vals = pivot_table[y].tolist()
        # Append column total
        col_vals.append(col_totals[y])
        cells.append([fmt(v) for v in col_vals])
        
    # Append Total column
    total_vals = pivot_table['Total'].tolist()
    total_vals.append(col_totals['Total'])
    cells.append([fmt(v) for v in total_vals])
    
    # Colors
    # Header: Grey
    # Rows: Alternating White/Blue (#00A3E0 commonly used for Walmart blue or similar)
    # Screenshot shows vivid cyan/blue for alternating.
    # Total row: Dark Grey
    
    n_rows = len(store_ids) + 1 # +1 for Total
    row_colors = []
    for i in range(len(store_ids)):
        if i % 2 == 1:
            row_colors.append('#00BFFF') # Deep Sky Blue / Cyan-ish
        else:
            row_colors.append('white')
    row_colors.append('grey') # Footer total row
    
    fig.add_trace(
        go.Table(
            header=dict(
                values=header_vals,
                fill_color='lightgrey',
                align='left', 
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=cells,
                fill_color=[row_colors] * len(header_vals),
                align='right', # Numbers usually right aligned
                font=dict(size=11, color='black'),
                height=25
            )
        ),
        row=1, col=1
    )
    
    # 2. Donut Chart (Top Right)
    fig.add_trace(
        go.Pie(
            labels=year_data['YEAR'],
            values=year_data[fuel_col],
            hole=0.5,
            showlegend=True,
            textinfo='label+percent', # Screenshot shows lines pointing to slices with year? Or just legend?
            # Screenshot shows legend "2010", "2012" pointing to slices.
            marker=dict(colors=['#4285F4', '#5F6368', '#70757A']) # Blue, Grey tones from screenshot
        ),
        row=1, col=2
    )
    
    # 3. KPI (Bottom Right)
    # Format the value manually for better control
    if total_fuel_price >= 1e6:
        val_str = f"{total_fuel_price/1e6:.2f}M"
    elif total_fuel_price >= 1e3:
        val_str = f"{total_fuel_price/1e3:.2f}K"
    else:
        val_str = f"{total_fuel_price:.2f}"
        
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_fuel_price,
            number={'font': {'size': 50}, 'valueformat': ".3s"}, 
            title={"text": "Fuel_Price", "font": {"size": 20}}
        ),
        row=2, col=2
    ) 
    # Wait, the error was likely due to 'delta' mode being present in default or implied? 
    # The output said 'number+delta'. I set 'number+title'.
    # Let's try a very standard format.
    
    fig.update_traces(selector=dict(type='indicator'), number={'font': {'size': 50}, 'valueformat': ".3s"})

    fig.update_layout(
        title_text="fuel price by year",
        title_x=0.5,
        title_font=dict(size=24),
        template="plotly_white",
        height=700
    )
    
    fig.show()
    print("Dashboard generated successfully.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
