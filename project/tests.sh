#!/bin/bash

# Running the pipeline
echo "Running the pipeline..."
./pipeline.sh

# Run the system tests
echo "Running system tests..."
./tests/system_test.sh

# Run the unit tests
echo "Running unit tests..."
python ./tests/unit_test.py
