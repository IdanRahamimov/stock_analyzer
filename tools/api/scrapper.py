import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_shares_outstanding(symbol: str):
    # make a request to the website
    r = requests.get(f'https://www.macrotrends.net/stocks/charts/{symbol}/apple/shares-outstanding')

    # create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(r.text, 'html.parser')

    # find the table on the webpage
    table = soup.find_all('table')[0] 

    # create a dataframe from the table
    df = pd.read_html(str(table))[0]

    # print the dataframe
    return (df)

if __name__ == '__main__':
    df = get_shares_outstanding('AAPL')
    print(df)
