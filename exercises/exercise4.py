import pandas as pd
import zipfile

from sqlalchemy import create_engine, Integer, Float, String, Text
from urllib.request import urlretrieve


def convert_to_fahrenheit(temp_str):
    """
    Converts a temperature string from Celsius to Fahrenheit.
    :param temp_str: Temperature string in Celsius.
    :return: Temperature in Fahrenheit as float or None if failed.
    """
    try:
        temp_float = float(temp_str.replace(',', '.'))
        return temp_float * 9 / 5 + 32
    except ValueError:
        return None


def validate_geraet(geraet):
    """
    Validates the 'Geraet' column.
    :param geraet: 'Geraet' field as string.
    :return: Validated 'Geraet' field as integer or None if failed.
    """
    try:
        geraet = int(geraet)
        if geraet > 0:
            return geraet
        else:
            return None
    except ValueError:
        return None


def main():
    """
    Main function to process the data.

    Steps:
    1. Download the dataset.
    2. Extract the dataset.
    3. Read the data into a pandas DataFrame.
    4. Rename and select relevant columns.
    5. Apply the conversion and validation functions.
    6. Remove rows with invalid 'Geraet' values.
    7. Save the DataFrame to a SQLite database.
    """

    # Download the dataset
    file_path = 'mowesta-dataset.zip'
    urlretrieve('https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip', file_path)

    # Extract the dataset
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall()

    # Read the data into a pandas DataFrame
    data = []
    with open('data.csv', 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split(';')[:-1]
        for line in f:
            row = line.strip().split(';')
            row_dict = {header: value for header, value in zip(headers, row[:-1])}
            row_dict['...'] = row[-1].split(';')
            data.append(row_dict)

    df = pd.DataFrame(data)

    # Rename and select relevant columns
    df = df[["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C",
             "Geraet aktiv"]]
    df = df.rename(
        columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"})

    # Apply the conversion and validation functions
    df["Temperatur"] = df["Temperatur"].apply(convert_to_fahrenheit)
    df["Batterietemperatur"] = df["Batterietemperatur"].apply(convert_to_fahrenheit)
    df["Geraet"] = df["Geraet"].apply(validate_geraet)

    # Remove rows with invalid 'Geraet' values
    df = df.dropna(subset=["Geraet"])

    # Define the data types for the SQLite database
    dtype = {'Geraet': Integer, 'Hersteller': String, 'Model': String, 'Monat': Integer, 'Temperatur': Float,
             'Batterietemperatur': Float, 'Geraet aktiv': Text}

    # Save the DataFrame to a SQLite database
    engine = create_engine('sqlite:///temperatures.sqlite')
    df.to_sql('temperatures', engine, if_exists='replace', dtype=dtype, index=False)


if __name__ == '__main__':
    main()
