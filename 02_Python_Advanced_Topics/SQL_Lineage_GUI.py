import tkinter as tk
from tkinter import scrolledtext, ttk
import sqlglot
from sqlglot.expressions import Column, Table, Subquery, Select
import pandas as pd

# Global lineage list
lineage = []

def resolve_columns(table_alias, column_name, alias_map):
    """Resolve column lineage from alias map"""
    if table_alias in alias_map:
        mapping = alias_map[table_alias]
        if column_name in mapping:
            return mapping[column_name]
    return (None, table_alias, column_name)  # Fallback if not mapped

def extract_lineage(expr, alias_map=None):
    """Extract lineage from SQL expression"""
    global lineage
    
    if alias_map is None:
        alias_map = {}
        
    # Process subqueries
    for subquery in expr.find_all(Subquery):
        sub_alias = subquery.alias
        sub_select = subquery.this
        
        if sub_select and 'from' in sub_select.args:
            sub_from = sub_select.args['from'].this
            
            if isinstance(sub_from, Table):
                schema = sub_from.args.get('db')
                schema_name = schema.name if schema else None
                table_name = sub_from.this.name
                col_map = {}
                
                for proj in sub_select.args.get('expressions', []):
                    if isinstance(proj, Column):
                        col_name = proj.name
                        col_map[col_name] = (schema_name, table_name, col_name)
                
                alias_map[sub_alias] = col_map
                
                # Recursion into the subquery
                extract_lineage(sub_select, alias_map=alias_map)
    
    # Handle current Select
    if isinstance(expr, Select):
        for proj in expr.expressions:
            tgt_col = proj.alias_or_name
            if not tgt_col:
                continue
                
            for src_col in proj.find_all(Column):
                from_col = src_col.name
                from_table = src_col.table or next(iter(alias_map), None) if alias_map else None
                from_schema, from_table_resolved, from_col_resolved = resolve_columns(from_table, from_col, alias_map)
                
                lineage.append({
                    'From_Schema': from_schema, 
                    'From_Table': from_table_resolved, 
                    'From_Column': from_col_resolved,
                    'To_Schema': None,
                    'To_Table': None,
                    'To_Column': tgt_col,
                    'Transformation': proj.sql()
                })

def parse_sql():
    """Parse SQL and display lineage"""
    global lineage
    lineage = []
    sql = text_area.get("1.0", tk.END).strip()
    
    if not sql:
        return
    
    try:
        parsed = sqlglot.parse_one(sql)
        extract_lineage(parsed)
        df = pd.DataFrame(lineage)
        
        # Clear previous results
        for i in tree.get_children():
            tree.delete(i)
        
        # Insert new results
        if not df.empty:
            for index, row in df.iterrows():
                tree.insert(parent="", index="end", values=list(row))
        else:
            print("No lineage found in the SQL query")
    except Exception as e:
        print(f"Error parsing SQL: {e}")

# Create main window
root = tk.Tk()
root.title("SQL Lineage Parser")
root.geometry("900x700")

# SQL Input Section
tk.Label(root, text="Enter SQL Query", font=("Arial", 16, "bold")).pack(pady=10)
text_area = tk.Text(root, height=10, width=100, font=("Courier", 10))
text_area.pack(pady=10, padx=10)

# Parse button
tk.Button(root, text="Parse SQL", command=parse_sql, font=("Arial", 12, "bold"), 
          bg="#4CAF50", fg="white", padx=20, pady=5).pack(pady=10)

# Results Section
tk.Label(root, text="Lineage Results", font=("Arial", 14, "bold")).pack(pady=5)

# Create Treeview with scrollbar
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, 
                    columns=('From_Schema', 'From_Table', 'From_Column', 'To_Schema', 'To_Table', 'To_Column', 'Transformation'), 
                    show='headings', 
                    height=12,
                    yscrollcommand=tree_scroll.set)

tree_scroll.config(command=tree.yview)

# Configure column headings
tree.heading('From_Schema', text='From Schema')
tree.heading('From_Table', text='From Table')
tree.heading('From_Column', text='From Column')
tree.heading('To_Schema', text='To Schema')
tree.heading('To_Table', text='To Table')
tree.heading('To_Column', text='To Column')
tree.heading('Transformation', text='Transformation')

