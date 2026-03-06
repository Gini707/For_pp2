import re

text = input()

result = re.split(r'(?=[A-Z])', text)
print(result)

#(?=[A-Z]) space before a upper letter