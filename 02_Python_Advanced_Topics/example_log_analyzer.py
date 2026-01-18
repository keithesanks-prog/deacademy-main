# Example 2: Log File Analyzer GUI
# Demonstrates file handling and Treeview widget

import tkinter as tk
from tkinter import ttk, filedialog
from collections import Counter
import os

def analyze_log():
    """Analyze log file and display statistics"""
    # Open file dialog
    filepath = filedialog.askopenfilename(
        title="Select Log File",
        filetypes=[
            ("Log files", "*.log"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    
    if not filepath:
        return  # User cancelled
    
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Count log levels
        log_levels = Counter()
        for line in lines:
            line_upper = line.upper()
            if 'ERROR' in line_upper:
                log_levels['ERROR'] += 1
            elif 'WARNING' in line_upper or 'WARN' in line_upper:
                log_levels['WARNING'] += 1
            elif 'INFO' in line_upper:
                log_levels['INFO'] += 1
            elif 'DEBUG' in line_upper:
                log_levels['DEBUG'] += 1
        
        # Update file info
        filename = os.path.basename(filepath)
        file_label.config(text=f"File: {filename}")
        total_label.config(text=f"Total Lines: {len(lines)}")
        
        # Clear previous results
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert results
        for level, count in log_levels.most_common():
            percentage = (count / len(lines)) * 100
            tree.insert('', 'end', values=(level, count, f"{percentage:.1f}%"))
        
        status_label.config(text="✓ Analysis complete", fg="green")
        
    except Exception as e:
        status_label.config(text=f"✗ Error: {str(e)}", fg="red")

def create_sample_log():
    """Create a sample log file for testing"""
    sample_content = """2026-01-11 10:00:01 INFO Application started
2026-01-11 10:00:05 DEBUG Loading configuration
2026-01-11 10:00:10 INFO Configuration loaded successfully
2026-01-11 10:01:15 WARNING High memory usage detected
2026-01-11 10:02:30 ERROR Failed to connect to database
2026-01-11 10:02:31 ERROR Connection timeout after 30 seconds
2026-01-11 10:03:00 INFO Retrying connection
2026-01-11 10:03:05 INFO Connected to database successfully
2026-01-11 10:05:00 DEBUG Processing batch 1 of 10
2026-01-11 10:06:00 DEBUG Processing batch 2 of 10
2026-01-11 10:07:00 WARNING Slow query detected (3.5s)
2026-01-11 10:08:00 INFO Batch processing complete
"""
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".log",
        filetypes=[("Log files", "*.log"), ("All files", "*.*")]
    )
    
    if filepath:
        with open(filepath, 'w') as f:
            f.write(sample_content)
        status_label.config(text=f"✓ Sample log created: {os.path.basename(filepath)}", fg="green")

# Create main window
root = tk.Tk()
root.title("Log File Analyzer")
root.geometry("700x500")

# Title
tk.Label(
    root,
    text="📊 Log File Analyzer",
    font=("Arial", 18, "bold")
).pack(pady=15)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="📁 Select Log File",
    command=analyze_log,
    font=("Arial", 11, "bold"),
    bg="#2196F3",
    fg="white",
    padx=15,
    pady=5
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="📝 Create Sample Log",
    command=create_sample_log,
    font=("Arial", 11),
    bg="#9E9E9E",
    fg="white",
    padx=15,
    pady=5
).pack(side=tk.LEFT, padx=5)

# File info frame
info_frame = tk.Frame(root)
info_frame.pack(pady=10)

file_label = tk.Label(info_frame, text="No file selected", font=("Arial", 10))
file_label.pack()

total_label = tk.Label(info_frame, text="", font=("Arial", 10))
total_label.pack()

# Results label
tk.Label(
    root,
    text="Log Level Statistics",
    font=("Arial", 12, "bold")
).pack(pady=10)

# Treeview for results
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(
    tree_frame,
    columns=('Level', 'Count', 'Percentage'),
    show='headings',
    height=8,
    yscrollcommand=tree_scroll.set
)

tree_scroll.config(command=tree.yview)

tree.heading('Level', text='Log Level')
tree.heading('Count', text='Count')
tree.heading('Percentage', text='Percentage')

tree.column('Level', width=150, anchor=tk.CENTER)
tree.column('Count', width=100, anchor=tk.CENTER)
tree.column('Percentage', width=100, anchor=tk.CENTER)

tree.pack(fill=tk.BOTH, expand=True)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=10)

# Start the application
root.mainloop()
