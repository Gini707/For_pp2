import re

text = input()

result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(result)

#sub replace, (?<!^) first letter not included  replace upper letter with space 