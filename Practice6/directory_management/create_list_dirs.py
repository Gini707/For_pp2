import os

# 1. Создание вложенных папок
os.makedirs("test_folder/subfolder/inner_folder", exist_ok=True)
print("Directories created")

# 2. Показать список файлов и папок
print("\nFiles and folders in current directory:")
items = os.listdir(".")

for item in items:
    print(item)

# 3. Найти файлы с расширением .txt
print("\nTXT files:")
for item in items:
    if item.endswith(".txt"):
        print(item)