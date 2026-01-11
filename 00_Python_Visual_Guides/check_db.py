import sqlalchemy

# Check if database and tables exist
try:
    engine = sqlalchemy.create_engine("mysql+pymysql://python_user:password@127.0.0.1:3306/walmart_db")
    
    with engine.connect() as conn:
        # Check what tables exist
        result = conn.execute(sqlalchemy.text("SHOW TABLES;"))
        tables = [row[0] for row in result]
        
        if tables:
            print(f"✅ Database 'walmart_db' exists with {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️  Database 'walmart_db' exists but has NO tables")
            print("   You need to run the notebook to create the tables!")
            
except sqlalchemy.exc.OperationalError as e:
    if "Unknown database" in str(e):
        print("❌ Database 'walmart_db' does not exist")
        print("   You need to run the notebook to create it!")
    else:
        print(f"❌ Connection error: {e}")
