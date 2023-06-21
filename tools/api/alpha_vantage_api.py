import requests
import pandas as pd

# Get api key here https://site.financialmodelingprep.com/developer/docs
# And put it in the config file

def get_statement(symbol: str, function: str, key: str, quarterly: bool = False):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['quarterlyReports' if quarterly else 'annualReports'])
    return df

if __name__ == '__main__':
    df = get_statement('AAPL', 'INCOME_STATEMENT')
    print(df)
    df.to_excel('1.xlsx', index=False)