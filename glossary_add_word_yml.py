import os
import re
import yaml

def extract_en_term(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("term:"):
                en_term = line.split("term: ")[1].strip()
                return en_term
    return None

def extract_related_words(filepath):
    related_words = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if "For more information," in line:
                related_words = re.findall(r'\[(.*?)\]', line)
                return related_words
    return related_words

def clean_related_word(word):
    return word.replace('**', '')

def create_word_yaml(subfolder_path):
    en_md_path = os.path.join(subfolder_path, 'en.md')
    en_term = extract_en_term(en_md_path)
    related_words = extract_related_words(en_md_path)
    cleaned_related_words = [clean_related_word(word) for word in related_words]

    word_data = {
        'en_word': en_term,
        'related_words': cleaned_related_words,
        'tags': ['']
    }

    yaml_path = os.path.join(subfolder_path, 'word.yml')
    with open(yaml_path, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(word_data, yaml_file, default_flow_style=False, indent=2)

    print(f"Created word.yml in {subfolder_path} with en_word: {en_term} and related_words: {cleaned_related_words}")

def main():
    base_path = "../glossary"
    print(f"Starting process in directory: {base_path}")
    for subfolder in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"Processing subfolder: {subfolder}")
            en_md_path = os.path.join(subfolder_path, 'en.md')
            if os.path.exists(en_md_path):
                create_word_yaml(subfolder_path)
            else:
                print(f"en.md not found in {subfolder_path}, skipping...")
    print("Process completed.")

if __name__ == "__main__":
    main()

# BUG: the indentation doesn't word 
# NOTE: need to remove with bash the '' of the tags list
