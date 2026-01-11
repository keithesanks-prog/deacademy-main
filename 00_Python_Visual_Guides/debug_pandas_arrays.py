import pandas as pd

try:
    data = { 
        'Name': ['John', 'Jane', 'Bob', 'Alice', 'Mike', 'Sara','Mark','Eric','John','Jane','Bob','Alice','Mike','Sara','Mark','Eric'],
        'Age': [28, 22, 34, 42, 19, 31, 67,28, 22, 34, 42, 19, 31, 67,28, 22],
        'City': ['New York','New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia','San Francisco','New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia','San Francisco']
    }
    
    print(f"Name count: {len(data['Name'])}")
    print(f"Age count: {len(data['Age'])}")
    print(f"City count: {len(data['City'])}")
    
    df = pd.DataFrame(data)
    print("DataFrame created successfully")
    
except ValueError as e:
    print(f"\n❌ Error caught: {e}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
