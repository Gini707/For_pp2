import re

text = input()
pattern = r'ab{2,3}'

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

#вся строка соответсвует шаблону fullmatch the entire string matches the pattern 