#!/bin/bash

echo "Files found in 'data' directory:"
ls -l data

expected_files=$(cat data/csv_files_info.json | jq -r '.file_names[]')

for file in $expected_files
do
    if [ ! -f "data/$file.csv" ]; then
        echo "Error: $file.csv not found"
        exit 1
    fi
done

echo "System Test Passed: All expected CSV files present"
