from app.analyst import single
import pandas as pd
import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser(description='This script accepts a stock symbol and generates an Excel file containing basic information about the stock. The data is sourced from the Alpha Vantage API. You can obtain an API key from "https://www.alphavantage.co/support/#api-key". Please note that the free API has certain limitations: it is restricted to 5 calls per minute and 500 calls per day. If you need the script to run more frequently or more quickly, consider purchasing a premium plan.')
    parser.add_argument('-s', '--symbol', required=True, type=str, help='Stock symbol for the script.')
    return parser.parse_args()

# Loading the config file
def load_config() -> dict:
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script.
    parent_dir = os.path.dirname(script_dir)  # Get the parent directory of the current script.
    config_path = os.path.join(parent_dir, 'config.json')  # Join parent directory with the config file name.

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    else:
        raise FileNotFoundError(f'{config_path} not found')


def create_folder(dir_path: str):
    # Check if the directory already exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def main():
    # Get api key here https://site.financialmodelingprep.com/developer/docs
    # And put it in the config file
    config = load_config()
    # Check if KEY exsist and not empty in the config file
    if "KEY" not in config or not config["KEY"]:
        raise ValueError("Invalid config: 'KEY' not found or empty, you can get a key for free from https://www.alphavantage.co/support/ ")
    key = config['KEY']

    args = parse_args()
    # Create the directory to put the excel files in
    dir_path='../../excel'
    create_folder(dir_path=dir_path)

    analyst = single(symbol=args.symbol,key=key, dir_path=dir_path)
    df = analyst.basic_analysis()
    analyst.create_excel(df=df, name='analysis')
    print('done!')

if __name__ == '__main__':
    main()
