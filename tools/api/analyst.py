from alpha_vantage_api import get_statement

class single():
    def __init__(self, symbol: str, key: str):
        self.symbol = symbol
        self.key = key

    def create_income_statement(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='INCOME_STATEMENT', key=self.key, quarterly=quarterly)
        df.to_excel(f'{self.symbol}_income_statement_{"quarterly" if quarterly else "annual"}.xlsx', index=False)

    def create_balance_sheet(self, quarterly: bool = False):
        df = get_statement(symbol=self.symbol, function='BALANCE_SHEET', key=self.key, quarterly=quarterly)
        df.to_excel(f'{self.symbol}_balance_sheet_{"quarterly" if quarterly else "annual"}.xlsx', index=False)

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