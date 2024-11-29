import os
import shutil

# Define the source and destination directories
# source_dir = "../../bec-test/"
source_dir = "../../bitcoin-educational-content/"
destination_dir = "./pbn-thumbnails/"
subfolders = ["courses", "professors", "resources", "tutorials"]
tags = ["thumbnail", "profile", "cover_", "logo"]

def copy_and_rename_files():
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Loop through each specific subfolder
    for specific_folder in subfolders:
        specific_folder_path = os.path.join(source_dir, specific_folder)
        
        # Walk through each directory and subdirectory within the specific folder
        for dirpath, dirnames, filenames in os.walk(specific_folder_path):
            # Check if there's an 'assets' folder
            if 'assets' in dirnames:
                assets_path = os.path.join(dirpath, 'assets')
                
                # Process each file in the assets directory
                for filename in os.listdir(assets_path):
                    # Check if the file has the correct tag and format
                    if filename.endswith('.webp') and any(tag in filename for tag in tags):
                        # Construct the source file path
                        src_file = os.path.join(assets_path, filename)
                        
                        # Extract the path after the specific folder and use it in the new filename
                        relative_path = dirpath.split(specific_folder_path)[-1].strip(os.sep).replace(os.sep, "_")
                        new_name = f"{specific_folder}_{relative_path}_{filename}"
                        
                        # Construct the destination file path
                        dest_file = os.path.join(destination_dir, new_name)
                        
                        # Copy the file to the destination directory
                        shutil.copy(src_file, dest_file)
                        print(f"Copied {src_file} to {dest_file}")

if __name__ == "__main__":
    copy_and_rename_files()

