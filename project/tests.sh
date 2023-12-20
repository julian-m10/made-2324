#!/bin/bash

# Running the pipeline
echo "Running the pipeline..."
bash ./pipeline.sh

# Check the return value of pipeline.sh
if [ $? -ne 0 ]; then
    echo "Error: pipeline.sh failed."
    exit 1
fi

# Run the system tests
echo "Running system tests..."
bash ./system_test.sh

# Check the return value of system_test.sh
if [ $? -ne 0 ]; then
    echo "Error: system_test.sh failed."
    exit 1
fi

# Run the unit tests
echo "Running unit tests..."
python ./unit_tests.py
