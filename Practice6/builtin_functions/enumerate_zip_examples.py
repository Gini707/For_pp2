# enumerate example
names = ["Alice", "Bob", "Charlie"]

print("Enumerate example:")
for index, name in enumerate(names):
    print(index, name)

print()

# zip example
numbers = [10, 20, 30]

print("Zip example:")
for name, number in zip(names, numbers):
    print(name, number)