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
    print("Fetching sales data by store type and month...")
    
    # First, let's get all data from STG_DEPARTMENT to see what columns are available
    sales_query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
    df_sales = pd.read_sql(sales_query, conn)
    df_sales.columns = [c.upper() for c in df_sales.columns]
    
    # Get store dimension data
    store_query = "SELECT * FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM"
    df_store = pd.read_sql(store_query, conn)
    df_store.columns = [c.upper() for c in df_store.columns]
    
    # Check if store dimension has TYPE column and data
    if df_store.empty or 'TYPE' not in df_store.columns:
        print("WARNING: WALMART_STORE_DIM is empty or missing TYPE column. Generating dummy store types.")
        # Generate random store types for each unique store
        import numpy as np
        unique_stores = df_sales['STORE_ID'].unique()
        store_types = {store: np.random.choice(['A', 'B', 'C']) for store in unique_stores}
        df_sales['STORE_TYPE'] = df_sales['STORE_ID'].map(store_types)
        df = df_sales
    else:
        # Merge the dataframes
        df = pd.merge(df_sales, df_store[['STORE_ID', 'TYPE']], on='STORE_ID', how='left')
        df.rename(columns={'TYPE': 'STORE_TYPE'}, inplace=True)
        
        # Fill any missing store types
        df['STORE_TYPE'].fillna('Unknown', inplace=True)
    
    # Data Preparation
    # Find the date column (could be DATE, WEEK_DATE, SALES_DATE, etc.)
    date_col = None
    possible_date_cols = ['DATE', 'WEEK_DATE', 'SALES_DATE', 'WEEK', 'TRANSACTION_DATE']
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break
    
    if date_col is None:
        print("WARNING: No date column found. Generating sample months for demonstration.")
        # Generate sample dates based on row count
        import numpy as np
        num_months = 12
        months = pd.date_range(start='2023-01-01', periods=num_months, freq='MS')
        df['DATE'] = np.random.choice(months, size=len(df))
        date_col = 'DATE'
    else:
        # Convert to datetime
        df['DATE'] = pd.to_datetime(df[date_col])
    
    # Extract Year and Month for grouping
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['YEAR_MONTH'] = df['DATE'].dt.to_period('M').astype(str)  # Format: 2023-01
    
    # Aggregation: Group by YEAR_MONTH and STORE_TYPE, sum WEEKLY_SALES
    sales_by_month_type = df.groupby(['YEAR_MONTH', 'STORE_TYPE'])['WEEKLY_SALES'].sum().reset_index()
    
    # Sort by YEAR_MONTH to ensure chronological order
    sales_by_month_type['SORT_KEY'] = pd.to_datetime(sales_by_month_type['YEAR_MONTH'])
    sales_by_month_type.sort_values('SORT_KEY', inplace=True)
    
    # Get unique months in order
    months_ordered = sales_by_month_type['YEAR_MONTH'].unique()
    
    # Calculate total sales by store type (for sorting)
    total_by_type = df.groupby('STORE_TYPE')['WEEKLY_SALES'].sum().reset_index()
    total_by_type.sort_values('WEEKLY_SALES', ascending=False, inplace=True)
    type_order = total_by_type['STORE_TYPE'].tolist()
    
    # Create a pivot table for the table display: Rows = Months, Columns = Store Types
    pivot_table = sales_by_month_type.pivot(index='YEAR_MONTH', columns='STORE_TYPE', values='WEEKLY_SALES')
    pivot_table = pivot_table.fillna(0)  # Fill missing values with 0
    
    # Sort columns alphabetically (A, B, C)
    pivot_table = pivot_table.sort_index(axis=1)
    
    # Extract month names from YEAR_MONTH for better display
    pivot_table.index = pd.to_datetime(pivot_table.index).strftime('%B')
    
    # Calculate column totals
    totals = pivot_table.sum()
    
    # Prepare data for the table
    store_types = pivot_table.columns.tolist()
    months = pivot_table.index.tolist()
    
    # Build header: ["Month"] + store types
    header_values = ['Month'] + store_types
    
    # Build cell values: each column is a list
    cell_values = [months]  # First column is months
    
    # Add each store type column with formatted values
    for store_type in store_types:
        formatted_values = [f"{val:,.2f}" for val in pivot_table[store_type]]
        cell_values.append(formatted_values)
    
    # Add Total row
    months_with_total = months + ['Total']
    cell_values[0] = months_with_total  # Update months column to include Total
    
    for i, store_type in enumerate(store_types, start=1):
        # Add total to each store type column
        formatted_total = f"{totals[store_type]:,.2f}"
        cell_values[i] = cell_values[i] + [formatted_total]
    
    # Create alternating row colors (highlight every other month)
    num_rows = len(months_with_total)
    row_colors = []
    for i in range(num_rows):
        if i == num_rows - 1:  # Total row
            row_colors.append('lightgrey')
        elif i % 2 == 1:  # Odd rows (0-indexed, so 1, 3, 5... are actually even months)
            row_colors.append('#B3D9FF')  # Light blue
        else:
            row_colors.append('white')
    
    # Color palette for store types
    colors = {
        'A': '#4285F4',  # Blue
        'B': '#34A853',  # Green
        'C': '#EA4335',  # Red
        'Unknown': '#FBBC04'  # Yellow
    }
    
    # Create subplots: Line chart on left, Table on right
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.65, 0.35],
        specs=[[{'type': 'xy'}, {'type': 'table'}]],
        subplot_titles=("Weekly Sales by Month and Type", "Month")
    )
    
    # 1. Line Chart (Left)
    # Show sales trends over time for each store type
    for store_type in type_order:
        subset = sales_by_month_type[sales_by_month_type['STORE_TYPE'] == store_type]
        fig.add_trace(
            go.Scatter(
                x=subset['YEAR_MONTH'],
                y=subset['WEEKLY_SALES'],
                name=f"Type {store_type}",
                mode='lines+markers+text',
                line=dict(color=colors.get(store_type, 'gray'), width=3),
                marker=dict(size=8),
                text=subset['WEEKLY_SALES'].apply(lambda x: f'{x/1e6:.0f}M'),
                textposition='top center',
                textfont=dict(size=10),
                hovertemplate='<b>Type %{fullData.name}</b><br>' +
                             'Month: %{x}<br>' +
                             'Sales: $%{y:,.0f}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )
    
    # 2. Pivot Table (Right)
    fig.add_trace(
        go.Table(
            header=dict(
                values=header_values,
                fill_color='grey',
                align='left',
                font=dict(color='white', size=12, family='Arial')
            ),
            cells=dict(
                values=cell_values,
                fill_color=[row_colors] * len(header_values),  # Apply same row colors to all columns
                align='left',
                font=dict(color='black', size=11, family='Arial'),
                height=25
            )
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Weekly Sales by Store Type and Month",
        title_x=0.5,
        title_font=dict(size=20),
        template="plotly_white",
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01
        )
    )
    
    # Update x-axis for line chart
    fig.update_xaxes(
        categoryorder='array',
        categoryarray=months_ordered,
        tickangle=-45,
        row=1, col=1
    )
    
    # Update y-axis for line chart
    fig.update_yaxes(title_text="Weekly Sales ($)", row=1, col=1)
    
    fig.show()
    
    print(f"\nDashboard generated successfully!")
    print(f"Total records analyzed: {len(df):,}")
    print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
    print(f"Store types: {', '.join(store_types)}")
    print(f"\nGrand Total: ${totals.sum():,.2f}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
