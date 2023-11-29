import pandas as pd
import re
import sqlalchemy as sql
import urllib.request as req

from io import StringIO


def retrieve_csv_data(url):
    try:
        response = req.urlopen(url)
        if response.getcode() == 200:
            print('CSV fetched correctly.')
            return response.read().decode('utf-8')
    except Exception as e:
        print(f'CSV could not be reached: {e}')
        return None


def alter_csv_data(untidy_df):
    untidy_df.drop(columns='Status')

    def is_valid_verkehr(value):
        return value in ['FV', 'RV', 'nur DPN']

    def is_valid_coord(value):
        return -90 <= value <= 90

    def is_valid_ifopt(value):
        ifopt_pattern = r'^[A-Za-z]{2}:\d+:\d+(:\d+)?$'
        bool(re.match(ifopt_pattern, str(value)))

    valid_verkehr = untidy_df.Verkehr.apply(is_valid_verkehr)
    valid_laenge = untidy_df.Laenge.apply(is_valid_coord)
    valid_breite = untidy_df.Breite.apply(is_valid_coord)
    valid_ifopt = untidy_df.IFOPT.apply(is_valid_ifopt)

    valid_rows = valid_verkehr & valid_laenge & valid_breite & valid_ifopt
    tidy_df = untidy_df[valid_rows].dropna()
    return tidy_df


def create_sqlite_db(sql_data, db_name, table_name):
    try:
        engine = sql.create_engine(f'sqlite:///../data/{db_name}')
        data_types = {
            'Laenge': sql.Float,
            'Breite': sql.Float,
            'IFOPT': sql.Text
        }
        sql_data.to_sql(table_name, engine, index=False, dtype=data_types, if_exists='replace')
    except Exception as e:
        print(f'SQLite database could not be created: {e}')


# Fetching csv data from url
csv_url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'
csv_data = retrieve_csv_data(csv_url)

# Alter data in the database
df = pd.read_csv(StringIO(csv_data), sep=';', decimal=',')
altered_df = alter_csv_data(df)

# Write data to SQLite database
if csv_data:
    create_sqlite_db(sql_data=altered_df, db_name='trainstops.sqlite', table_name='trainstops')
else:
    print('No csv_data available, could not create database')
