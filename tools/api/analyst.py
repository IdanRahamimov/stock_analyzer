from alpha_vantage_api import get_statement, get_daily_adjusted
import pandas as pd
import numpy as np
import json

class single():
    def __init__(self, symbol: str, key: str, dir_path: str):
        self.dir_path = dir_path
        self.symbol = symbol
        self.key = key

    def create_excel(self, df: pd.DataFrame, name: str = "no_name", quarterly: bool = False):
        df.to_excel(f'{self.dir_path}/{self.symbol}_{name}_{"quarterly" if quarterly else "annual"}.xlsx', index=True)

    def get_income_statement(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='INCOME_STATEMENT', key=self.key, quarterly=quarterly)
        return df

    def get_balance_sheet(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='BALANCE_SHEET', key=self.key, quarterly=quarterly)
        return df

    # Get estimated value of shares
    def get_discounted_value(self, quarterly: bool = False):
        balance_sheet = self.get_balance_sheet(quarterly=quarterly)
        income_statement = self.get_income_statement(quarterly=quarterly)
        
        df = calculate_discounted_value(balance_sheet=balance_sheet, income_statement=income_statement)
        return df

    def get_estimated_growth(self, quarterly: bool = False, days: int = 5*365+100):
        daily_adjusted = get_daily_adjusted(symbol=self.symbol, key=self.key, days=days)
        balance_sheet = self.get_balance_sheet(quarterly=quarterly)
        income_statement = self.get_income_statement(quarterly=quarterly)

        # Find If and When there was a stock split
        mask = daily_adjusted['8. split coefficient'] != '1.0'
        splits = daily_adjusted[mask]
        
        for date, row in splits.iterrows():
            split_coefficient = float(row['8. split coefficient'])  # convert to float, if it's not already
            
            # Find the rows in 'balance_sheet' where 'fiscalDateEnding' is before 'split_date'
            mask = balance_sheet['fiscalDateEnding'] < date
            
            # Multiply 'commonStockSharesOutstanding' by 'split_coefficient' for these rows
            balance_sheet.loc[mask, 'commonStockSharesOutstanding'] *= split_coefficient
        
        self.create_excel(df=balance_sheet,name='1')
        self.create_excel(df=income_statement,name='2')
        for i in range(len(balance_sheet)-2):
            pass


# Here we use a simple form of Discounted Cash Flow (DCF) model to get an estimated value of shares.
def calculate_discounted_value(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame):
    # I want the avrage income over 3 year.
    avrage_income = income_statement['netIncome'][:3].mean()
    shares = balance_sheet['commonStockSharesOutstanding'][0]
    equity = balance_sheet['totalShareholderEquity'][0]

    data = []
    # Loop over the discount rates 1% to 30%.
    for discount in np.arange(0.01, 0.31, 0.01):
        # Loop over the investments length 1 to 20 years.
        for year in range(1, 21):
            # Calculate value_per_share by present value of an ordinary annuity
            # PVA = C * [(1 - (1 + r)^-n) / r]
            discounted_income = avrage_income * (1 - (1 + discount)**-year)/discount
            value = equity + discounted_income
            value_per_share = value/shares
            
            # Append new data to the data list
            data.append([year, discount, value_per_share])

    # Create DataFrame from the data list
    df = pd.DataFrame(data, columns=['Years', 'discountRate', 'estimatedValuePerShare'])
    # Set the row index name
    df.set_index('Years', inplace=True)
    return df


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    KEY = config['KEY']
    a = single('AAPL', KEY)
    a.create_income_statement()