<div style="text-align: center;">

# London Urban Demographic Analysis

[![Licence](https://img.shields.io/badge/Licence-MIT-orange)](https://opensource.org/license/mit/)
[![Continuous Integration](https://github.com/julian-m10/made-2324/actions/workflows/project-tests.yml/badge.svg)](https://github.com/julian-m10/made-2324/actions/workflows/project-tests.yml)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

</div>

## Overview
This project aims to analyze the demographic subdivisions of the city of London and explore their correlation with the 
general quality of life. By investigating various demographic factors such as age, income, housing, health indicators, 
education, transportation, and political aspects, deriving insights into how these factors contribute to the 
overall well-being of different urban areas is the main goal of this project.

## Motivation
The motivation behind this project lies in the increasing awareness of the impact of demographic factors on individuals' 
quality of life. As discussions about health, both physical and mental, have gained prominence, understanding how 
demographic strata influence the overall well-being becomes crucial. This project utilizes sample data from the City of 
London spanning the years 2014 to 2016 to draw correlations between demographic aspects and quality of life indicators.

## Final Report
The final report can be found [here](./project/report.pdf). It includes a detailed description of the project, aiming to 
provide valuable insights into the relationships between demographic characteristics and the well-being of different 
urban areas in London.

## Usage
1. Ensure 'packages.json' is present.
2. Execute `pipeline.sh` to install dependencies and run the data pipeline.

**Note:** A Kaggle API token must be available locally in order to connect to the remote datasets
``(~/.kaggle/kaggle.json)``.

## Project Structure

- **`.github/`**: Directory to store GitHub Actions workflows.
    - `workflows/`: Directory to store GitHub Actions workflows.
        - `project-tests.yml`: GitHub Actions workflow for project tests.
- **`data/`**: Directory to store the project data.
    - `data.sqlite`: SQLite database storing the cleaned and processed data.
    - `plots/`: Directory to store generated plots and figures.

- **`project/`**: Directory to store project files.
    - `analyse_data.py`: Python script for data analysis and plotting.
    - `csv_files_info.json`: Information about CSV files needed for analysis.
    - `packages.json`: File specifying Python package dependencies.
    - `pipeline.sh`: Shell script for pipeline orchestration.
    - `report.pdf`: Final report with analysis results.
    - `retrieve_data.py`: Python script for data retrieval, cleaning, and database population.
    - `system_tests.sh`: Shell script for system tests.
    - `tests.sh`: Shell script executing unit and system tests.
    - `unit_tests.py`: Python script for unit tests.

- **`README.md`**: Project overview, context, and instructions.

## Data Pipeline
The data pipeline consists of two main components: [`pipeline.sh`](./project/pipeline.sh) and 
[`retrieve_data.py`](./project/retrieve_data.py).

### `pipeline.sh`
This shell script installs necessary Python packages based on the specifications in `packages.json` and then executes 
the Python data retrieval script.

### `retrieve_data.py`
The Python script connects to Kaggle for data retrieval, checks file existence, downloads missing files, and processes 
existing files. It includes functions for cleaning the dataset and creating/updating SQLite database tables.