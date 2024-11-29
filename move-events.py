import os
import shutil

# Set the source and destination directories
source_dir = './resources/conference'
destination_dir = './events'

# Walk through the source directory
for root, dirs, files in os.walk(source_dir):
    # Check if 'event.yml' exists in the current directory
    if 'event.yml' in files:
        # Get the current subfolder path
        subfolder = root
        # Get the folder name (last part of the path)
        folder_name = os.path.basename(subfolder)
        
        # Create the destination path
        dest_path = os.path.join(destination_dir, folder_name)
        
        # Move the entire subfolder to the destination
        try:
            shutil.move(subfolder, dest_path)
            print(f"Moved: {subfolder} -> {dest_path}")
        except Exception as e:
            print(f"Failed to move {subfolder}: {e}")
