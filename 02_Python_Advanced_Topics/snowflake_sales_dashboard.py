import snowflake.connector
import pandas as pd
import plotly.express as px

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connection details
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

# Pull the Star Schema data
query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
df = pd.read_sql(query, conn)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Visualization
if not df.empty:
    # Data Preparation
    df['IS_HOLIDAY'] = df['IS_HOLIDAY'].astype(str)
    
    # Aggregations
    total_sales = df['WEEKLY_SALES'].sum()
    sales_by_holiday = df.groupby('IS_HOLIDAY')['WEEKLY_SALES'].sum().reset_index()
    sales_by_store = df.groupby(['STORE_ID', 'IS_HOLIDAY'])['WEEKLY_SALES'].sum().reset_index()
    
    # Calculate total sales by store to determine sort order
    total_by_store = df.groupby('STORE_ID')['WEEKLY_SALES'].sum().reset_index()
    total_by_store = total_by_store.sort_values('WEEKLY_SALES', ascending=False)
    
    # Create ordered list of store IDs (highest sales first)
    store_order = total_by_store['STORE_ID'].tolist()

    # Create Subplots Layout
    # Row 1: Left=Pie, Right=Bar (Rowspan 2)
    # Row 2: Left=KPI, Right=(covered by Bar)
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.3, 0.7],
        row_heights=[0.5, 0.5],
        specs=[
            [{'type': 'domain'}, {'type': 'xy', 'rowspan': 2}],
            [{'type': 'indicator'}, None]
        ],
        subplot_titles=("Weekly Sales by IsHoliday", "Weekly Sales by Store and Holiday", "Total Weekly Sales")
    )

    # 1. Pie Chart (Top Left)
    fig.add_trace(
        go.Pie(
            labels=sales_by_holiday['IS_HOLIDAY'], 
            values=sales_by_holiday['WEEKLY_SALES'],
            name="Sales by Holiday",
            marker_colors=['#4285F4', '#DB4437'] # Example colors
        ),
        row=1, col=1
    )

    # 2. Bar Chart (Right Column)
    # We iterate to create group bars for True/False
    colors = {'FALSE': '#4285F4', 'TRUE': '#DB4437'} # Match Pie colors
    for holiday_status in sales_by_store['IS_HOLIDAY'].unique():
        subset = sales_by_store[sales_by_store['IS_HOLIDAY'] == holiday_status]
        fig.add_trace(
            go.Bar(
                x=subset['STORE_ID'], 
                y=subset['WEEKLY_SALES'],
                name=f"IsHoliday: {holiday_status}",
                marker_color=colors.get(holiday_status, 'gray'),
                text=subset['WEEKLY_SALES'].apply(lambda x: f'{x/1e6:.0f}M'), # Manual Python formatting
                textposition='outside', 
                cliponaxis=False, # Prevent labels from being cut off
                textfont=dict(size=16, color="black"),
                outsidetextfont=dict(size=16, color="black"),
                insidetextfont=dict(size=16, color="black")
            ),
            row=1, col=2
        )

    # 3. KPI Indicator (Bottom Left)
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_sales,
            title={"text": "Weekly Sales"},
            number={'prefix': "$", 'font': {'size': 50}}
        ),
        row=2, col=1
    )

    # Update Layout
    fig.update_layout(
        title_text="Weekly Sales by Store and Holiday",
        title_x=0.5,
        template="plotly_white",
        height=600,
        showlegend=True,
        barmode='group', # Key for side-by-side bars
        uniformtext=dict(minsize=16, mode='show') # Force text to be at least 16pt
    )
    
    # Update x-axis to use categorical ordering (preserves our sort order)
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=store_order,
        row=1, col=2
    )

    fig.show()
else:
    print("No data available to visualize.")
