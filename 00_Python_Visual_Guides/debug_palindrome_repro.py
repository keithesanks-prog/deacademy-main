def is_palindrome_broken(s):
    s = s.lower()
    s = s.replace(" ", "")
    s = s.replace(",", "")
    s = s.replace(":", "")
    return s, s[::-1], s == s[::-1]

input_str = "A man, a plan, a canal: Panama"
processed, reversed_s, result = is_palindrome_broken(input_str)

print(f"Input:    '{input_str}'")
print(f"Processed:'{processed}'")
print(f"Reversed: '{reversed_s}'")
print(f"Match:    {result}")
