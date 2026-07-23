import os

documents_folder = "documents"

# List all files in the documents folder
files = os.listdir(documents_folder)
print(f"Found {len(files)} files:\n")

for filename in files:
    filepath = os.path.join(documents_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"File: {filename}")
    print(f"Length: {len(content)} characters")
    print(f"Preview: {content[:100]}...")
    print()