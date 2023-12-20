#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Expected .csv files
mapfile -t expected_csv_files < <(jq -r '.[].file_name' csv_files_info.json)

# Check if CSV files exist in any sub-folder of data
data_dir="../data"
all_files_exist=true

for csv_file in "${expected_csv_files[@]}"; do
    found_file=$(find "$data_dir" -type f -name "$csv_file")
    if [ -z "$found_file" ]; then
        echo "Expected CSV file '$csv_file' not found in sub-folders of $data_dir"
        all_files_exist=false
    fi
    echo "Expected CSV file '$csv_file' found."
done

if [ "$all_files_exist" = true ]; then
    echo "All expected CSV files exist. System test passed!"
    exit 0  # Exit with success code
else
    echo "Not all expected CSV files found in sub-folders of $data_dir. System test failed!"
    exit 1  # Exit with failure code
fi
