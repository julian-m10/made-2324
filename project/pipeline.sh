#!/bin/bash

# Read package names from dependencies in packages.json file
required_packages=$(jq -r '.dependencies | to_entries[] | "\(.key) \(.value)"' packages.json)

# Loop through each package and install the specified version, if not already installed
while read -r package version; do
    if ! python -c "import $package" &> /dev/null; then
        echo "Installing $package@$version..."
        pip install "$package==$version"
    else
        echo "$package@$version is already installed."
    fi
done <<< "$required_packages"

# IMPORTANT:
## Because the data pipeline is going to connect to kaggle, it is necessary that a kaggle API token is available on the
## local device under '~/.kaggle/kaggle.json'.
## For own data security, ensure that other users on your computer do not have access to those credentials.

# Run Python data_pipeline
python retrieve_data.py
