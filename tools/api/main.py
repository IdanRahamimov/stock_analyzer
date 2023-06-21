from analyst import single
import pandas as pd
import json

with open('config.json', 'r') as f:
    config = json.load(f)

KEY = config['KEY']

def main():
    analyst = single(symbol='AAPL',key=KEY)
    analyst.create_income_statement()
    analyst.create_income_statement(quarterly=True)

if __name__ == '__main__':
    main()
