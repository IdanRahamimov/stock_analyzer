from datetime import datetime, timedelta
import pandas as pd
import requests
import json

# Get api key here https://site.financialmodelingprep.com/developer/docs
# And put it in the config file

def get_statement(symbol: str, function: str, key: str, quarterly: bool = False):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={key}'
    response = requests.get(url)
    data = response.json()
    try:
        df = pd.DataFrame(data['quarterlyReports' if quarterly else 'annualReports'])

        # change datatype
        for column in df.columns:
            # If the current column is not the 'fiscalDateEnding' or 'reportedCurrency' column, convert it to float
            if column == 'fiscalDateEnding':
                df[column] = pd.to_datetime(df[column])
            elif column != 'reportedCurrency':
                df[column] = pd.to_numeric(df[column], errors='coerce')

        df.set_index('fiscalDateEnding', inplace=True)

        return df
    except Exception as e:
        print(data)
        print(e)

def get_daily_adjusted(symbol: str, key: str, days: int = 5*365+100):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={key}'
    response = requests.get(url)

    try:
        data = response.json()
        df = pd.DataFrame(data['Time Series (Daily)'])
        
        # Get date for x days ago from today
        df = df.transpose()
        df.index = pd.to_datetime(df.index)
        x_days = datetime.now() - timedelta(days=days)
        # change datatype
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        # Filter data to include only the last 5 years
        df = df[df.index >= x_days]
        
        return df
    except Exception as e:
        print(data)
        print(e)


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    KEY = config['KEY']
    df = get_news('AAPL', KEY)
    print(df)
    mask = df['8. split coefficient'] != '1.0'
    splits = df[mask]
    for date, row in splits.iterrows():
        print(f"Date: {date}, Split coefficient: {row['8. split coefficient']}")
    df.to_excel('1.xlsx', index=True)