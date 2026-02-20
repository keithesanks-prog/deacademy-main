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
    print("Fetching Department Wise Weekly Sales data...")
    
    # Query: Total Sales by Department
    query = """
    SELECT 
        DEPT_ID, 
        SUM(WEEKLY_SALES) as TOTAL_SALES 
    FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT 
    GROUP BY DEPT_ID 
    ORDER BY TOTAL_SALES DESC
    """
    
    df = pd.read_sql(query, conn)
    df.columns = [c.upper() for c in df.columns]
    
    if df.empty:
        print("WARNING: No data returned from STG_DEPARTMENT.")
    else:
        # Data Prep
        total_sales_all = df['TOTAL_SALES'].sum()
        top_5_df = df.head(5)
        
        # Determine number of depts
        n_depts = len(df)

        # Create Layout
        # Row 1: Table (Left), KPI (Middle), List (Right)
        # Row 2: Bar Chart (Full Width)
        fig = make_subplots(
            rows=2, cols=3,
            column_widths=[0.4, 0.3, 0.3],
            row_heights=[0.4, 0.6],
            specs=[
                [{'type': 'table'}, {'type': 'indicator'}, {'type': 'table'}], 
                [{'type': 'xy', 'colspan': 3}, None, None]
            ],
            subplot_titles=("Department Sales Table", "", "Top 5 Department Wise Sales", "Weekly_Sales by Dept"),
            vertical_spacing=0.1
        )
        
        # 1. Table (Top Left)
        # Columns: Dept-Copy, Weekly_Sales
        # Formatting Number
        def fmt_currency(x): return f"{x:,.2f}"
        
        fig.add_trace(
            go.Table(
                header=dict(
                    values=["Dept - Copy", "Weekly_Sales"],
                    fill_color='black',
                    font=dict(color='white', size=12),
                    align='left'
                ),
                cells=dict(
                    values=[df['DEPT_ID'], df['TOTAL_SALES'].apply(fmt_currency)],
                    fill_color=[['lightgrey', 'white'] * (len(df)//2 + 1)],
                    font=dict(color='black', size=11),
                    align='right'
                )
            ),
            row=1, col=1
        )
        
        # 2. KPI (Top Middle)
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=total_sales_all,
                title={"text": "Weekly_Sales"},
                number={'valueformat': ".3s", 'suffix': "bn" if total_sales_all > 1e9 else "M", 'font': {'size': 50}}
            ),
            row=1, col=2
        )
        
        # 3. Top 5 List (Top Right)
        # Using a simplified Table to mimic the list view
        fig.add_trace(
            go.Table(
                header=dict(values=[], height=0), # Hide header
                cells=dict(
                    values=[
                        top_5_df['DEPT_ID'], 
                        top_5_df['TOTAL_SALES'].apply(lambda x: f"{x:,.2f}")
                    ],
                    align=['left', 'right'],
                    fill_color='white',
                    font=dict(size=12),
                    height=30
                )
            ),
            row=1, col=3
        )
        
        # 4. Bar Chart (Bottom)
        # Sort by Dept ID for the chart (Left=Smallest ID, Right=Largest ID)
        df_bar = df.copy()
        df_bar['DEPT_ID_NUM'] = pd.to_numeric(df_bar['DEPT_ID'])
        df_bar = df_bar.sort_values('DEPT_ID_NUM')

        fig.add_trace(
            go.Bar(
                x=df_bar['DEPT_ID'].astype(str),
                y=df_bar['TOTAL_SALES'],
                marker=dict(color=df_bar['DEPT_ID_NUM'], colorscale='Viridis'), 
                text=df_bar['TOTAL_SALES'].apply(lambda x: f'{x/1e9:.1f}bn' if x > 1e9 else f'{x/1e6:.1f}M'),
                textposition='outside'
            ),
            row=2, col=1
        )
        
        # Layout Updates
        fig.update_layout(
            title_text="department wise weekly sales",
            title_x=0.5,
            title_font=dict(size=24),
            template="plotly_white",
            height=700,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Dept - Copy", type='category', row=2, col=1)
        
        fig.show()
        print("Dashboard generated successfully.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
