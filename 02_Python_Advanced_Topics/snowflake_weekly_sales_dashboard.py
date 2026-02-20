import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv
import calendar

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
    print("Fetching weekly sales data...")
    query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
    df = pd.read_sql(query, conn)
    df.columns = [c.upper() for c in df.columns]
    
    if df.empty:
        print("WARNING: STG_DEPARTMENT is empty. Cannot generate dashboard.")
    else:
        # Date Handling
        date_col = None
        possible_date_cols = ['SALE_DATE', 'DATE', 'WEEK_DATE', 'TRANSACTION_DATE']
        for col in possible_date_cols:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            df['DATE'] = pd.to_datetime(df[date_col])
        else:
            print("WARNING: No date column found. Generating dummy dates.")
            # Generate sample dates covering a few years
            import numpy as np
            dates = pd.date_range(start='2010-02-05', end='2012-11-01', freq='W')
            df['DATE'] = np.random.choice(dates, size=len(df))

        # Extract Date Parts
        df['YEAR'] = df['DATE'].dt.year
        df['MONTH'] = df['DATE'].dt.month
        df['MONTH_NAME'] = df['DATE'].dt.month_name()
        df['DAY'] = df['DATE'].dt.day
        
        # Aggregations
        # 1. By Year
        sales_by_year = df.groupby('YEAR')['WEEKLY_SALES'].sum().reset_index()
        
        # 2. By Month
        sales_by_month = df.groupby(['MONTH', 'MONTH_NAME'])['WEEKLY_SALES'].sum().reset_index()
        sales_by_month.sort_values('MONTH', inplace=True)
        
        # 3. By Day
        sales_by_day = df.groupby('DAY')['WEEKLY_SALES'].sum().reset_index()
        
        # Visuals
        fig = make_subplots(
            rows=2, cols=2,
            specs=[
                [{'type': 'xy'}, {'type': 'xy'}], # Row 1: Year, Month
                [{'type': 'xy', 'colspan': 2}, None] # Row 2: Day (Span 2 cols)
            ],
            subplot_titles=("Weekly_Sales by Year", "Weekly_Sales by Month", "Weekly_Sales by Day"),
            vertical_spacing=0.15
        )
        
        # Colors: Walmart Blue #0071CE (or similar generic blue)
        bar_color = '#00BFFF' # Deep Sky Blue, similar to screenshot
        
        # 1. Year Bar Chart
        fig.add_trace(
            go.Bar(
                x=sales_by_year['YEAR'],
                y=sales_by_year['WEEKLY_SALES'],
                name="Sales by Year",
                marker_color=bar_color,
                text=sales_by_year['WEEKLY_SALES'].apply(lambda x: f'{x/1e9:.2f}bn' if x >= 1e9 else f'{x/1e6:.2f}M'),
                textposition='outside',
                textfont=dict(size=12)
            ),
            row=1, col=1
        )
        
        # 2. Month Bar Chart
        fig.add_trace(
            go.Bar(
                x=sales_by_month['MONTH_NAME'],
                y=sales_by_month['WEEKLY_SALES'],
                name="Sales by Month",
                marker_color=bar_color,
                text=sales_by_month['WEEKLY_SALES'].apply(lambda x: f'{x/1e9:.2f}bn' if x >= 1e9 else f'{x/1e6:.2f}M'),
                textposition='outside',
                textfont=dict(size=12)
            ),
            row=1, col=2
        )
        
        # 3. Day Bar Chart
        fig.add_trace(
            go.Bar(
                x=sales_by_day['DAY'],
                y=sales_by_day['WEEKLY_SALES'],
                name="Sales by Day",
                marker_color=bar_color,
                text=sales_by_day['WEEKLY_SALES'].apply(lambda x: f'{x/1e6:.0f}M'),
                textposition='outside',
                textfont=dict(size=10)
            ),
            row=2, col=1
        )
        
        # Layout Updates
        fig.update_layout(
            title_text="weekly sales by year, month and date",
            title_x=0.5,
            title_font=dict(size=24),
            template="plotly_white",
            height=800,
            showlegend=False,
            # Uniform text for consistent label sizing
            uniformtext=dict(minsize=10, mode='hide')
        )
        
        # Update Axes
        fig.update_xaxes(title_text="", row=1, col=1, type='category') # Force Year to be categorical
        fig.update_yaxes(showgrid=True, gridcolor='lightgrey')
        
        fig.show()
        print("Dashboard generated successfully.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
