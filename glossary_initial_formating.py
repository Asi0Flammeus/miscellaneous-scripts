import os
import re
import shutil

def get_foldername_from_file(filepath):
    print(f"Reading term from file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("term:"):
                raw_foldername = line.split("term: ")[1].strip()
                break
    raw_foldername = re.sub(r'[^\w\s]', '', raw_foldername)  # Remove special characters
    foldername = raw_foldername.lower().replace(" ", "-").replace("_", "-")
    foldername = foldername.strip("-")
    print(f"Raw foldername: {raw_foldername} -> Processed foldername: {foldername}")
    return foldername

def main():
    base_path = "../glossary"
    print(f"Starting process in directory: {base_path}")
    for filename in os.listdir(base_path):
        if filename.endswith("_en.md"):
            print(f"Processing file: {filename}")
            initial_filename = filename.replace("_en.md", "")
            filepath = os.path.join(base_path, filename)
            foldername = get_foldername_from_file(filepath)
            folder_path = os.path.join(base_path, foldername)
            
            print(f"Creating folder: {folder_path}")
            os.makedirs(folder_path, exist_ok=True)
            
            for file in os.listdir(base_path):
                if file.startswith(initial_filename):
                    old_file_path = os.path.join(base_path, file)
                    if file == initial_filename + "_en.md":
                        new_file_path = os.path.join(folder_path, "en.md")
                        print(f"Moving {old_file_path} to {new_file_path}")
                        shutil.move(old_file_path, new_file_path)
                    elif file == initial_filename + ".md":
                        new_file_path = os.path.join(folder_path, "fr.md")
                        print(f"Moving {old_file_path} to {new_file_path}")
                        shutil.move(old_file_path, new_file_path)
            print("")
    print("Process completed.")

if __name__ == "__main__":
    main()

