from app.alpha_vantage_api import get_statement, get_daily_adjusted
import pandas as pd
import numpy as np
import xlsxwriter
import json
import re

class single():
    def __init__(self, symbol: str, key: str, dir_path: str):
        self.dir_path = dir_path
        self.symbol = symbol
        self.key = key

        self.statements_cache = {}

    def create_excel(self, df: pd.DataFrame, name: str = ""):
        # Create a writer object
        print(df)
        df.columns = [add_space(i) for i in df.columns]
        df.index = pd.to_datetime(df.index).date
        df = df.rename_axis('date')

        if name:
            file_path = f'{self.dir_path}/{self.symbol}_{name}.xlsx'
        else:
            file_path = f'{self.dir_path}/{self.symbol}.xlsx'
        
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

        # Write your DataFrame to an excel file
        # Note that we set the index to False, so that the index (row names) will not be written to the file
        df.to_excel(writer, sheet_name='Sheet1', index=True)

        # Get the xlsxwriter workbook and worksheet objects in order to set the column widths
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Iterate over the columns and set the width to the max length in each column
        for i, col in enumerate(df.columns):   
            # define column length as max of column name length and data length
            column_len = max(len(col), df[col].astype(str).map(len).max())
            # set the length of the column to the max length found
            worksheet.set_column(i+1, i+1, column_len+5)

        # Formating the date
        # Create a format for date columns
        date_format = workbook.add_format({'num_format': 'mm/dd/yy'})
        worksheet.set_column(0, 0, 10, date_format)
        # Adding filter
        worksheet.autofilter(0, 0, df.shape[0], len(df.columns))
        # Close the writer and save the excel file
        writer.close()

    def get_statement(self, function: str, filter_: str):
        """
        Retrieves the specified financial statement for the symbol. 
        Utilizes caching to prevent unnecessary API calls if the statement is unchanged.
        """
        cache_key = f"{function}_{filter_}"

        if cache_key not in self.statements_cache:
            self.statements_cache[cache_key] = get_statement(symbol=self.symbol, function=function, filter_=filter_, key=self.key)

        return self.statements_cache[cache_key]

    def average_growth(self, df, column_name):
        results = []
        prev_value = None

        for row in df.itertuples():
            value = getattr(row, column_name)
            if prev_value is not None:
                results.append((value - prev_value) / prev_value)
            prev_value = value

        return sum(results) / len(results) if results else None

    # The balance_sheet does not take into accunt stock splits
    # Which can actually be good sometimes and other times not
    def fix_shares_outstanding(self, balance_sheet: pd.DataFrame, days: int = 5*365+100):
        daily_adjusted = get_daily_adjusted(symbol=self.symbol, key=self.key, days=days)
        # Find If and When there was a stock split
        mask = daily_adjusted['8. split coefficient'] != '1.0'
        splits = daily_adjusted[mask]
        
        for date, row in splits.iterrows():
            # Get the split coefficient from the current row in splits
            split_coefficient = getattr(row, '8. split coefficient')
            if split_coefficient > 1:
                # Find the rows in 'balance_sheet' where 'fiscalDateEnding' is before 'split_date'
                mask = balance_sheet.index < date
                # Multiply 'commonStockSharesOutstanding' by 'split_coefficient' for these rows
                balance_sheet.loc[mask, 'commonStockSharesOutstanding'] *= split_coefficient
        
        return balance_sheet

    def basic_analysis(self):
        balance_sheet = self.get_statement(function='BALANCE_SHEET', filter_='annualReports')
        balance_sheet = self.fix_shares_outstanding(balance_sheet=balance_sheet)
        cash_flow = self.get_statement(function='CASH_FLOW', filter_='annualReports')
        annual_earnings = self.get_statement(function='EARNINGS', filter_='annualEarnings')

        # Selecting the data I'am interested in
        income = cash_flow['netIncome']
        retainedEarnings = balance_sheet['retainedEarnings']
        treasuryStock = balance_sheet['treasuryStock']
        commonStockSharesOutstanding = balance_sheet['commonStockSharesOutstanding']

        # Calculating dividend per share and book value
        dividend_per_share = cash_flow['dividendPayoutCommonStock']/balance_sheet['commonStockSharesOutstanding']
        book_value = balance_sheet['totalShareholderEquity']/balance_sheet['commonStockSharesOutstanding']
        # Giving those column names
        dividend_per_share = dividend_per_share.rename('dividendPerShare')
        book_value = book_value.rename('bookValue')

        # Concatenate them into a new DataFrame
        df = pd.concat([income, retainedEarnings, dividend_per_share, book_value, treasuryStock, 
                        commonStockSharesOutstanding], axis=1)

        df = df.join(annual_earnings, how='inner')


        return df

def add_space(text):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', text)
    return ' '.join([m.group(0) for match in matches for m in [match]])

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    KEY = config['KEY']
    a = single('AAPL', KEY)
    a.create_income_statement()