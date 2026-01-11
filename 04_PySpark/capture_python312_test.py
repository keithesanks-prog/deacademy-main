import subprocess
import sys

result = subprocess.run(
    [r"C:\Users\ksank\training\.venv312\Scripts\python.exe", "test_python312_fix.py"],
    cwd=r"C:\Users\ksank\training\04_PySpark",
    capture_output=True,
    text=True
)

print("=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR ===")
print(result.stderr)
print(f"\n=== EXIT CODE: {result.returncode} ===")

# Save to file
with open(r"C:\Users\ksank\training\04_PySpark\python312_test_output.txt", "w", encoding="utf-8") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n\n=== EXIT CODE: {result.returncode} ===\n")

print("\nOutput saved to python312_test_output.txt")
