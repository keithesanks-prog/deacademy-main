import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv
import numpy as np

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
    print("Fetching sales and store data...")
    
    # Fetch all sales data
    sales_query = "SELECT STORE_ID, WEEKLY_SALES FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT"
    df_sales = pd.read_sql(sales_query, conn)
    df_sales.columns = [c.upper() for c in df_sales.columns]
    
    # Fetch store dimension - query all columns to be safe
    store_query = "SELECT * FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM"
    try:
        df_store = pd.read_sql(store_query, conn)
        df_store.columns = [c.upper() for c in df_store.columns]
    except Exception as e:
        print(f"Warning: Could not fetch store dimension: {e}")
        df_store = pd.DataFrame(columns=['STORE_ID'])

    # Handle missing/empty store table or missing TYPE column
    if df_store.empty or 'TYPE' not in df_store.columns:
        print("WARNING: WALMART_STORE_DIM is empty or missing TYPE. Generating dummy types.")
        unique_stores = df_sales['STORE_ID'].unique()
        # Reproducible random types
        np.random.seed(42)
        store_types = {store: np.random.choice(['A', 'B', 'C']) for store in unique_stores}
        # Create a dataframe for types to merge
        df_store_types = pd.DataFrame(list(store_types.items()), columns=['STORE_ID', 'TYPE'])
        
        # Merge types back to sales
        # Ensure STORE_ID types match (convert to int/str consistency)
        # Using map is safer
        df_sales['TYPE'] = df_sales['STORE_ID'].map(store_types).fillna('Unknown')
    else:
        # Merge if TYPE exists
        # Select only relevant columns to merge
        df_store_subset = df_store[['STORE_ID', 'TYPE']].copy()
        
        # Ensure proper types for merge keys
        # Convert to string just in case
        df_sales['STORE_ID'] = df_sales['STORE_ID'].astype(str)
        df_store_subset['STORE_ID'] = df_store_subset['STORE_ID'].astype(str)
        
        df_sales = pd.merge(df_sales, df_store_subset, on='STORE_ID', how='left')
        df_sales['TYPE'] = df_sales['TYPE'].fillna('Unknown')
    
    # Aggregate data
    # 1. Total by Type (for Pie Chart)
    sales_by_type = df_sales.groupby('TYPE')['WEEKLY_SALES'].sum().reset_index()
    
    # 2. Total by Store and Type (for Bar Chart)
    sales_by_store = df_sales.groupby(['STORE_ID', 'TYPE'])['WEEKLY_SALES'].sum().reset_index()
    sales_by_store.sort_values(by=['TYPE', 'WEEKLY_SALES'], ascending=[True, True], inplace=True)
    
    # Prepare Arrays for Plotly
    types = sorted(sales_by_type['TYPE'].unique())
    # Ensure color consistency
    type_colors = {'A': '#4285F4', 'B': '#34A853', 'C': '#EA4335', 'Unknown': '#FBBC04'}
    
    # Create Subplots
    # Layout: 
    # Row 1, Col 1: Placeholder/Text for "Select Store Type" (Visual only, actual buttons are layout menu)
    # Row 2, Col 1: Pie Chart
    # Row 1-2, Col 2: Horizontal Bar Chart
    
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.4, 0.6],
        row_heights=[0.2, 0.8],
        specs=[
            [{'type': 'domain'}, {'type': 'xy', 'rowspan': 2}], # Top Left used for spacing/text, Right is bar
            [{'type': 'domain'}, None]                          # Bottom Left is Pie
        ],
        horizontal_spacing=0.05,
        vertical_spacing=0.05,
        subplot_titles=("", "Weekly_Sales by Type and Store - Copy", "Weekly_Sales by store Type")
    )

    # --- Pie Chart (Bottom Left) ---
    # We want this to update based on selection too, essentially highlighting or slicing?
    # The requirement screenshot shows "Weekly_Sales by store Type" Pie chart with A, B, C slices.
    # Usually this remains constant or filters locally. 
    # If I select "A", showing a Pie chart of just "A" is a full circle. 
    # Let's assume the Pie chart always shows the distribution of the *visible* data or just the static distribution.
    # Given "Select Store Type" is a filter, usually it filters the detailed view (Bar chart). 
    # Let's make the Pie Chart show the total distribution always, or we can make it filter. 
    # Let's stick to consistent filtering: If "A" is selected, we see totals for A.
    
    # Actually, simpler: The Pie chart shows the composition. The Filter typically applies to the detailed view.
    # However, to match standard dashboard interactivity, let's allow the buttons to filter *visibility* of traces.
    
    # Add Pie Chart Trace (Trace 0)
    fig.add_trace(
        go.Pie(
            labels=sales_by_type['TYPE'],
            values=sales_by_type['WEEKLY_SALES'],
            marker_colors=[type_colors.get(t, 'grey') for t in sales_by_type['TYPE']],
            textinfo='label',
            showlegend=False,
            hole=0.0
        ),
        row=2, col=1
    )

    # --- Horizontal Bar Chart (Right) ---
    # We need a bar for each store.
    # Grouping by Type on Y-axis visually means sorting by Type.
    # We can color bars by TYPE or by STORE?
    # Screenshot says "Store - Copy" in legend, with many colors. 
    # It depicts grouped bars (Categorical Y axis with Type A, B, C).
    # Since Plotly doesn't support multi-level categorical axes easily in basic Bar, 
    # we can fake it or use `y` as `[Type, StoreID]`. Plotly handles multicategory axes!
    
    sales_by_store['STORE_STR'] = sales_by_store['STORE_ID'].astype(str)
    
    # Create specific traces for each Type to allow filtering via updatemenus buttons
    # Wait, if we use one trace with multicategory, filtering is harder.
    # If we use separate traces for Type A, Type B, Type C, we can toggle them easily.
    
    for t in types:
        df_subset = sales_by_store[sales_by_store['TYPE'] == t]
        
        # We want distinct colors for stores? Or just one color for the Type?
        # Screenshot legend shows "Store - Copy" and many specific colors points. 
        # But the bars themselves in the screenshot look mostly consistent or grouped.
        # Actually, looking closely at the screenshot for "Weekly_Sales by Type and Store - Copy":
        # The bars are thin lines. The colors seem random or specific to store.
        # The Y-axis has Big Labels "A", "B", "C". 
        
        # Let's use separate traces for each Type to enable the "Select A, B, C" buttons easily.
        # This works well.
        
        fig.add_trace(
            go.Bar(
                x=df_subset['WEEKLY_SALES'],
                y=[df_subset['TYPE'], df_subset['STORE_STR']], # Multicategory Y
                orientation='h',
                name=f"Type {t}",
                hovertext=df_subset['STORE_STR'],
                text=df_subset['WEEKLY_SALES'].apply(lambda x: f'{x/1e6:.0f}M'),
                textposition='outside',
                marker=dict(color=type_colors.get(t, 'grey')) # Use standard type color for now, user can request rainbow later if needed
            ),
            row=1, col=2
        )

    # Updatemenus for "Select Store Type"
    # Buttons: Select All, A, B, C
    
    # Visibility logic:
    # Trace 0 is Pie (Always visible? Or filters?) -> Let's keep Pie always visible for context.
    # Traces 1..N are the Bar charts for each Type.
    
    # Indices:
    # 0: Pie
    # 1: Bar Type A (assuming sort order)
    # 2: Bar Type B
    # 3: Bar Type C
    
    # If Select All: All Bar traces visible.
    # If Select A: Only Bar trace for A visible.
    
    # Note: Logic depends on exact number of types found.
    # We construct the buttons dynamically.
    
    # Trace indices for bars start at 1.
    bar_trace_indices = list(range(1, 1 + len(types)))
    
    buttons = []
    
    # 1. Select All Button
    buttons.append(dict(
        label="Select All",
        method="update",
        args=[{"visible": [True] * (1 + len(types))}, # All traces visible
              {"title": "Weekly Sales by Store Type - All"}]
    ))
    
    # 2. Individual Type Buttons
    for i, t in enumerate(types):
        # Construct visibility list
        # Pie (idx 0) always True
        # Bars: Only idx (1+i) is True, others False
        vis = [True] # Pie
        for j in range(len(types)):
            if i == j:
                vis.append(True)
            else:
                vis.append(False)
                
        buttons.append(dict(
            label=t,
            method="update",
            args=[{"visible": vis},
                  {"title": f"Weekly Sales by Store Type - Type {t}"}]
        ))
        
    # Layout Config
    fig.update_layout(
        title_text="Weekly Sales by Store Type",
        title_x=0.5,
        title_font=dict(size=24),
        template="plotly_white",
        height=700,
        showlegend=False, # Screenshot doesn't show standard legend for Types, legend is for Stores which is implied
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.0,
                y=1.05, # Position above the Pie Chart area (Top Left)
                xanchor="left",
                yanchor="top",
                buttons=buttons,
                bgcolor="lightgrey",
                bordercolor="white",
                font=dict(size=12)
            )
        ]
    )
    
    # Add text annotation for "Select store type" label
    fig.add_annotation(
        text="Select Store Type",
        x=0.0,
        y=1.12,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14, color="black"),
        xanchor="left"
    )

    fig.show()
    print("Dashboard generated.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
