import re

text = input()

result = re.sub(r'([A-Z])', r'_\1', text).lower()
print(result)

#find uuper letter   1 first save letter   r'_\1' _+найденная буква 