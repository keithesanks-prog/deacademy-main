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
    print("Fetching markdown sales data by year and store...")
    
    # Fetch sales data
    sales_query = "SELECT * FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
    df = pd.read_sql(sales_query, conn)
    df.columns = [c.upper() for c in df.columns]
    
    # Data Preparation
    # Find the date column
    date_col = None
    possible_date_cols = ['DATE', 'WEEK_DATE', 'SALES_DATE', 'WEEK', 'TRANSACTION_DATE']
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break
    
    if date_col is None:
        print("WARNING: No date column found. Generating sample years for demonstration.")
        import numpy as np
        years = [2010, 2011, 2012]
        df['DATE'] = pd.to_datetime(np.random.choice(years, size=len(df)), format='%Y')
        date_col = 'DATE'
    else:
        df['DATE'] = pd.to_datetime(df[date_col])
    
    # Extract Year
    df['YEAR'] = df['DATE'].dt.year
    
    # Generate markdown columns (MarkDown1 through MarkDown5)
    # In a real scenario, these would come from your data
    # For demonstration, we'll create them based on WEEKLY_SALES
    import numpy as np
    np.random.seed(42)
    
    # Check if markdown columns exist
    markdown_cols = [f'MARKDOWN{i}' for i in range(1, 6)]
    has_markdown = any(col in df.columns for col in markdown_cols)
    
    if not has_markdown:
        print("WARNING: No markdown columns found. Generating sample markdown data.")
        # Generate random markdown values with different ranges for each column
        # This ensures the bars will have different heights
        df['MARKDOWN1'] = df['WEEKLY_SALES'] * np.random.uniform(0.01, 0.03, size=len(df))
        df['MARKDOWN2'] = df['WEEKLY_SALES'] * np.random.uniform(0.015, 0.035, size=len(df))
        df['MARKDOWN3'] = df['WEEKLY_SALES'] * np.random.uniform(0.02, 0.04, size=len(df))
        df['MARKDOWN4'] = df['WEEKLY_SALES'] * np.random.uniform(0.025, 0.045, size=len(df))
        df['MARKDOWN5'] = df['WEEKLY_SALES'] * np.random.uniform(0.03, 0.05, size=len(df))
    
    # Get unique years and stores
    years = sorted(df['YEAR'].unique())
    stores = sorted(df['STORE_ID'].unique())
    
    # Aggregate by year for the bar chart (used across all year selections)
    year_agg_dict = {f'MARKDOWN{i}': 'sum' for i in range(1, 6)}
    markdown_by_year = df.groupby('YEAR').agg(year_agg_dict).reset_index()
    markdown_by_year.sort_values('YEAR', inplace=True)
    
    # Colors for each markdown column
    colors = ['#4285F4', '#34A853', '#EA4335', '#FBBC04', '#9C27B0']
    
    # Create the base figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.45, 0.55],
        row_heights=[0.7, 0.3],
        specs=[
            [{'type': 'table'}, {'type': 'xy', 'rowspan': 2}],
            [{'type': 'table'}, None]
        ],
        subplot_titles=(
            "markdown sales by year and store",
            "MarkDown1, MarkDown2, MarkDown3, MarkDown4 and MarkDown5 by Year",
            "select year for markdown sales"
        )
    )
    
    # Prepare data for each year option (including "All")
    year_options = ['All'] + years
    table_data_by_year = {}
    bar_data_by_year = {}
    
    for year_option in year_options:
        # Filter data by year
        if year_option == 'All':
            filtered_df = df.copy()
        else:
            filtered_df = df[df['YEAR'] == year_option].copy()
        
        # Aggregate markdown sales by store for the table
        agg_dict = {f'MARKDOWN{i}': 'sum' for i in range(1, 6)}
        markdown_by_store = filtered_df.groupby('STORE_ID').agg(agg_dict).reset_index()
        markdown_by_store.sort_values('STORE_ID', inplace=True)
        
        # Calculate totals
        totals = {f'MARKDOWN{i}': markdown_by_store[f'MARKDOWN{i}'].sum() for i in range(1, 6)}
        
        # Build cell values for table
        cell_values = [markdown_by_store['STORE_ID'].tolist() + ['Total']]
        
        for i in range(1, 6):
            col_name = f'MARKDOWN{i}'
            formatted_values = [f"{val:,.2f}" for val in markdown_by_store[col_name]]
            formatted_values.append(f"{totals[col_name]:,.2f}")
            cell_values.append(formatted_values)
        
        # Create row colors
        num_rows = len(markdown_by_store) + 1
        row_colors = ['white'] * (num_rows - 1) + ['grey']
        
        table_data_by_year[str(year_option)] = {
            'cell_values': cell_values,
            'row_colors': row_colors
        }
        
        # Prepare bar chart data for this year
        if year_option == 'All':
            # For "All", show data by year
            year_agg = df.groupby('YEAR').agg(agg_dict).reset_index()
            year_agg.sort_values('YEAR', inplace=True)
            bar_data_by_year[str(year_option)] = {
                'x_values': year_agg['YEAR'].tolist(),
                'y_values': {f'MARKDOWN{i}': year_agg[f'MARKDOWN{i}'].tolist() for i in range(1, 6)},
                'x_label': 'Year'
            }
        else:
            # For specific year, show the 5 markdown columns as bars
            markdown_names = [f'MarkDown{i}' for i in range(1, 6)]
            markdown_values = [totals[f'MARKDOWN{i}'] for i in range(1, 6)]
            bar_data_by_year[str(year_option)] = {
                'x_values': markdown_names,
                'y_values': {f'MARKDOWN{i}': [markdown_values[i-1]] for i in range(1, 6)},
                'x_label': 'Markdown Type'
            }
    
    # Add the initial table (All years)
    header_values = ['Store - Copy'] + [f'MarkDown{i}' for i in range(1, 6)]
    initial_data = table_data_by_year['All']
    
    fig.add_trace(
        go.Table(
            name='table_trace',
            header=dict(
                values=header_values,
                fill_color='lightgrey',
                align='left',
                font=dict(color='black', size=11)
            ),
            cells=dict(
                values=initial_data['cell_values'],
                fill_color=[initial_data['row_colors']] * len(header_values),
                align='left',
                font=dict(color='black', size=10),
                height=25
            )
        ),
        row=1, col=1
    )
    
    # Year Selector Table (Bottom Left)
    year_selector_options = ['Select All'] + [str(year) for year in years]
    fig.add_trace(
        go.Table(
            header=dict(
                values=['Year'],
                fill_color='white',
                align='center',
                font=dict(color='black', size=12)
            ),
            cells=dict(
                values=[year_selector_options],
                fill_color='lightgrey',
                align='center',
                font=dict(color='black', size=11),
                height=30
            )
        ),
        row=2, col=1
    )
    
    # Bar Chart (Right - Full Height) - Initial state shows all years
    initial_bar_data = bar_data_by_year['All']
    for i in range(1, 6):
        col_name = f'MARKDOWN{i}'
        fig.add_trace(
            go.Bar(
                x=initial_bar_data['x_values'],
                y=initial_bar_data['y_values'][col_name],
                name=f'MarkDown{i}',
                marker_color=colors[i-1],
                text=[f'{x/1e9:.2f}bn' if x >= 1e9 else f'{x/1e6:.2f}m' for x in initial_bar_data['y_values'][col_name]],
                textposition='outside',
                textfont=dict(size=9)
            ),
            row=1, col=2
        )
    
    # Create dropdown buttons for year selection
    buttons = []
    for year_option in year_options:
        year_str = str(year_option)
        year_label = "All Years" if year_option == 'All' else year_str
        table_data = table_data_by_year[year_str]
        bar_data = bar_data_by_year[year_str]
        
        # Prepare update args for all bar traces
        bar_updates = {}
        for i in range(1, 6):
            trace_idx = i + 1  # +1 because table is trace 0, year selector is trace 1
            col_name = f'MARKDOWN{i}'
            bar_updates[f'x[{trace_idx}]'] = bar_data['x_values']
            bar_updates[f'y[{trace_idx}]'] = bar_data['y_values'][col_name]
            bar_updates[f'text[{trace_idx}]'] = [f'{x/1e9:.2f}bn' if x >= 1e9 else f'{x/1e6:.2f}m' for x in bar_data['y_values'][col_name]]
        
        button = dict(
            label=year_label,
            method='update',
            args=[
                {
                    'cells.values': [table_data['cell_values']],
                    'cells.fill_color': [[table_data['row_colors']] * len(header_values)],
                    'x': [None, None] + [bar_data['x_values']] * 5,  # None for table traces, then x values for each bar
                    'y': [None, None] + [bar_data['y_values'][f'MARKDOWN{i}'] for i in range(1, 6)],
                    'text': [None, None] + [[f'{x/1e9:.2f}bn' if x >= 1e9 else f'{x/1e6:.2f}m' for x in bar_data['y_values'][f'MARKDOWN{i}']] for i in range(1, 6)]
                },
                {
                    'title': f"Markdown Sales by Year and Store - {year_label}",
                    'xaxis2.title.text': bar_data['x_label']
                }
            ]
        )
        buttons.append(button)
    
    # Update layout with dropdown menu
    fig.update_layout(
        title_text="Markdown Sales by Year and Store - All Years",
        title_x=0.5,
        title_font=dict(size=18),
        template="plotly_white",
        height=700,
        showlegend=True,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.08,
            xanchor="right",
            x=1
        ),
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.15,
                xanchor="left",
                y=1.15,
                yanchor="top",
                bgcolor="lightgrey",
                bordercolor="grey",
                font=dict(size=11)
            )
        ]
    )
    
    # Update axes
    fig.update_xaxes(title_text="Year", row=1, col=2)
    fig.update_yaxes(title_text="Markdown Sales ($)", row=1, col=2)
    
    fig.show()
    
    print(f"\nDashboard generated successfully!")
    print(f"Total records analyzed: {len(df):,}")
    print(f"Years available: {', '.join(map(str, years))}")
    print(f"Number of stores: {len(stores)}")
    print("\nUse the dropdown menu at the top to select different years!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
