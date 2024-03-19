import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# def check_move_higher(symbol):
#     # Get historical data for the symbol
#     a1=pd.Timestamp.now() - pd.DateOffset(months=3)
#     b2=pd.Timestamp.now()
#     stock_data = yf.download(symbol, start=pd.Timestamp.now() - pd.DateOffset(months=3), end=pd.Timestamp.now())
    
#     # Calculate the percentage change over the past 3 months
#     a= stock_data['Close'].iloc[-1]
#     b=stock_data['Close'].iloc[0]
#     percentage_change = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
    
#     # Check if the percentage change is greater than 30%
#     if percentage_change > 30:
#         print(f"{symbol} has moved more than 30% higher in the past 3 months.")
#     else:
#         print(f"{symbol} hasn't moved more than 30% higher in the past 3 months.")

# # Example usage:
# check_move_higher('LYFT')  # Replace 'AAPL' with the symbol you want to check
stock = yf.Ticker("OCGN")
def calculate_average_volume(stock_symbol):
    # Fetch historical price data for the past 30 days
    # stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data=yf.download(stock_symbol, start=pd.Timestamp.now() - pd.DateOffset(days=30), end=pd.Timestamp.now())
    # Calculate average trading volume for the past 30 days
    avg_volume = stock_data['Volume'].mean()
    
    return avg_volume



# print(f"volume: ${msft.info['volume']}")
# print(f"averageVolume: ${msft.info['averageVolume']}")
# print(f"averageVolume10days: ${msft.info['averageVolume10days']}")
# print(f"regularMarketVolume: ${msft.info['regularMarketVolume']}")
# print(f"averageDailyVolume10Day: ${msft.info['averageDailyVolume10Day']}")
# print(f"marketCap: ${msft.info['marketCap']}")
