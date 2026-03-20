from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map example (квадраты чисел)
squared = list(map(lambda x: x**2, numbers))
print("Map (squared):", squared)

# filter example (только чётные)
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Filter (even):", even)

# reduce example (сумма)
total = reduce(lambda x, y: x + y, numbers)
print("Reduce (sum):", total)