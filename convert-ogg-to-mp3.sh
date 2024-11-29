#!/bin/bash

# Directory containing the OGG files
directory="$HOME/Vault/pro/DB/workspace/DécouvreBitcoin/DB-Assets/journalling/audios/"

# Loop through all the OGG files in the directory
for file in "$directory"/*.ogg
do
    if [ -f "$file" ]; then
        # Construct the new MP3 filename
        newfile="${file%.ogg}.mp3"

        # Convert OGG to MP3
        ffmpeg -i "$file" -acodec libmp3lame "$newfile"

        # Remove the original OGG file if the conversion was successful
        if [ $? -eq 0 ]; then
            rm "$file"
        else
            echo "Failed to convert $file"
        fi
    fi
done
