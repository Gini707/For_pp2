import shutil
import os

# создаём папки
os.makedirs("test_folder/subfolder", exist_ok=True)

# копируем файл
shutil.copy("sample.txt", "test_folder/sample.txt")
print("File copied to test_folder.")

# копируем ещё раз
shutil.copy("test_folder/sample.txt", "test_folder/subfolder/sample_copy.txt")
print("File copied to subfolder.")