# Stock Journal

This repository houses a comprehensive account of my investment history, along with a suite of custom tools that aid in making informed investment decisions.

## Tools

### Alpha Vantage API Tool

One such tool is built using the Alpha Vantage API. This tool streamlines the process of gathering historical information about a stock, helping you save valuable time.

#### Using the Alpha Vantage API Tool

1. Obtain an API key from the Alpha Vantage website. You can do this by visiting their support page at https://www.alphavantage.co/support/.
2. Insert your obtained key into the config file located at `./tools/alpha_vantage_api/`.
3. Execute the `main.py` script with your desired stock symbol as an argument by running the following command:

    ```
    python main.py -s [stock symbol]
    ```

    Replace `[stock symbol]` with your specific stock symbol. For example, for Apple Inc., the stock symbol would be `AAPL`.

    This command generates an Excel file containing the historical data of your specified stock.

    The Excel file can be found in the newly created `excel` directory.

Here's a sample preview of the generated Excel file:

![excel img]([link-to-your-image](https://github.com/IdanRahamimov/stock_journal/blob/main/screenshots/apple_analysis.png))
