# Example 3: Email Validator with History
# Demonstrates Entry widgets, Listbox, and validation logic

import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime

def validate_email():
    """Validate email address and add to history"""
    email = email_entry.get().strip()
    
    if not email:
        result_label.config(text="Please enter an email address", fg="orange")
        return
    
    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if re.match(pattern, email):
        result_label.config(text="✓ Valid Email Address", fg="green")
        status = "✓ VALID"
        color = "green"
    else:
        result_label.config(text="✗ Invalid Email Address", fg="red")
        status = "✗ INVALID"
        color = "red"
    
    # Add to history
    history_listbox.insert(0, f"[{timestamp}] {email} - {status}")
    history_listbox.itemconfig(0, fg=color)
    
    # Clear entry
    email_entry.delete(0, tk.END)
    email_entry.focus()
    
    # Update counter
    update_counter()

def clear_history():
    """Clear validation history"""
    history_listbox.delete(0, tk.END)
    update_counter()

def update_counter():
    """Update validation counter"""
    count = history_listbox.size()
    counter_label.config(text=f"Total Validations: {count}")

# Create main window
root = tk.Tk()
root.title("Email Validator")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Title
tk.Label(
    root,
    text="📧 Email Validator",
    font=("Arial", 20, "bold"),
    bg="#f5f5f5",
    fg="#1976D2"
).pack(pady=20)

# Input frame
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Email Address:",
    font=("Arial", 12),
    bg="#f5f5f5"
).grid(row=0, column=0, padx=5, sticky=tk.E)

email_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
email_entry.grid(row=0, column=1, padx=5)
email_entry.focus()

# Bind Enter key to validate
email_entry.bind('<Return>', lambda e: validate_email())

tk.Button(
    input_frame,
    text="Validate",
    command=validate_email,
    font=("Arial", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=15,
    pady=3
).grid(row=0, column=2, padx=5)

# Result label
result_label = tk.Label(
    root,
    text="Enter an email address to validate",
    font=("Arial", 11),
    bg="#f5f5f5"
)
result_label.pack(pady=10)

# Validation rules
rules_frame = tk.LabelFrame(
    root,
    text="Validation Rules",
    font=("Arial", 10, "bold"),
    bg="#f5f5f5",
    padx=10,
    pady=5
)
rules_frame.pack(pady=10, padx=20, fill=tk.X)

rules = [
    "✓ Must contain @ symbol",
    "✓ Must have domain name after @",
    "✓ Must have valid TLD (e.g., .com, .org)",
    "✓ Can contain letters, numbers, dots, underscores"
]

for rule in rules:
    tk.Label(
        rules_frame,
        text=rule,
        font=("Arial", 9),
        bg="#f5f5f5",
        anchor=tk.W
    ).pack(anchor=tk.W)

# History section
history_frame = tk.LabelFrame(
    root,
    text="Validation History",
    font=("Arial", 11, "bold"),
    bg="#f5f5f5",
    padx=10,
    pady=5
)
history_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Listbox with scrollbar
listbox_frame = tk.Frame(history_frame, bg="#f5f5f5")
listbox_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_listbox = tk.Listbox(
    listbox_frame,
    font=("Courier", 9),
    yscrollcommand=scrollbar.set,
    height=8
)
history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=history_listbox.yview)

# Bottom frame
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(pady=10)

counter_label = tk.Label(
    bottom_frame,
    text="Total Validations: 0",
    font=("Arial", 10),
    bg="#f5f5f5"
)
counter_label.pack(side=tk.LEFT, padx=10)

tk.Button(
    bottom_frame,
    text="Clear History",
    command=clear_history,
    font=("Arial", 9),
    bg="#f44336",
    fg="white",
    padx=10
).pack(side=tk.LEFT, padx=10)

# Start the application
root.mainloop()
