import json

# with open('example.json', 'r') as file:
#     data = json.load(file)

# print(data)

data = {'name': 'John', 'age': 30, 'city': 'New York'}
with open('test.json', 'w') as file:
    json.dump(data, file, indent=4)

