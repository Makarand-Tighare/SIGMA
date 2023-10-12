# Imports
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# Set up yfinance to use pandas
yf.pdr_override()

# Data Retrieval
start_date = '2006-01-01'
end_date = '2016-12-31'

# List of index symbols
index_symbols = ['SPY', 'DJI', 'IXIC', 'RUT']  # Example indices: S&P 500, Dow Jones, Nasdaq, Russell 2000

# Initialize an empty DataFrame
index_data = pd.DataFrame()

# Fetch data for each index and add it to the DataFrame
for symbol in index_symbols:
    try:
        data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        index_data[symbol] = data['Adj Close']
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Create a list of the ticker symbols (as strings) in alphabetical order
index_tickers = ['SPY', 'DJI', 'IXIC', 'RUT']  # Example tickers for the indices

# Concatenate the index dataframes together to a single data frame called index_stocks
index_stocks = pd.concat([index_data], axis=1, keys=index_tickers)

# Set the column name levels
index_stocks.columns.names = ['Index Ticker', 'Stock Info']

# EDA
try:
    # Max Close price for each index
    max_close_price = index_stocks.max()
    print("\nMax Close price for each index:")
    print(max_close_price)

    # Create a new empty DataFrame called returns
    returns = index_stocks.pct_change()

    # Create a pairplot using seaborn
    sns.pairplot(returns[1:])
    plt.show()

    # Dates of best and worst single day returns
    worst_drop_dates = returns.idxmin()
    best_gain_dates = returns.idxmax()
    print("\nDates of worst drop:")
    print(worst_drop_dates)
    print("\nDates of best gain:")
    print(best_gain_dates)

    # Standard deviation of the returns
    returns_std = returns.std()
    print("\nStandard deviation of returns:")
    print(returns_std)

    # Create a distplot using seaborn of the returns for one of the indices
    returns_subset_IXIC = returns['IXIC']['Adj Close']  # Example: Using Nasdaq returns
    sns.histplot(returns_subset_IXIC, color='green', bins=100)
    plt.show()

    # ... (Continue with the rest of your analysis)

except Exception as e:
    print(f"Error during EDA: {e}")
