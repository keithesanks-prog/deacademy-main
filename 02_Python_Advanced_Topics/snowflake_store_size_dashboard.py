import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

try:
    print("Fetching Store Size data...")
    
    # 1. Fetch Store Dimension (Small table)
    # Using simple SELECT * to avoid column name issues
    df_store = pd.read_sql("SELECT * FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM", conn)
    # Ensure column names are upper case for consistency
    df_store.columns = [c.upper() for c in df_store.columns]
    
    # 2. Fetch Raw Sales Data (Un-aggregated)
    # We will aggregate this in Python to demonstrate Pandas capabilities
    sales_query = """
    SELECT 
        STORE_ID,
        WEEKLY_SALES
    FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT
    """
    df_raw_sales = pd.read_sql(sales_query, conn)
    df_raw_sales.columns = [c.upper() for c in df_raw_sales.columns]
    
    # DEBUG: Check Raw Data
    print(f"Raw Sales Data: {len(df_raw_sales)} rows")
    
    # --- LEARNING MOMENT: Pandas Aggregation ---
    # Instead of doing "GROUP BY" in SQL, we do it here.
    # Logic: "Group by STORE_ID, and for WEEKLY_SALES, calculate the SUM"
    print("Aggregating sales data using Pandas...")
    
    df_sales = df_raw_sales.groupby(['STORE_ID']).agg({
        'WEEKLY_SALES': 'sum'
    }).reset_index()
    
    # Rename column to match our previous logic (Expected: TOTAL_SALES)
    df_sales.rename(columns={'WEEKLY_SALES': 'TOTAL_SALES'}, inplace=True)
    
    # DEBUG: Check Aggregated Data
    print(f"Aggregated Sales Data: {len(df_sales)} rows")
    print(f"Sales Store IDs: {sorted(df_sales['STORE_ID'].unique())[:10]}...")
    
    import numpy as np

    # 3. Merge in Pandas
    # Verify we have sales data
    if df_sales.empty:
        print("Error: No Sales Data found in STG_DEPARTMENT.")
    else:
        # Fallback for Empty Store Table
        if df_store.empty:
            print("WARNING: WALMART_STORE_DIM is empty. Generating DUMMY Store Size data for visualization.")
            # Get unique stores from sales
            unique_stores = df_sales['STORE_ID'].unique()
            # Generate random sizes between 100k and 250k
            sizes = np.random.randint(100000, 250000, size=len(unique_stores))
            
            df_store = pd.DataFrame({
                'STORE_ID': unique_stores,
                'STORE_SIZE': sizes
            })
            print(f"Generated {len(df_store)} dummy store records.")

        # Ensure STORE_ID is same type (int)
        df_store['STORE_ID'] = pd.to_numeric(df_store['STORE_ID'], errors='coerce').fillna(0).astype(int)
        df_sales['STORE_ID'] = pd.to_numeric(df_sales['STORE_ID'], errors='coerce').fillna(0).astype(int)

        df = pd.merge(df_sales, df_store, on='STORE_ID', how='inner')
        
        # Sort by STORE_SIZE descending (largest stores first, for smooth area chart)
        df.sort_values(by='STORE_SIZE', ascending=False, inplace=True)
        
        # Calculate Total for Footer
        grand_total = df['TOTAL_SALES'].sum()
        
        # Prepare Table Data
        
        # --- LEARNING MOMENT: Regular Functions vs Lambda ---
        # A lambda is just a shortcut. You can always write a normal function instead!
        def format_millions(value):
            return f"{value:,.2f}"

        # Apply the normal function
        df['Formatted_Sales'] = df['TOTAL_SALES'].apply(format_millions)
        
        # Calculate max for annotation or highlighting?
        # User screenshot shows Area chart "WeeklySales by Size"
        # X axis seems to be Size (numeric)
        # Y axis is Sales.
        
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.7, 0.3],
            specs=[[{'type': 'xy'}, {'type': 'table'}]],
            subplot_titles=("Weekly Sales by Size", "")
        )

        # 1. Area Chart (Left)
        # Area chart with STORE_SIZE on X-axis and SALES on Y-axis
        # Sorted descending by size (largest to smallest)
        fig.add_trace(go.Scatter(
            x=df['STORE_SIZE'],  # STORE_SIZE on horizontal axis
            y=df['TOTAL_SALES'],  # SALES on vertical axis
            fill='tozeroy',  # Fill to bottom (y-axis)
            mode='lines+markers+text',
            name='Sales',
            line=dict(color='#4285F4', width=2),
            marker=dict(size=6),
            text=df['TOTAL_SALES'].apply(lambda x: f'{x/1e6:.0f}M'),
            textposition="top center",
            textfont=dict(size=10, color='black'),
            hovertemplate='<b>Store %{customdata}</b><br>' +
                         'Size: %{x:,.0f} sq ft<br>' +
                         'Sales: $%{y:,.0f}<br>' +
                         '<extra></extra>',
            customdata=df['STORE_ID']
        ), row=1, col=1)

        # 2. Data Table (Right)
        # Columns: Store, Size, Weekly_Sales
        # Add a Total Row at the bottom?
        # Screenshot has "Total 6,055,109..."
        
        # Construct header and cells
        header_values = ["Store", "Size", "Weekly_Sales"]
        
        # Create a separate dataframe for the table, sorted by sales descending
        df_table = df.sort_values(by='TOTAL_SALES', ascending=False)
        
        # Add Total row to dataframe for display
        # We can append it or handle in trace
        cell_values = [
            df_table['STORE_ID'].tolist() + ['Total'],
            df_table['STORE_SIZE'].tolist() + [''],
            df_table['Formatted_Sales'].tolist() + [f"{grand_total:,.2f}"]
        ]
        
        # Stylistic coloring for table based on screenshot (Blue headers, alternating rows?)
        # Screenshot has vivid blue header and some highlighted rows.
        # We'll stick to basic formatting for now.
        
        fig.add_trace(go.Table(
            header=dict(
                values=header_values,
                fill_color='grey',
                align='left',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=cell_values,
                fill_color=[['white']*len(df) + ['lightgrey']], # Grey background for Total row
                align='left',
                font=dict(color='black', size=11)
            )
        ), row=1, col=2)

        fig.update_layout(
            title_text="Weekly Sales by Store Size",
            template="plotly_white",
            height=600,
            showlegend=False
        )

        fig.show()
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
