import os

def modify_file_content(path, file_name):
    if file_name == "conference.yml":
        modify_lines = lambda line: line.replace('Builder:', 'builder:') if line.startswith('Builder:') else line
    elif file_name == "en.md":
        modify_lines = lambda line: line.replace('Name:', 'name:') if line.startswith('Name:') else \
                                    line.replace('Description:', 'description:') if line.startswith('Description:') else line
    else:
        return  # No modification needed for other files

    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines([modify_lines(line) for line in lines])

def rename_file(path, new_name):
    os.rename(path, new_name)

def process_directory(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(root, file)
            if file == "conference.yml" or file == "en.md":
                modify_file_content(path, file)
            if file.startswith("thumbnails"):
                new_name = os.path.join(root, file.replace("thumbnails", "thumbnail"))
                rename_file(path, new_name)

# Call the function with the path to the directory you want to process
process_directory("./")

