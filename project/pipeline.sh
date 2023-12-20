#!/bin/bash

# Check if 'packages.json' exists
if [ ! -f "packages.json" ]; then
    echo "Error: 'packages.json' file not found."
    exit 1
fi

# Read 'packages.json' and install required packages
required_packages=$(python3 - << END
import json

with open('packages.json') as f:
    data = json.load(f)
    dependencies = data.get('dependencies', {})

    packages = []
    for package, version in dependencies.items():
        packages.append(f"{package}=={version}")

    print(" ".join(packages))
END
)

# Install or upgrade required packages
pip3 install --upgrade $required_packages


# IMPORTANT:
## Because the data pipeline is going to connect to kaggle, it is necessary that a kaggle API token is available on the
## local device under '~/.kaggle/kaggle.json'.
## For own data security, ensure that other users on your computer do not have access to those credentials.

# Run Python data_pipeline
python retrieve_data.py
