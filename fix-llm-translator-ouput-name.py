import os

def rename_files_in_directory(directory):
    # Define the prefixes that need to be processed
    prefixes = ["professors_", "books_", "builders_", "exchange_", "privacy_", "merchant_", "others_", "wallet_", "node_", "mining_"]
    suffix = "_vietnamese"

    # List all files in the directory
    for filename in os.listdir(directory):
        # Ensure the filename is in lowercase
        new_filename = filename.lower()
        
        # Check if the file matches the pattern and replace '_' with '-'
        for prefix in prefixes:
            if new_filename.startswith(prefix) and new_filename.endswith(suffix):
                start_index = len(prefix)
                end_index = new_filename.rfind(suffix)
                part_to_replace = new_filename[start_index:end_index]
                new_part = part_to_replace.replace('_', '-')
                new_filename = new_filename[:start_index] + new_part + new_filename[end_index:]
                break  # Exit the loop once the correct prefix is found

        # Rename the file if the name has changed
        if new_filename != filename:
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_filename}'")
        else:
            print(f"No change for '{filename}'")

if __name__ == "__main__":
    directory_path = "../LLM-Translator/outputs/planb-content/vi/"
    rename_files_in_directory(directory_path)

