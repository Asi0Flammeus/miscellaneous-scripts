import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified = False
    for i, line in enumerate(lines):
        if line.startswith("![") and not line.rstrip().endswith(")"):
            lines[i] = line.rstrip() + ")\n"
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print(f"Updated: {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'en.md':
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    start_directory = '../sovereign-university-data/resources/conference/'  # start directory, adjust as needed
    process_directory(start_directory)

