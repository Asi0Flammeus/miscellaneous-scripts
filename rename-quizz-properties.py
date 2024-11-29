import os

def correct_yml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all lines and strip off extraneous whitespace and line endings
            lines = [line.strip() for line in file.readlines()]

        # Correct the lines based on your specifications
        if not lines[0].startswith("question:"):
            lines[0] = "question:" + lines[0].split(':', 1)[1]
        if not lines[1].startswith("answer:"):
            lines[1] = "answer:" + lines[1].split(':', 1)[1]
        if not lines[2].startswith("wrong_answer:"):
            lines[2] = "wrong_answer:" + lines[2].split(':', 1)[1]
        if not lines[6].startswith("explanation:"):
            lines[6] = "explanation:" + lines[6].split(':', 1)[1]
        if not lines[8].startswith("reviewed:"):
            lines[8] = "reviewed:" + lines[8].split(':', 1)[1]

        # Write the corrected lines back to the file, re-adding a newline character
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines([line + '\n' for line in lines])

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    # Recursively find all .yml files in the directory and subdirectories
    for dirpath, _, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith('.yml')]:
            file_path = os.path.join(dirpath, filename)
            correct_yml_file(file_path)

# Replace 'root_directory' with the root directory you want to process
root_directory = '../LLM-Translator/outputs/btc204/'
process_directory(root_directory)

print("Processing complete.")

