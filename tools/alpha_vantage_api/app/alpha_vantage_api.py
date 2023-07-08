from datetime import datetime, timedelta
import pandas as pd
import requests
import json
import time

# Get api key here https://site.financialmodelingprep.com/developer/docs
# And put it in the config file

def get_respone(url: str) -> dict:
    '''
        If you dont have premium you can only call the api 5 times a minute and 500 a day
        if we try to use it more we will get a {'Note': "..."} so if we get the note we 
        will wait a minute
    '''
    data = {}
    for i in range(3): # up to 3 min
        response = requests.get(url)
        data = response.json()
        if 'Note' in data.keys():
            time.sleep(60)
        else:
            return data
            break
        raise ValueError(f'Unable to received data from the server, {data}')

def clean_statment(data: dict, filter_: str) -> pd.DataFrame:
    if filter_ not in data:
        if 'fiscalDateEnding' not in data[filter_]:
            raise ValueError('missing data')
        
    df = pd.DataFrame(data[filter_])
    # Set fiscalDateEnding as the index
    df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
    df.set_index('fiscalDateEnding', inplace=True)
    # Change datatype
    for column in df.columns:
        if column != 'reportedCurrency':
            df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)

    return df

def get_statement(symbol: str, function: str, filter_: str, key: str) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={key}'
    data = get_respone(url)
    return clean_statment(data, filter_)


def clean_daily_adjusted(data: dict, time_range: datetime) -> pd.DataFrame:
    df = pd.DataFrame(data['Time Series (Daily)'])
    
    # Get date for x days ago from today
    df = df.transpose()
    df.index = pd.to_datetime(df.index)
    # change datatype
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)
    # Filter data to include only the last 5 years
    df = df[df.index >= time_range]
    return df

def get_daily_adjusted(symbol: str, key: str, days: int = 5*365+100) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={key}'
    data = get_respone(url)
    time_range = datetime.now() - timedelta(days=days)
    return clean_daily_adjusted(data, time_range)


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    key = config['KEY']
    df = get_statement('AAPL', function='EARNINGS', filter_='annualEarnings',key=key)
    print(df)