# Configure column widths
tree.column('From_Schema', width=100)
tree.column('From_Table', width=120)
tree.column('From_Column', width=120)
tree.column('To_Schema', width=100)
tree.column('To_Table', width=120)
tree.column('To_Column', width=120)
tree.column('Transformation', width=200)

tree.pack(fill=tk.BOTH, expand=True)

# Start the GUI
root.mainloop()
#SQL_Lineage_GUI.py

import tkinter as tk
from tkinter import scrolledtext, ttk
import sqlglot
from sqlglot.expressions import Column, Table, Subquery, Select
import pandas as pd

#Create a window

root = tk.Tk()
root.title('SQL Lineage Parser')

#Input area for SQL
tk.Label(root, text="Enter SQL Statement:").pack()
text_area = scrolledtext.ScrolledText(root,width=80,height=10)
text_area.pack()

#Collect lineage rows
lineage=[]

def resolve_column(table_alias,column_name, alias_map):
    if table_alias in alias_map:
        mapping = alias_map[table_alias]

        if column_name in mapping:
            return mapping[column_name]
        
    return (None, table_alias, column_name) #Fallback if not mapped

def extract_lineage(expr, alias="anonymous", alias_map=None):
    if alias_map is None:
        alias_map = {}

    #Map Subqueries

    for subquery in expr.find_all(Subquery):
        sub_alias = subquery.alias
        sub_select = subquery.this
        sub_from = sub_select.args['from'].this
        if isinstance(sub_from, Table):
            schema = sub_from.args.get("db") 
            schema_name = schema.name if schema else None
            table_name = sub_from.this.name
            col_map = {}
            for proj in sub_select.args['expressions']:
                if isinstance(proj, Column):
                    col_name = proj.name
                    col_map[col_name] = (schema_name,table_name,col_name)
            alias_map[sub_alias]=col_map
            #Rescursion into the subquery
        extract_lineage(sub_select, alias=sub_alias,alias_map=alias_map)
        
        # Handle current Select        
    if isinstance(expr,Select):
        for proj in expr.expressions:
            tgt_col = proj.alias_or_name
            if not tgt_col:
                continue
            for src_col in proj.find_all(Column):
                from_table = src_col.table or next(iter(alias_map),None)
                from_col = src_col.name
                from_schema,from_table_resolved,from_col_resolved = resolve_column(from_table,from_col,alias_map)
                lineage.append({
                "From_Schema": from_schema,
                "From_Table": from_table_resolved,
                "From_Column": from_col_resolved,
                "To_Schema": None,
                "To_Table": alias,
                "To_Column": tgt_col,
                "Transformation": proj.sql()
            })
def parse_sql():
    global lineage
    lineage = []

    sql = text_area.get("1.0",tk.END).strip()

    try:
        #Parse the query
        parsed = sqlglot.parse_one(sql)

        #Extract Lineage
        extract_lineage(parsed)

        #Create DataFrame
        df = pd.DataFrame(lineage)

        #Clear previous results
        for i in tree.get_children():
            tree.delete(i)

        if not df.empty:
            #Insert data into TreeView
            for _,row in df.iterrows():
                tree.insert('','end',values=(
                row.get('From_Schema', 'None'),
                row.get('From_Table', 'Unknown'),
                row.get('From_Column', 'Unknown'),
                row.get('To_Column', 'Unknown'),
                row.get('Transformation', 'None')
                ))

            error_label.config(text="")

        else:
            error_label.config(text="No lineage found. Please enter a valid SELECT statement.")
    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

# Parse button
tk.Button(root, text="Parse", command=parse_sql).pack()

# Treeview to display lineage in tabular format
tree = ttk.Treeview(root, columns=('From_Schema', 'From_Table', 'From_Column', 'To_Column', 'Transformation'), show='headings')
tree.heading('From_Schema', text='From Schema')
tree.heading('From_Table', text='From Table')
tree.heading('From_Column', text='From Column')
tree.heading('To_Column', text='To Column')
tree.heading('Transformation', text='Transformation')
tree.pack()

# Error label for displaying messages
error_label = tk.Label(root, text="", fg="red")
error_label.pack()


root.mainloop()