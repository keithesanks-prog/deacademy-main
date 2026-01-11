import pandas as pd
import sqlalchemy

# Connect to walmart_db
db_connection_str = "mysql+pymysql://python_user:password@127.0.0.1:3306/walmart_db"
engine = sqlalchemy.create_engine(db_connection_str)

print("✅ Connected to walmart_db!")
print("=" * 70)

# Simple test query
query = """
SELECT 
    p.category,
    COUNT(f.transaction_id) as total_sales,
    ROUND(SUM(f.total_amount), 2) as revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
"""

print("\n📊 REVENUE BY CATEGORY:")
print("=" * 70)
df = pd.read_sql(query, engine)
print(df.to_string(index=False))
print("\n" + "=" * 70)
print("🎉 SUCCESS! Your Walmart database is ready for SQL practice!")
print("=" * 70)
print("\nTry modifying the query in this file or use walmart_sql_practice.py")
print("for more examples!")
