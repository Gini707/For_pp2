file = open("sample.txt", "w")
file.write("My first file.\n")
file.write("This is sample data.\n")
file.close()

print("sample.txt created")

file = open("sample.txt", "a")
file.write("This line was added later.\n")
file.write("Another new line.\n")
file.close()

print("New lines added")