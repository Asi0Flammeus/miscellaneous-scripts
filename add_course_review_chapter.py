import os
import uuid

# Define the dictionary with language codes and their corresponding feedback request in each language
feedback_requests = {
    'cs': 'Dejte nám zpětnou vazbu k tomuto kurzu',
    'de': 'Geben Sie uns Ihr Feedback zu diesem Kurs',
    'en': 'Give us some feedback about this course',
    'es': 'Danos tu opinión sobre este curso',
    'et': 'Andke meile tagasisidet selle kursuse kohta',
    'fi': 'Anna meille palautetta tästä kurssista',
    'fr': 'Donnez-nous votre avis sur ce cours',
    'id': 'Beri kami umpan balik tentang kursus ini',
    'it': 'Dacci un feedback su questo corso',
    'ja': 'このコースについてのフィードバックをお寄せください',
    'pt': 'Dê-nos seu feedback sobre este curso',
    'ru': 'Оставьте отзыв о данном курсе',
    'vi': 'Cho chúng tôi biết phản hồi của bạn về khóa học này',
    'zh-Hans': '给我们关于这门课程的反馈'
}

def generate_uuid_from_path(path):
    # Namespace UUID for version 5 UUIDs (You can generate your own namespace UUID or use one of the predefined)
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # Namespace for URL as example
    return str(uuid.uuid5(namespace, path))

def insert_feedback_section(file_path, language_code, folder_uuid):
    # Read the existing content from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Check if the feedback section is already added
    if any('<isCourseReview>true</isCourseReview>' in line for line in content):
        print(f"Feedback section already exists in {file_path}. Skipping...")
        return

    # Define the section to be added
    insert_text = f"\n## {feedback_requests[language_code]}\n<chapterId>{folder_uuid}</chapterId>\n<isCourseReview>true</isCourseReview>\n"

    # Find the last "## " heading and get the index
    headings = [index for index, line in enumerate(content) if line.startswith("## ")]
    if not headings:
        # If no heading found, append to the end of the file
        content.append(insert_text)
    else:
        # Insert the text before the last heading
        last_heading_index = headings[-1]
        content.insert(last_heading_index, insert_text)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def search_and_update_files(start_path):
    # Walk through all directories and files in the given path
    for root, dirs, files in os.walk(start_path):
        # Generate a UUID based on the directory path for consistent use in this directory
        folder_uuid = generate_uuid_from_path(root)
        for file in files:
            # Check if the file name matches any language code with .md extension
            if file.split('.')[-1] == 'md' and file.split('.')[0] in feedback_requests:
                file_path = os.path.join(root, file)
                language_code = file.split('.')[0]
                insert_feedback_section(file_path, language_code, folder_uuid)

# Set the directory path where the script should start processing
# start_path = '../bitcoin-educational-content/courses/'
start_path = '../bitcoin-educational-content/courses/'

# Call the function to start the process
search_and_update_files(start_path)

