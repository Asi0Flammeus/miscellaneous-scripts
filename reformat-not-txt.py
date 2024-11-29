import os
import shutil
import re

def move_and_delete_images(base_directory):
    assets_directory = os.path.join(base_directory, 'assets')
    notext_directory = os.path.join(assets_directory, 'notext')
    if not os.path.exists(notext_directory):
        os.mkdir(notext_directory)
    
    image_numbers = input("Entrez les numéros des images notext séparés par un espace : ").split()
    
    image_extensions = ['png', 'webp', 'jpeg']
    
    language_codes = ['fr', 'en', 'es', 'de', 'it', 'pt']

    for number in image_numbers:
        moved = False
        for extension in image_extensions:
            source_path = os.path.join(assets_directory, 'fr', f'{number}.{extension}')
            if os.path.exists(source_path):
                shutil.move(source_path, os.path.join(notext_directory, f'{number}.{extension}'))
                moved = True
                for code in language_codes:
                    image_path = os.path.join(assets_directory, code, f'{number}.{extension}')
                    if os.path.exists(image_path):
                        os.remove(image_path)
                break
        if moved:
            for code in language_codes:
                markdown_file = os.path.join(base_directory, f'{code}.md')
                if os.path.exists(markdown_file):
                    with open(markdown_file, 'r', encoding='utf-8') as file:
                        content = file.read()
                    content = re.sub(
                        rf'\!\[(.*?)\]\(assets/{code}/{number}\.{extension}\)',
                        rf'![\1](assets/notext/{number}.{extension})',
                        content
                    )
                    with open(markdown_file, 'w', encoding='utf-8') as file:
                        file.write(content)

if __name__ == "__main__":
    article_folder = input("Entrez le chemin du dossier de l'article : ")
    move_and_delete_images(article_folder)
