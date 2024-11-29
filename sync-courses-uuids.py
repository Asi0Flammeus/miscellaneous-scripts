import os
import json
import re

def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)

def normalize_text(text):
    """ Normalize text for better matching. """
    return re.sub(r'\s+', ' ', text).strip().lower()

def find_uuid(title, course_data, lang_code):
    """ Find the UUID for a given title. """
    title = normalize_text(title)
    for key, value in course_data.items():
        if title == normalize_text(value.get(lang_code, '')):
            return value.get('uuid')
    return None

def update_md_file(md_path, course_data, lang_code):
    with open(md_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    uuid_inserted = False

    for line in lines:
        if line.startswith('# ') or line.startswith('## '):
            title = line.strip()[2:].strip()
            uuid = find_uuid(title, course_data, lang_code)
            if uuid:
                new_lines.append(line)
                uuid_tag = 'partId' if line.startswith('# ') else 'chapterId'
                new_uuid_line = f"<{uuid_tag}>{uuid}</{uuid_tag}>\n"
                # Check if the next line already has the UUID
                if len(lines) > lines.index(line) + 1 and not lines[lines.index(line) + 1].strip().startswith('<partId>') and not lines[lines.index(line) + 1].strip().startswith('<chapterId>'):
                    new_lines.append(new_uuid_line)
                    uuid_inserted = True
                continue
        new_lines.append(line)

    if uuid_inserted:
        with open(md_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

def sync_uuids(base_dir, course_structure_dir):
    courses = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for course in courses:
        json_path = os.path.join(course_structure_dir, f"{course}_course_structure.json")
        if not os.path.exists(json_path):
            continue
        course_data = load_json(json_path)[course]
        course_folder = os.path.join(base_dir, course)
        for md_file in os.listdir(course_folder):
            if md_file.endswith('.md') and md_file != 'en.md':
                lang_code = md_file.split('.')[0]
                update_md_file(os.path.join(course_folder, md_file), course_data, lang_code)

# Example Usage
base_directory = "../sovereign-university-data/courses/"
course_structure_directory = "./course_structure/"
sync_uuids(base_directory, course_structure_directory)

