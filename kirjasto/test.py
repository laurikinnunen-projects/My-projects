import os
print(os.path.abspath("library.db"))

# Test code snippet to remove databases used during the testing phase
# In the repo there is method with same functionality, this does it without running main

db_path = os.path.abspath("library.db")
if os.path.exists(db_path):
    os.remove(db_path)
    print("deleted")
else:
    print("no file")