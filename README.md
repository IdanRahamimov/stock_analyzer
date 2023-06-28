# Stock Journal

Welcome to Stock Journal - a unique blend of my personal investment history documentation and custom toolkits designed to assist in making well-informed investment decisions.

## Alpha Vantage API Tool

The Alpha Vantage API allow us to simplifies the process of fetching historical data for any given stock, aiding in time-efficient decision-making. Here's an illustrative representation of the Excel file the tool generates:

![Excel Image](https://github.com/IdanRahamimov/stock_journal/blob/main/screenshots/apple_analysis.png)

## How to Use Alpha Vantage API Tool

### Setup

1. Install the necessary libraries from the `requirements.txt` file with the following command:
    ```
    pip install -r ./tools/alpha_vantage_api/requirements.txt
    ```
    
2. Obtain Free API key from the Alpha Vantage website: `https://www.alphavantage.co/support/`.
   note: the free key is limited to 5 api calls a minute and 500 a day

3. Once you have your key, update the config file located at ./tools/alpha_vantage_api/.

#### Executetion 

Execute the `run.py` script with your desired stock symbol as an argument by running the following command:

    python ./tools/alpha_vantage_api/run.py -s [stock symbol]

Replace [stock symbol] with the specific symbol of the stock you're interested in. For example, for Apple Inc., the stock symbol is AAPL.

Executing this command will generate an Excel file containing historical data for the specified stock, which you can find in the excel directory created upon execution.
   
#### Testing
To test the code I used pytest.
Install pytest using:

    pip install pytest
    
And run the test suite with:

    python -m pytest .\tools\alpha_vantage_api\tests\

    
This project is an ongoing effort. Your feedback and contributions are greatly appreciated.
