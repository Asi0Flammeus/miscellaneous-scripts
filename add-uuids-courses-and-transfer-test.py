import os
import uuid
import hashlib
import json

# Constant seed UUID for deterministic namespace generation
SEED_NAMESPACE = uuid.UUID('1b671a64-40d5-491e-99b0-da01ff1f3341')

def generate_namespace_uuid(folder_path):
    hasher = hashlib.md5()
    hasher.update(folder_path.encode('utf-8'))
    namespace = uuid.UUID(hasher.hexdigest())
    return uuid.uuid5(SEED_NAMESPACE, str(namespace))

def generate_uuid(namespace, identifier):
    return str(uuid.uuid5(namespace, identifier))  # Return UUID string with dashes

def process_folder(folder_path, folder_name, namespace):
    header_info = []  # Use a list to maintain the order of headers
    en_filepath = os.path.join(folder_path, 'en.md')
    json_filename = f"{folder_name}_header_scheme.json"
    script_location = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the script
    json_path = os.path.join(script_location, json_filename)

    if not contains_uuids(en_filepath):
        process_markdown(en_filepath, header_info, namespace)
        # Save new header info to JSON file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(header_info, json_file, indent=4)
    else:
        # Load existing header info from JSON file
        if os.path.exists(json_path):
            print("true")
            with open(json_path, 'r', encoding='utf-8') as json_file:
                header_info = json.load(json_file)
                print(header_info)

    # Apply UUIDs to other markdown files in the same folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.md') and filename != 'en.md' and not contains_uuids(os.path.join(folder_path, filename)):
            print(filename)
            print(header_info)
            apply_uuids_to_file(folder_path, filename, header_info, namespace)

def contains_uuids(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        contents = file.read()
    return "<partId>" in contents or "<chapterId>" in contents

def process_markdown(filepath, header_info, namespace):
    with open(filepath, 'r', encoding='utf-8') as f:
        contents = f.readlines()

    updated_contents, part_count, chapter_count = [], 0, 0
    start_counting = True  # Assume file starts directly with content needing UUIDs

    for line in contents:
        updated_contents.append(line)
        if line.strip() == "+++":
            start_counting = True
            continue

        if start_counting:
            if line.startswith('# ') and not line.startswith('## '):
                part_count += 1
                chapter_count = 0  # Reset chapter count for each new part
                identifier = f"part-{part_count}"
                part_uuid = generate_uuid(namespace, identifier)
                updated_contents.append(f"<partId>{part_uuid}</partId>\n")
                header_info.append({"type": "part", "uuid": part_uuid})
            elif line.startswith('## '):
                chapter_count += 1
                identifier = f"part-{part_count}-chapter-{chapter_count}"
                chapter_uuid = generate_uuid(namespace, identifier)
                updated_contents.append(f"<chapterId>{chapter_uuid}</chapterId>\n")
                header_info.append({"type": "chapter", "uuid": chapter_uuid})

    # Write the updated contents back to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(updated_contents)

def apply_uuids_to_file(folder_path, filename, header_info, namespace):
    filepath = os.path.join(folder_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        contents = f.readlines()

    updated_contents = []
    header_index = 0
    start_applying = False

    for line in contents:
        updated_contents.append(line)
        if line.strip() == "+++":
            start_applying = True
            continue

        if start_applying and header_index < len(header_info):
            if (line.startswith('# ') and not line.startswith('## ') and header_info[header_index]["type"] == "part") or \
               (line.startswith('## ') and header_info[header_index]["type"] == "chapter"):
                updated_contents.append(f"<{header_info[header_index]['type']}Id>{header_info[header_index]['uuid']}</{header_info[header_index]['type']}Id>\n")
                header_index += 1

    # Write the updated contents back to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(updated_contents)

def process_files_and_insert_uuids(path):
    # Process each folder in the given path
    for root, dirs, files in os.walk(path):
        if 'en.md' in files:
            folder_name = os.path.basename(root)
            namespace = generate_namespace_uuid(root)
            process_folder(root, folder_name, namespace)

# Main execution path
path = '../sovereign-university-data/courses/'
process_files_and_insert_uuids(path)

