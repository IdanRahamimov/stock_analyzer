from app.alpha_vantage_api import clean_daily_adjusted, clean_statment
from datetime import datetime, timedelta
import pandas as pd

def test_clean_daily_adjusted():
    mock_data = {
        'Time Series (Daily)': {
            '2002-08-26': {
                '1. open': '15.95', '2. high': '15.95', '3. low': '15.16', '4. close': '15.53',
                '5. adjusted close': '0.235677646378487', '6. volume': '3392300', 
                '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
            },
            '2002-08-23': {
                '1. open': '15.9', '2. high': '15.93', '3. low': '15.45', '4. close': '15.73',
                '5. adjusted close': '0.238712773827019', '6. volume': '2915100',
                '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
            },
            '2002-08-22': {
                '1. open': '16.2', '2. high': '16.25', '3. low': '15.66', '4. close': '15.97',
                '5. adjusted close': '0.242354926765257', '6. volume': '4612700',
                '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
            }
        }
    }
    days = 3
    fixed_date = datetime.strptime('2002-08-26', '%Y-%m-%d')  # set a fixed date
    time_range = fixed_date - timedelta(days=days)
    
    df = clean_daily_adjusted(mock_data, time_range)
    # Validate
    assert len(df) == 2  # check length of dataframe is 2
    assert isinstance(df.index, pd.DatetimeIndex)  # check index is a datetime index
    assert all(df.dtypes == float)  # check all columns are of float type

def test_clean_statment():
    mock_data = {'symbol': 'AAPL', 'annualReports': [{
                'fiscalDateEnding': '2022-09-30', 'reportedCurrency': 'USD', 'operatingCashflow': '122151000000',
                'paymentsForOperatingActivities': '4665000000', 'proceedsFromOperatingActivities': 'None',
                'changeInOperatingLiabilities': '15558000000', 'changeInOperatingAssets': '14358000000',
                'depreciationDepletionAndAmortization': '11104000000', 'capitalExpenditures': '10708000000',
                'changeInReceivables': '9343000000', 'changeInInventory': '-1484000000', 'profitLoss': '99803000000',
                'cashflowFromInvestment': '-22354000000', 'cashflowFromFinancing': '-110749000000',
                'proceedsFromRepaymentsOfShortTermDebt': '7910000000', 'paymentsForRepurchaseOfCommonStock': '89402000000',
                'paymentsForRepurchaseOfEquity': '89402000000', 'paymentsForRepurchaseOfPreferredStock': 'None',
                'dividendPayout': '14841000000', 'dividendPayoutCommonStock': '14841000000',
                'dividendPayoutPreferredStock': 'None', 'proceedsFromIssuanceOfCommonStock': 'None',
                'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet': '5465000000',
                'proceedsFromIssuanceOfPreferredStock': 'None', 'proceedsFromRepurchaseOfEquity': '-89402000000',
                'proceedsFromSaleOfTreasuryStock': 'None', 'changeInCashAndCashEquivalents': '-10952000000',
                'changeInExchangeRate': 'None', 'netIncome': '99803000000'
            },{
                'fiscalDateEnding': '2021-09-30','reportedCurrency': 'USD', 'operatingCashflow': '104038000000',
                'paymentsForOperatingActivities': '4087000000', 'proceedsFromOperatingActivities': 'None',
                'changeInOperatingLiabilities': '19801000000', 'changeInOperatingAssets': '24712000000',
                'depreciationDepletionAndAmortization': '11284000000', 'capitalExpenditures': '11085000000',
                'changeInReceivables': '14028000000', 'changeInInventory': '2642000000', 'profitLoss': '94680000000', 
                'cashflowFromInvestment': '-14545000000', 'cashflowFromFinancing': '-93353000000',
                'proceedsFromRepaymentsOfShortTermDebt': '2044000000', 'paymentsForRepurchaseOfCommonStock': '85971000000',
                'paymentsForRepurchaseOfEquity': '85971000000', 'paymentsForRepurchaseOfPreferredStock': 'None',
                'dividendPayout': '14467000000', 'dividendPayoutCommonStock': '14467000000',
                'dividendPayoutPreferredStock': 'None', 'proceedsFromIssuanceOfCommonStock': '1105000000',
                'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet': '20393000000', 
                'proceedsFromIssuanceOfPreferredStock': 'None', 'proceedsFromRepurchaseOfEquity': '-84866000000',
                'proceedsFromSaleOfTreasuryStock': 'None', 'changeInCashAndCashEquivalents': '-3860000000',
                'changeInExchangeRate': 'None', 'netIncome': '94680000000'
            }
        ]
    }

    df = clean_statment(mock_data, filter_='annualReports')
    # Validate
    assert len(df) == 2  # check length of dataframe is 2
    assert isinstance(df.index, pd.DatetimeIndex)  # check index is a datetime index

    if 'reportedCurrency' in df.columns:
        print(df.drop(columns='reportedCurrency').dtypes)
        assert all(df.drop(columns='reportedCurrency').dtypes == float)  # check all columns are of float type, excluding 'reportedCurrency'
    else:
        assert all(df.dtypes == float) # check all columns are of float type