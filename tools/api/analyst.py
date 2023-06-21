from alpha_vantage_api import get_statement
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