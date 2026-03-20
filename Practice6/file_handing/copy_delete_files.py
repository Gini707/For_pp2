import shutil
import os

# copy
shutil.copy("sample.txt", "sample_backup.txt")
print("File copied successfully.")

# delete
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup file deleted.")
else:
    print("File does not exist.")