import re
text = input()
pattern = r'[a-z]+_[a-z]+'
matches = re.findall(pattern, text)
print(matches)