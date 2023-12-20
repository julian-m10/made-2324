import json
import os
import numpy as np
import pandas as pd
import sqlalchemy as sql
import zipfile

from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi


def check_file_exists(directory, file_substring):
    """
    :param directory: The directory in which the search is executed.
    :param file_substring: The file to check on. Can be a substring.
    :return: The file path if a file with the substring was found.
    """
    file_list_exists = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file_substring in file
    ]
    return file_list_exists


def download_files_from_kaggle(kaggle_api, dataset_name, author, file_name, directory):
    """
    :param kaggle_api: Kaggle API object.
    :param dataset_name: The dataset from which data shall be downloaded.
    :param author: The author of the searched dataset.
    :param file_name: The file which should be downloaded.
    :param directory: The target directory in which the downloaded data will be saved.
    """
    kaggle_api.dataset_download_file(dataset=f"{author}/{dataset_name}", file_name=file_name, path=directory)


def process_non_existing_file(kaggle_api, engine, data_directory, file_info):
    """
    :param kaggle_api: Kaggle API object.
    :param engine: SQLite database engine.
    :param data_directory: Directory in which data file should be located.
    :param file_info: Information about the file which is to be processed. Retrievable from the csv_files_info.json.
    """
    print(f"{file_info['file_name']} not found. Downloading from Kaggle...")
    download_files_from_kaggle(
        kaggle_api, file_info['dataset_name'], file_info['author'], file_info['file_name'],
        data_directory + '/' + file_info['dataset_name']
    )
    file_path = check_file_exists(data_directory, file_info['file_name']).pop()
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(data_directory + '/' + file_info['dataset_name'])
    existing_file = check_file_exists(data_directory, file_info['file_name'])
    process_existing_file(existing_file, engine, file_info)


def process_existing_file(existing_file, engine, file_info):
    """
    All files will at any point be treated in this function.
    :param existing_file: The path specifying where the file is located.
    :param engine: SQLite database engine.
    :param file_info: Information about the file which is to be processed. Retrievable from the csv_files_info.json.
    """
    file_path = [file for file in existing_file if file.lower().endswith('.csv')][0]
    print(f"Importing {file_info['file_name']} from file system")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            column_types = file_info['column_types']
            df = pd.read_csv(file)
            print(f"Clean the {file_info['file_name']} dataset...")
            tidy_df = clean_dataset(df, file_info)
            print(f"Creating table for {file_info['file_name']} in SQLite database...")
            create_sqlite_table(tidy_df, file_info['file_name'].replace('.csv', ''), engine)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")


def clean_dataset(df, file_info):
    """
    :param df: The dataframe which is to be cleaned.
    :param file_info: Information about the file which is to be processed. Retrievable from the csv_files_info.json.
    :return: The cleaned dataframe containing only the wanted data.
    """
    important_cols = file_info['important_columns']

    # Check if the column 'year' or 'date' exists
    # If yes, convert the column to datetime and filter out all data before 2013
    if 'year' in df.columns:
        df = df[df['year'] > 2012]
    if 'date' in df.columns:
        df = df[pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce').dt.year > 2012]

    # Replace empty strings with NaN
    df.replace('', np.nan, inplace=True)
    df.replace('nan', np.nan, inplace=True)
    df.replace('#', np.nan, inplace=True)

    # Drop all rows with NaN values
    cleaned_df = df[important_cols].dropna()
    cleaned_df = cleaned_df.astype(file_info['column_types'])

    return cleaned_df


def create_sqlite_table(df, table_name, engine):
    """
    :param df: The dataframe for which a table will be created in the SQLite database. Existing ones will be updated.
    :param table_name: Specifies the table_name in the SQLite database.
    :param engine: SQLite database engine.
    :return:
    """
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')


def main():
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()

    # Specify the data directory and the SQLite database engine.
    data_directory = '../data'
    engine = sql.create_engine('sqlite:///../data/data.sqlite')

    # Import the info about the csv-files that are needed from a json-file.
    with open('csv_files_info.json', 'r', encoding='utf-8', errors='replace') as file:
        csv_files_info = json.load(file)

    for file_info in csv_files_info:
        # Process every file specified in the csv_files_info.json.
        # If the data does not exist locally, it is downloaded from Kaggle first.
        existing_file = check_file_exists(data_directory, file_info['file_name'])
        if not existing_file:
            process_non_existing_file(kaggle_api, engine, data_directory, file_info)
        if existing_file:
            process_existing_file(existing_file, engine, file_info)


if __name__ == "__main__":
    main()
