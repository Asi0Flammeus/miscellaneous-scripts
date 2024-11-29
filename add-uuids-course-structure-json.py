import os
import json
import re

def extract_uuids_from_markdown(file_path):
    part_pattern = re.compile(r'# (.+?)\n<partId>(.+?)</partId>')
    chapter_pattern = re.compile(r'## (.+?)\n<chapterId>(.+?)</chapterId>')

    parts = {}
    chapters = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        for part_match in part_pattern.finditer(content):
            part_name = part_match.group(1).strip()
            part_id = part_match.group(2).strip()
            parts[part_name] = part_id

        for chapter_match in chapter_pattern.finditer(content):
            chapter_name = chapter_match.group(1).strip()
            chapter_id = chapter_match.group(2).strip()
            chapters[chapter_name] = chapter_id

    return parts, chapters

def update_course_json(course_json_path, part_ids, chapter_ids):
    with open(course_json_path, 'r', encoding='utf-8') as file:
        course_data = json.load(file)
    
    course_name = list(course_data.keys())[0]
    
    for part_name_en, part_id in part_ids.items():
        for key, value in course_data[course_name].items():
            if 'fr' in value and value['fr'] == part_name_en:
                course_data[course_name][key]['uuid'] = part_id
    
    for chapter_name_en, chapter_id in chapter_ids.items():
        for key, value in course_data[course_name].items():
            if 'fr' in value and value['fr'] == chapter_name_en:
                course_data[course_name][key]['uuid'] = chapter_id
    
    with open(course_json_path, 'w', encoding='utf-8') as file:
        json.dump(course_data, file, ensure_ascii=False, indent=4)

    print(f'Updated {course_json_path} with part and chapter UUIDs.')


def process_courses(course_structure_path, courses_path):
    for course_file in os.listdir(course_structure_path):
        if course_file.endswith('.json'):
            course_name = course_file.split('_')[0]
            course_json_path = os.path.join(course_structure_path, course_file)
            course_md_path = os.path.join(courses_path, course_name, 'fr.md')

            if os.path.exists(course_md_path):
                part_ids, chapter_ids = extract_uuids_from_markdown(course_md_path)
                update_course_json(course_json_path, part_ids, chapter_ids)
            else:
                print(f'Markdown file not found for course {course_name}.')

if __name__ == "__main__":
    course_structure_path = './course_structure/'
    courses_path = '../sovereign-university-data/courses/'

    process_courses(course_structure_path, courses_path)

