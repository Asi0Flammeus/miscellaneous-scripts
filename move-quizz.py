import os
import shutil

def move_quiz_folders(base_path):
    quizzes_path = os.path.join(base_path, "quizzes/questions")
    destination_base_path = os.path.join(base_path)

    # Dictionary to keep track of the folder numbering for each course
    course_counters = {}

    # Process folders in order named "1", "2", etc.
    for i in range(1, 954):  # Adjust the range as needed for the maximum expected folders
        subfolder_name = str(i)
        subfolder_path = os.path.join(quizzes_path, subfolder_name)
        question_file_path = os.path.join(subfolder_path, "question.yml")

        if os.path.exists(question_file_path):
            # Read the course property from question.yml
            with open(question_file_path, 'r') as file:
                lines = file.readlines()
                course = None
                for line in lines:
                    if line.startswith('course:'):
                        course = line.split(':')[1].strip()
                        break

            if course:
                # Determine the destination path
                destination_path = os.path.join(destination_base_path, "courses", course, "quizz")
                os.makedirs(destination_path, exist_ok=True)

                # Get the current counter for this course and increment it
                counter = course_counters.get(course, 0)
                new_folder_name = f"{counter:03}"
                course_counters[course] = counter + 1

                # Move and rename the folder
                destination_folder = os.path.join(destination_path, new_folder_name)
                shutil.move(subfolder_path, destination_folder)
                print(f"Moved {subfolder_path} to {destination_folder}")

# Call the function with the base path
base_path = "../sovereign-university-data"
move_quiz_folders(base_path)

