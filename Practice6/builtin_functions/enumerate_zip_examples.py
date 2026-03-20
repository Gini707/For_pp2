# enumerate example
names = ["Alice", "Bob", "Charlie"]

for i, name in enumerate(names):
    print(i, name)

print()

# zip example
numbers = [1, 2, 3]

for name, num in zip(names, numbers):
    print(name, num)