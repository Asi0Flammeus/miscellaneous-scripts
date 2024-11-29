#!/bin/bash

# Function to process each conference.yml file
process_file() {
  local file="$1"
  
  # Using awk to process the file
  awk '
    /^language:/ {in_language=1; print $0; next}
    /^links:/ {in_language=0}
    in_language && /^[[:space:]]{2}[^:]+:$/ {
      # Remove the colon and add a hyphen after two spaces
      sub(/:[[:space:]]*$/, "", $0)
      print "  - " substr($0, 3)
      next
    }
    {print $0}
  ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
}

# Export the function so it can be used by find -exec
export -f process_file

# Find all conference.yml files and process them
find . -type f -name "conference.yml" -exec bash -c 'process_file "$0"' {} \;

echo "Processing completed."

