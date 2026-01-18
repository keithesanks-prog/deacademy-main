# Example 1: Temperature Converter GUI
# A simple GUI to demonstrate Tkinter basics

import tkinter as tk
from tkinter import ttk

def convert_temperature():
    """Convert temperature based on selected direction"""
    try:
        temp = float(temp_entry.get())
        direction = conversion_var.get()
        
        if direction == "C to F":
            result = (temp * 9/5) + 32
            result_label.config(
                text=f"{temp}°C = {result:.2f}°F",
                fg="green"
            )
        else:  # F to C
            result = (temp - 32) * 5/9
            result_label.config(
                text=f"{temp}°F = {result:.2f}°C",
                fg="green"
            )
    except ValueError:
        result_label.config(
            text="Please enter a valid number",
            fg="red"
        )

# Create main window
root = tk.Tk()
root.title("Temperature Converter")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Title
tk.Label(
    root, 
    text="🌡️ Temperature Converter",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
).pack(pady=20)

# Input frame
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Temperature:",
    font=("Arial", 12),
    bg="#f0f0f0"
).grid(row=0, column=0, padx=5)

temp_entry = tk.Entry(input_frame, width=15, font=("Arial", 12))
temp_entry.grid(row=0, column=1, padx=5)

# Conversion direction
conversion_var = tk.StringVar(value="C to F")

radio_frame = tk.Frame(root, bg="#f0f0f0")
radio_frame.pack(pady=10)

tk.Radiobutton(
    radio_frame,
    text="Celsius → Fahrenheit",
    variable=conversion_var,
    value="C to F",
    font=("Arial", 11),
    bg="#f0f0f0"
).pack(anchor=tk.W)

tk.Radiobutton(
    radio_frame,
    text="Fahrenheit → Celsius",
    variable=conversion_var,
    value="F to C",
    font=("Arial", 11),
    bg="#f0f0f0"
).pack(anchor=tk.W)

# Convert button
tk.Button(
    root,
    text="Convert",
    command=convert_temperature,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=5
).pack(pady=15)

# Result label
result_label = tk.Label(
    root,
    text="Enter a temperature and click Convert",
    font=("Arial", 12),
    bg="#f0f0f0"
)
result_label.pack(pady=10)

# Start the application
root.mainloop()
