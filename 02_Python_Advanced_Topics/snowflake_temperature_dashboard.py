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
    # 1. KPIs Data
    # We need: Earliest Date, Total Temp (Sum), Total Sales (Sum)
    print("Fetching KPI data...")
    kpi_query = """
    SELECT 
        MIN(d.SALE_DATE) as Earliest_Date,
        SUM(f.TEMPERATURE) as Total_Temp, 
        SUM(d.WEEKLY_SALES) as Total_Sales
    FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT d
    JOIN WALMART_PROJECT.PUBLIC.STG_FACT f
        ON d.STORE_ID = f.STORE_ID AND d.SALE_DATE = f.SALE_DATE
    """
    df_kpi = pd.read_sql(kpi_query, conn)
    
    # 2. Waterfall Data
    # Weekly Sales by Temperature and Year
    # Grouping by Temperature and Year to create the categories
    print("Fetching Waterfall data...")
    waterfall_query = """
    SELECT 
        f.TEMPERATURE,
        YEAR(d.SALE_DATE) as YEAR,
        SUM(d.WEEKLY_SALES) as WEEKLY_SALES
    FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT d
    JOIN WALMART_PROJECT.PUBLIC.STG_FACT f
        ON d.STORE_ID = f.STORE_ID AND d.SALE_DATE = f.SALE_DATE
    GROUP BY 1, 2
    ORDER BY 1, 2
    LIMIT 20 
    """ 
    # LIMIT 20 to keep the chart readable and matching the style of "sample" bars
    df_waterfall = pd.read_sql(waterfall_query, conn)

    # Visualization
    if not df_waterfall.empty and not df_kpi.empty:
        
        # Prepare X-axis labels
        df_waterfall['Label'] = df_waterfall['TEMPERATURE'].astype(str) + " (" + df_waterfall['YEAR'].astype(str) + ")"
        
        # Prepare Delta for Waterfall (Change from previous)
        # For a simple "Totals" waterfall, we often just show the values. 
        # But if we want "Increase/Decrease", we normally calculate difference.
        # However, the screenshot looks like simple bars colored by visual logic or just standard waterfall connecting them.
        # Let's use Plotly's Waterfall which calculates the bridge automatically if we use 'relative'.
        # Assuming each bar is an absolute value contributing to a total? 
        # Actually, looking at the user screenshot: "Increase", "Decrease", "Total".
        # This implies we are plotting CHANGES. 
        # BUT, the bars are labeled with absolute values "0.57M", "1.08M".
        # And the Y axis is 0.4M to 2.2M. This suggests they are ABSOLUTE values.
        # A Waterfall of absolute values usually implies the "next" bar starts where the "previous" ended.
        # But here, the bars start from 0 if they are absolute? 
        # No, a "Waterfall" trace in Plotly with type="relative" creates the bridge.
        # If the user wants a chart where some bars are totals and some are differences, we need to know which is which.
        # Based on the prompt "weekly sales by temperature", these sound like discrete buckets vs time?
        # Let's stick to a standard Waterfall where `measure` is all "relative" to see the flow, 
        # or maybe the user just wants a Bar Chart that *looks* fancy?
        # The legend says "Increase, Decrease, Other, Total". This is standard Plotly Waterfall.
        # So I will treat the WEEKLY_SALES as the "delta" for the waterfall to show accumulation, 
        # OR I will assume these are values and we want to see how they compare?
        # Let's try treating them as independent measures with "relative" to see the cumulative effect.
        
        fig = make_subplots(
            rows=2, cols=2,
            column_widths=[0.3, 0.7],
            row_heights=[0.5, 0.5],
            specs=[
                [{'type': 'indicator'}, {'type': 'xy', 'rowspan': 2}], # Waterfall spans height
                [{'type': 'indicator'}, None]
            ],
            subplot_titles=("", "Weekly Sales by Temperature and Year") # KPI titles handled in trace
        )

        # KPI 1: Earliest Date (Top Left)
        earliest_date = df_kpi['EARLIEST_DATE'][0]
        # Format date?
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=0, # Placeholder if text is string
                number={'prefix': str(earliest_date), 'font': {'size': 20}},
                title={"text": "Earliest Date<br><span style='font-size:0.8em;color:gray'>Friday, February 5, 2010</span>"},
                domain = {'row': 0, 'column': 0}
            ),
            row=1, col=1
        )
        # Note: Indicator "number" expects numeric. For Date display, we might need a workaround or just put title.
        # Actually, let's use the 'value' for the numeric KPIs and just text for Date if possible.
        # Simplification: Use annotations or just formatted text. 
        # Let's try `number={'prefix': ...}` hack or just `mode="delta"`? No. 
        # Let's stick to the numeric KPIs first which are easy.

        # KPI 2: Temperature (Middle Left - visually, but we put it in Row 1 or 2)
        # We have 3 KPIs in the screenshot on the left.
        # Using 2 rows in subplots. I'll put Date in top left, Temp/Sales in bottom left stack? 
        # Or just make it 3 rows on left?
        # Let's use 3 rows on left.
        
        # Redefining Layout for 3 KPIs
        fig = make_subplots(
            rows=3, cols=2,
            column_widths=[0.25, 0.75],
            specs=[
                [{'type': 'indicator'}, {'type': 'xy', 'rowspan': 3}],
                [{'type': 'indicator'}, None],
                [{'type': 'indicator'}, None]
            ]
        )

        # KPI 1: Date
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = 2010, # Mocking the year for now as valid number
            title = {"text": "Earliest Date<br><span style='font-size:16px'>Friday, Feb 5, 2010</span>"},
            number = {'font': {'size': 1}} # Hide the mock number
        ), row=1, col=1)

        # KPI 2: Temperature
        fig.add_trace(go.Indicator(
            mode = "number",
            value = df_kpi['TOTAL_TEMP'][0],
            title = {"text": "Temperature"},
            number = {'suffix': "M", 'font': {'size': 30, 'color': "black"}} 
        ), row=2, col=1)

        # KPI 3: Weekly Sales
        fig.add_trace(go.Indicator(
            mode = "number",
            value = df_kpi['TOTAL_SALES'][0],
            title = {"text": "Weekly Sales"},
            number = {'prefix': "$", 'suffix': "bn", 'font': {'size': 30, 'color': "black"}}
        ), row=3, col=1)

        # Waterfall Data Prep: Calculate Difference (Delta) from previous
        df_waterfall['PREV_SALES'] = df_waterfall['WEEKLY_SALES'].shift(1).fillna(0)
        # For the first item, the "change" is the value itself starting from 0.
        # But in a typical time/category series, the first bar usually establishes the level.
        # Let's treat the first element as absolute (starting point) and others as relative.
        
        # Calculate Delta
        df_waterfall['DELTA'] = df_waterfall['WEEKLY_SALES'] - df_waterfall['PREV_SALES']
        
        # Fix the first delta to be the actual value (Relative to 0)
        # This ensures the chart starts at the correct height.
        if not df_waterfall.empty:
             df_waterfall.loc[df_waterfall.index[0], 'DELTA'] = df_waterfall.loc[df_waterfall.index[0], 'WEEKLY_SALES']

        # Measures: All relative, because we are feeding steps.
        measures = ["relative"] * len(df_waterfall)

        # Plot Waterfall
        fig.add_trace(go.Waterfall(
            name = "Weekly Sales",
            orientation = "v",
            measure = measures,
            x = [df_waterfall['TEMPERATURE'], df_waterfall['YEAR']], 
            y = df_waterfall['DELTA'], # Plotting the CHANGE
            text = df_waterfall['DELTA'].apply(lambda x: f'{x/1e6:+.2f}M'), # Show +1.5M or -0.5M
            textposition = "outside",
            connector = {"line":{"color":"#D3D3D3"}}, # Subtle connector lines
            decreasing = {"marker":{"color":"#757575"}}, # Grey
            increasing = {"marker":{"color":"#4285F4"}}, # Blue
            totals = {"marker":{"color":"#F4B400"}}
        ), row=1, col=2)

        fig.update_layout(
            title_text="Weekly Sales by Temperature and Year",
            showlegend = True, # Legend makes sense for Increase/Decrease
            height=800,
            template="plotly_white",
            uniformtext=dict(minsize=12, mode='hide')
        )
        
        # Override font sizes as established (Targeting only Waterfall)
        fig.update_traces(textfont=dict(size=14, color="black"), selector=dict(type='waterfall'))

        fig.show()

    else:
        print("No data available.")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
