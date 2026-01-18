import re

# pattern = re.compile(r'(\w+)@(\w+\.\w+)')
# match = pattern.search('contact@company.com')

# if match:
#     print(match.group(0)) #Full match
#     print(match.group(1)) #Contact
#     print(match.group(2)) #Company.com


# pattern = re.compile(r'colou?r') #match color or colour
# print(pattern.search('color').group())
# print(pattern.search('colour').group())

# text = 'Emails: Info@example.com, support@example.com'
# pattern = re.compile(r'\b[\w.%+]+[\w-]+\.[a-zA-z]{2,}\b')
# emails = pattern.findall(text)
# print(emails)

#character class
# pattern = re.compile(r'[aeiou]') #match any vowel
# print(pattern.findall('Hello world'))

#phone 
# phone = "123-456-789"
# if re.match(r'^\d{3}-\d{3}-\{4}$', phone):
#     print("Valid phone number")
# else:
#     print("Invalid phone number")

#greedy matching
# text = "<p>First</p><p>Second</p>"
# greedy = re.compile(r'<p>.*</p>')


# non_greedy = re.compile(r'<p>.*?</p>')

# print(greedy.findall(text))
# print(non_greedy.findall(text))

text = "Hello World"
print(re.sub(r'world','Python',text,flags=re.IGNORECASE))