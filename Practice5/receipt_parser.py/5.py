import re

text = input()
pattern = r'a.*b'

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

    # .* means any number of any characters.