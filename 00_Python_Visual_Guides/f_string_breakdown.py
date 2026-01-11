# Break down the f-string formatting: f'{value:.2%}'

# 1. The Math Result (a decimal)
# Let's say 2 out of 3 orders were late.
calculation_result = 2 / 3 
print(f"Raw Calculation Result: {calculation_result}") 
# Output: 0.6666666666666666

print("\n--- applying :.2% formatting ---")

# 2. The Formatting Logic
# The colon ':' tells Python "Format what comes next"
# The '.2' tells Python "Give me 2 decimal places"
# The '%' tells Python "Multiply by 100 and add a % sign"

formatted_string = f"{calculation_result:.2%}"
print(f"Formatted Result: {formatted_string}")     
# Output: 66.67%

print("\n--- Other Examples ---")
print(f"0.5 formatted as .2%  -> {0.5:.2%}")   # 50.00%
print(f"0.123 formatted as .2% -> {0.123:.2%}") # 12.30%
print(f"1.0 formatted as .2%  -> {1.0:.2%}")    # 100.00%
