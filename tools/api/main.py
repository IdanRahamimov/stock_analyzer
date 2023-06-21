from analyst import single
import pandas as pd
import json
import os

# Loading the config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Get api key here https://site.financialmodelingprep.com/developer/docs
# And put it in the config file
KEY = config['KEY']

def create_folder(dir_path: str):
    # Check if the directory already exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def main():
    # Create the directory to put the excel files in
    dir_path='../../excel'
    create_folder(dir_path=dir_path)

    analyst = single(symbol='AAPL',key=KEY, dir_path=dir_path)
    analyst.create_income_statement()
    analyst.create_income_statement(quarterly=True)

if __name__ == '__main__':
    main()
