@echo off

REM IMPORTANT:
REM Because the data pipeline is going to connect to kaggle, it is necessary that a kaggle API token is available on the
REM local device under '~/.kaggle/kaggle.json'.
REM For own data security, ensure that other users on your computer do not have access to those credentials.

for /f %%i in ('python -c "import json; data = json.load(open('packages.json'));
    print(' '.join(data['dependencies'].keys()))"') do (
        pip install %%i
    )

python retrieve_data.py
