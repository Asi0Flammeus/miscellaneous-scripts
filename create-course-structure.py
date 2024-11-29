import os
import json
import re

def parse_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    parts = []
    current_part = None
    current_chapter = None
    is_indexing = False

    for line in content.splitlines():
        if line.strip() == '+++':
            is_indexing = True
            continue

        if not is_indexing:
            continue

        part_match = re.match(r'^# (.+)', line)
        chapter_match = re.match(r'^## (.+)', line)

        if part_match:
            if current_part:
                parts.append(current_part)
            current_part = {'title': part_match.group(1), 'chapters': []}
            current_chapter = None

        elif chapter_match and current_part:
            current_chapter = chapter_match.group(1)
            current_part['chapters'].append(current_chapter)

    if current_part:
        parts.append(current_part)

    return parts

def build_course_structure(subfolder):
    course_structure = {}

    for subdir, _, files in os.walk(subfolder):
        if subdir != subfolder:  # Skip nested subdirectories
            continue
        subfolder_name = os.path.basename(subdir)
        if subfolder_name not in course_structure:
            course_structure[subfolder_name] = {}

        for file in files:
            if file.endswith('.md'):
                language = os.path.splitext(file)[0]
                file_path = os.path.join(subdir, file)
                parts = parse_md_file(file_path)
                if not parts:
                    continue

                for i, part in enumerate(parts):
                    part_title_key = f"Part {i+1}"
                    if part_title_key not in course_structure[subfolder_name]:
                        course_structure[subfolder_name][part_title_key] = {}

                    course_structure[subfolder_name][part_title_key][language] = part['title']

                    for j, chapter in enumerate(part['chapters']):
                        chapter_title_key = f"Part {i+1} Chapter {j+1}"
                        if chapter_title_key not in course_structure[subfolder_name]:
                            course_structure[subfolder_name][chapter_title_key] = {}

                        course_structure[subfolder_name][chapter_title_key][language] = chapter

    return course_structure

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root_folder = '../sovereign-university-data/courses/'
    output_folder = './course_structure'
    os.makedirs(output_folder, exist_ok=True)

    for course in os.listdir(root_folder):
        course_path = os.path.join(root_folder, course)
        if os.path.isdir(course_path):  # Process only directories
            course_structure = build_course_structure(course_path)
            output_file = os.path.join(output_folder, f"{course}_course_structure.json")
            save_json(course_structure, output_file)

