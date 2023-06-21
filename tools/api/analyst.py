from alpha_vantage_api import get_statement
import pandas as pd
import numpy as np
import json

class single():
    def __init__(self, symbol: str, key: str, dir_path: str):
        self.dir_path = dir_path
        self.symbol = symbol
        self.key = key

    def create_income_statement(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='INCOME_STATEMENT', key=self.key, quarterly=quarterly)
        df.to_excel(f'{self.dir_path}/{self.symbol}_income_statement_{"quarterly" if quarterly else "annual"}.xlsx', index=False)

    def create_balance_sheet(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='BALANCE_SHEET', key=self.key, quarterly=quarterly)
        df.to_excel(f'{self.dir_path}/{self.symbol}_balance_sheet_{"quarterly" if quarterly else "annual"}.xlsx', index=False)

    def get_income_statement(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='INCOME_STATEMENT', key=self.key, quarterly=quarterly)
        return df

    def get_balance_sheet(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='BALANCE_SHEET', key=self.key, quarterly=quarterly)
        return df

    # Here we use a simple form of Discounted Cash Flow (DCF) model to get an
    # estimated value of shares 
    def create_discounted_value(self, quarterly: bool = False):
        balance_sheet = get_statement(symbol=self.symbol, function='BALANCE_SHEET', key=self.key, quarterly=quarterly)
        income_statement = get_statement(symbol=self.symbol, function='INCOME_STATEMENT', key=self.key, quarterly=quarterly)
        
        shares = float(balance_sheet['commonStockSharesOutstanding'][0])
        equity = float(balance_sheet['totalShareholderEquity'][0])

        # I want the avrage income over 3 year
        df_income = income_statement['netIncome']
        avrage_income = sum(float(df_income[i]) for i in range(3)) / 3

        df = pd.DataFrame()

        # loop over the discount rates 1% to 30% 
        for discount in np.arange(0.01, 0.31, 0.01):
            # Create a column with the discount rate
            #df[discount] = np.nan

            # loop over the investments length 1 to 20 years
            for year in range(1, 21):
                discounted_income = avrage_income * (1 - (1 + discount)**-year)/discount
                value = equity + discounted_income
                value_per_share = value/shares
                
                # Assign the value_per_share to the corresponding row and column in the DataFrame
                df.at[year, 'discount\n rate '+str(int(discount*100))+'%'] = value_per_share
        
        # Set the row index name
        df.index.name = 'Years'        
        df.to_excel(f'{self.dir_path}/{self.symbol}_discounted_value_{"quarterly" if quarterly else "annual"}.xlsx', index=True)
        
class multiple():
    def __init__(self, symbols: list, key: str):
        self.symbols = symbols
        self.key = key

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    KEY = config['KEY']
    a = single('AAPL', KEY)
    a.create_income_statement()