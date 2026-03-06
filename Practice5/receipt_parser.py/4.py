import re

text = input()
pattern = r'[A-Z][a-z]+'

matches = re.findall(pattern, text)
print(matches)