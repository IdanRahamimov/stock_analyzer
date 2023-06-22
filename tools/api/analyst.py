from alpha_vantage_api import get_statement, get_daily_adjusted
import pandas as pd
import numpy as np
import json

class single():
    def __init__(self, symbol: str, key: str, dir_path: str):
        self.dir_path = dir_path
        self.symbol = symbol
        self.key = key

        self.statements_cache = {}

    def create_excel(self, df: pd.DataFrame, name: str = "no_name", quarterly: bool = False):
        df.to_excel(f'{self.dir_path}/{self.symbol}_{name}_{"quarterly" if quarterly else "annual"}.xlsx', index=True)

    def get_statement(self, function: str, quarterly: bool = False):
        """
        Retrieves the specified financial statement for the symbol. 
        Utilizes caching to prevent unnecessary API calls if the statement is unchanged.
        """
        cache_key = f"{function}_{'quarterly' if quarterly else 'annual'}"

        if cache_key not in self.statements_cache:
            self.statements_cache[cache_key] = get_statement(symbol=self.symbol, function=function, key=self.key, quarterly=quarterly)

        return self.statements_cache[cache_key]

    # Get estimated value of shares
    def get_discounted_value(self, quarterly: bool = False):
        balance_sheet = self.get_statement(function='BALANCE_SHEET', quarterly=quarterly)
        income_statement = self.get_statement(function='INCOME_STATEMENT', quarterly=quarterly)
        
        df = calculate_discounted_value(balance_sheet=balance_sheet, income_statement=income_statement)
        return df

        # TODO this \/
    def get_average_growth(self, quarterly: bool = False, days: int = 5*365+100):
        balance_sheet = self.get_statement(function='BALANCE_SHEET', quarterly=quarterly)
        income_statement = self.get_statement(function='INCOME_STATEMENT', quarterly=quarterly)
        
        balance_sheet = self.fix_shares_outstanding(balance_sheet=balance_sheet, days=days)
        results = []
        prev_ratio = None

        for i in range(4):
            avrage_income = income_statement['netIncome'][i]
            shares = balance_sheet['commonStockSharesOutstanding'][i]
            equity = balance_sheet['totalShareholderEquity'][i]
            ratio = (avrage_income + equity) / shares

            if prev_ratio is not None:
                results.append((ratio - prev_ratio) / prev_ratio)

            prev_ratio = ratio

        return sum(results) / len(results)

    def get_(self, quarterly: bool = False, days: int = 5*365+100):
        balance_sheet = self.get_statement(function='BALANCE_SHEET', quarterly=quarterly)

        equity = balance_sheet['totalShareholderEquity'][0]
        shares = balance_sheet['commonStockSharesOutstanding'][0]
        asset_per_share = total_assets / shares
        print(f'Asset per share for year {i + 1}: {asset_per_share}')

    # The balance_sheet does not take into accunt stock splits
    # Which can actually be good sometimes and other times not
    def fix_shares_outstanding(self, balance_sheet: pd.DataFrame, days: int = 5*365+100):
        daily_adjusted = get_daily_adjusted(symbol=self.symbol, key=self.key, days=days)
        # Find If and When there was a stock split
        mask = daily_adjusted['8. split coefficient'] != '1.0'
        splits = daily_adjusted[mask]
        
        for date, row in splits.iterrows():
            # Get the split coefficient from the current row in splits
            split_coefficient = row['8. split coefficient']
            # Find the rows in 'balance_sheet' where 'fiscalDateEnding' is before 'split_date'
            mask = balance_sheet.index < date
            # Multiply 'commonStockSharesOutstanding' by 'split_coefficient' for these rows
            balance_sheet.loc[mask, 'commonStockSharesOutstanding'] *= split_coefficient
        
        return balance_sheet

# Calculate value_per_share by present value of an ordinary annuity
# PVA = C * [(1 - (1 + r)^-n) / r]
def ordinary_annuity(x: float, divider: int, discount: float, b: float = 0, time_frame: int = 1 ):
    discounted_x = x * (1 - (1 + discount)**-time_frame)/discount
    value = discounted_x + b
    return value/divider

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
            value_per_share = ordinary_annuity(x=avrage_income,b=equity,divider=shares,time_frame=year,discount=discount)
            
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