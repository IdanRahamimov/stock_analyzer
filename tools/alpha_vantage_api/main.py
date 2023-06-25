from analyst import single
import pandas as pd
import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser(description='This script accepts a stock symbol and generates an Excel file containing basic information about the stock. The data is sourced from the Alpha Vantage API. You can obtain an API key from "https://www.alphavantage.co/support/#api-key". Please note that the free API has certain limitations: it is restricted to 5 calls per minute and 500 calls per day. If you need the script to run more frequently or more quickly, consider purchasing a premium plan.')
    parser.add_argument('-s', '--symbol', required=True, type=str, help='Stock symbol for the script.')
    return parser.parse_args()

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
    args = parse_args()
    # Create the directory to put the excel files in
    dir_path='../../excel'
    create_folder(dir_path=dir_path)

    analyst = single(symbol=args.symbol,key=KEY, dir_path=dir_path)
    df = analyst.basic_analysis()
    analyst.create_excel(df=df, name='analysis')
    print('done!')

if __name__ == '__main__':
    main()
