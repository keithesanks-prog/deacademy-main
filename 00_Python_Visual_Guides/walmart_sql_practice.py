import pandas as pd
import sqlalchemy

# Connect to walmart_db
db_connection_str = "mysql+pymysql://python_user:password@127.0.0.1:3306/walmart_db"
engine = sqlalchemy.create_engine(db_connection_str)

print("✅ Connected to walmart_db!\n")
print("=" * 60)

# Example queries - modify these to practice!

# Query 1: Total Revenue by Product Category
query1 = """
SELECT 
    p.category,
    COUNT(f.transaction_id) as total_sales,
    CONCAT('$', FORMAT(SUM(f.total_amount), 2)) as revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY SUM(f.total_amount) DESC;
"""

print("QUERY 1: Total Revenue by Product Category")
print("=" * 60)
df1 = pd.read_sql(query1, engine)
print(df1)
print("\n")

# Query 2: Sales Performance by Region
query2 = """
SELECT 
    s.region,
    s.city,
    COUNT(f.transaction_id) as num_transactions,
    SUM(f.total_amount) as revenue
FROM fact_sales f
JOIN dim_stores s ON f.store_id = s.store_id
GROUP BY s.region, s.city
ORDER BY revenue DESC;
"""

print("QUERY 2: Sales Performance by Region")
print("=" * 60)
df2 = pd.read_sql(query2, engine)
print(df2)
print("\n")

# Query 3: Top 10 Customers by Total Spend
query3 = """
SELECT 
    c.customer_name,
    c.segment,
    COUNT(f.transaction_id) as num_purchases,
    SUM(f.total_amount) as total_spent
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_spent DESC
LIMIT 10;
"""

print("QUERY 3: Top 10 Customers by Total Spend")
print("=" * 60)
df3 = pd.read_sql(query3, engine)
print(df3)
print("\n")

# Query 4: Sales by Quarter
query4 = """
SELECT 
    d.quarter,
    COUNT(f.transaction_id) as num_sales,
    SUM(f.total_amount) as revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.quarter
ORDER BY d.quarter;
"""

print("QUERY 4: Sales by Quarter")
print("=" * 60)
df4 = pd.read_sql(query4, engine)
print(df4)
print("\n")

# Query 5: Day of Week Analysis
query5 = """
SELECT 
    d.day_name,
    COUNT(f.transaction_id) as num_sales,
    AVG(f.total_amount) as avg_transaction_value
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.day_name
ORDER BY num_sales DESC;
"""

print("QUERY 5: Sales by Day of Week")
print("=" * 60)
df5 = pd.read_sql(query5, engine)
print(df5)
print("\n")

print("=" * 60)
print("✨ Practice by modifying the queries above!")
print("=" * 60)

# YOUR CUSTOM QUERY HERE:
# Uncomment and write your own query to practice
"""
my_query = '''
SELECT 
    -- Write your query here
FROM fact_sales f
-- Add your joins and conditions
'''
df_custom = pd.read_sql(my_query, engine)
print(df_custom)
"""
