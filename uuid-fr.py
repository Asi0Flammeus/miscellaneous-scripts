import os
import uuid
import hashlib
import json

# Constant seed UUID for deterministic namespace generation
SEED_NAMESPACE = uuid.UUID('1b671a63-40d5-491e-99b0-da01ff1f3300')

def generate_namespace_uuid(folder_path):
    # Generate a consistent namespace UUID based on the folder path
    hasher = hashlib.md5()
    hasher.update(folder_path.encode('utf-8'))
    namespace = uuid.UUID(hasher.hexdigest())
    return uuid.uuid5(SEED_NAMESPACE, str(namespace))

def generate_uuid(namespace, identifier):
    # Generate a UUID based on the folder-specific namespace and identifier
    return str(uuid.uuid5(namespace, identifier))  # Return UUID string with dashes

def process_folder_for_fr(folder_path, folder_name, namespace):
    header_info = []  # Use a list to maintain the order of headers
    # fr_filepath = os.path.join(folder_path, 'fr.md')
    fr_filepath = os.path.join(folder_path, 'it.md')
    process_markdown(fr_filepath, header_info, namespace)

    # Save the header info to a JSON file named with the folder name
    script_location = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the script
    json_filename = f"{folder_name}_header_scheme_fr.json"
    json_path = os.path.join(script_location, json_filename)
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(header_info, json_file, indent=4)

def process_markdown(filepath, header_info, namespace):
    with open(filepath, 'r', encoding='utf-8') as f:
        contents = f.readlines()

    updated_contents, part_count, chapter_count = [], 0, 0
    start_counting = False

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

def apply_uuids_to_file_for_fr(folder_path, filename, header_info, namespace):
    filepath = os.path.join(folder_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        contents = f.readlines()

    updated_contents = []
    header_index = 0  # Start at the first header
    start_applying = False

    for line in contents:
        updated_contents.append(line)
        if line.strip() == "+++":
            start_applying = True
            continue

        if start_applying and header_index < len(header_info):
            header = header_info[header_index]
            header_tag = f"<{header['type']}Id>"
            if header['type'] == "part" and line.startswith('# ') and not line.startswith('## '):
                if header_tag in line:
                    current_uuid = line.split(header_tag)[1].split('</')[0]
                    if current_uuid != header['uuid']:
                        updated_contents.append(f"{header_tag}{header['uuid']}</{header['type']}Id>\n")
                else:
                    updated_contents.append(f"{header_tag}{header['uuid']}</{header['type']}Id>\n")
                header_index += 1
            elif header['type'] == "chapter" and line.startswith('## '):
                if header_tag in line:
                    current_uuid = line.split(header_tag)[1].split('</')[0]
                    if current_uuid != header['uuid']:
                        updated_contents.append(f"{header_tag}{header['uuid']}</{header['type']}Id>\n")
                else:
                    updated_contents.append(f"{header_tag}{header['uuid']}</{header['type']}Id>\n")
                header_index += 1

    # Write the updated contents back to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(updated_contents)

def process_files_and_insert_uuids_for_fr(path):
    # Process each folder in the given path
    for root, dirs, files in os.walk(path):
        # if 'fr.md' in files:
        if 'it.md' in files:
            folder_name = os.path.basename(root)
            # Generate a unique namespace UUID for each folder based on its path
            namespace = generate_namespace_uuid(root)
            process_folder_for_fr(root, folder_name, namespace)

# Main execution path
path = '../planB-premium-content/courses/btc105/'
process_files_and_insert_uuids_for_fr(path)

