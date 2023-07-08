from app.main import single
import pandas as pd

def test_create_excel(tmp_path):
    mock_data = [
        {
            'date': '2002-08-26', '1. open': '15.95', '2. high': '15.95', '3. low': '15.16', '4. close': '15.53',
            '5. adjusted close': '0.235677646378487', '6. volume': '3392300', 
            '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
        },
        {
            'date': '2002-08-23', '1. open': '15.9', '2. high': '15.93', '3. low': '15.45', '4. close': '15.73',
            '5. adjusted close': '0.238712773827019', '6. volume': '2915100',
            '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
        },
        {
            'date': '2002-08-22', '1. open': '16.2', '2. high': '16.25', '3. low': '15.66', '4. close': '15.97',
            '5. adjusted close': '0.242354926765257', '6. volume': '4612700',
            '7. dividend amount': '0.0000', '8. split coefficient': '1.0'
        }
    ]
    # Convert to DataFrame
    mock_df = pd.DataFrame(mock_data)
    # Set 'date' column as index
    mock_df.set_index('date', inplace=True)

    # tmp_path is a pytest fixture providing a temporary directory unique to the test invocation
    # It behaves like the pathlib.Path object
    analyst = single(symbol='AAPL',key='', dir_path=tmp_path)
    
    analyst.create_excel(mock_df, name="test")
    
    created_file_path = tmp_path / "AAPL_test.xlsx"
    assert created_file_path.exists(), "Excel file does not exist."