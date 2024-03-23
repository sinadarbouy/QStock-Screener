import yfinance as yf
import pandas as pd
import multiprocessing
import numpy as np
import sys

def calculate_adr_20(hist):
  sum = 0
  for i in range(0,20):
    sum = sum + hist['High'][i]/hist['Low'][i]

  adr_pct = 100 * (sum/20 - 1)
  return adr_pct

def calculate_average_volume(stock_symbol):
    # Fetch historical price data for the past 30 days
    # stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data=yf.download(stock_symbol, start=pd.Timestamp.now() - pd.DateOffset(days=30), end=pd.Timestamp.now())
    # Calculate average trading volume for the past 30 days
    avg_volume = stock_data['Volume'].mean()
    
    return avg_volume

def check_move_higher(symbol):
    # Get historical data for the symbol
    stock_data = yf.download(symbol, start=pd.Timestamp.now() - pd.DateOffset(months=3), end=pd.Timestamp.now())
    
    # Calculate the percentage change over the past 3 months
    percentage_change = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
    
    return percentage_change

def is_10_below_20(ticker):
  ticker['MA10'] = ticker['Close'].rolling(window=10).mean()
  ticker['MA20'] = ticker['Close'].rolling(window=20).mean()
  ticker['10_below_20'] = ticker['MA10'] < ticker['MA20']
  last_10 = ticker.tail(10)
  num_true = last_10['10_below_20'].sum()
  num_false = len(last_10) - num_true
  # Check if number of True is more than False
  if num_true > num_false:
      #10 days are below 20 days")
    return 1
  else:
    #10 days are not below 20 days
    return 0

def is_higher_low(ticker):
  ticker['higher_low'] = ticker['Low'].tail(5).diff() > 0
  last_10 = ticker.tail(5)
  num_true = last_10['higher_low'].sum()
  num_false = len(last_10) - num_true
  # Check if number of True is more than False
  if num_true > num_false:
    return 1
  else:
    return 0
  
def filter_stocks(ticker):
    try:
        stock = yf.Ticker(ticker["Symbol"])
        hist = stock.history(period="2mo")
        
        if hist.shape[0] <= 22:
            raise ValueError("Historical data not available for 22 days.")
        
        adr_pct_20_days = calculate_adr_20(hist.tail(20))
        if adr_pct_20_days <= 5:
            raise ValueError("ADR percentage for 20 days is too low.")

        volume_dollars_1day = hist['Close'][0] * hist['Volume'][0] / 100
        is_10_below_20_mv_10_days = is_10_below_20(hist)
        is_higher_low_5_days = is_higher_low(hist)
        avg_volume_10_days= stock.info['averageVolume10days']
        volume_cal= stock.info['volume']
        price_growth_one_month = hist['Close'][0] / min(hist['Low'][:-22])
        percentage_change_3months = check_move_higher(ticker["Symbol"])
    except Exception as e:
        print(f"Exception processing {ticker['Symbol']}: {e}")
        return pd.Series([None]*9, index=['Symbol','adr_pct_20_days', 'volume_dollars_1day', 'price_growth_one_month', 'move_higher_3_months_percent', 'avg_volume_10_days', 'volume_cal', 'is_10_below_20_mv_10_days', 'is_higher_low_5_days'])
    
    return pd.Series([ticker["Symbol"],adr_pct_20_days, volume_dollars_1day, price_growth_one_month, percentage_change_3months, avg_volume_10_days, volume_cal, is_10_below_20_mv_10_days, is_higher_low_5_days], 
                     index=['Symbol','adr_pct_20_days', 'volume_dollars_1day', 'price_growth_one_month', 'move_higher_3_months_percent', 'avg_volume_10_days', 'volume_cal', 'is_10_below_20_mv_10_days', 'is_higher_low_5_days'])

def scan(dataframe):
    print("after prescan:",len(dataframe))
    dataframe = dataframe[:100]
    num_cores = multiprocessing.cpu_count()
    chunks = np.array_split(dataframe, num_cores) 
    
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(apply_filter, chunks)
    result_df = pd.concat(results)
    result_df = result_df.dropna()  # Drop rows with NaN values
    result_df = result_df[result_df['move_higher_3_months_percent'] >= 30]
    sorted_df = result_df.sort_values(by='price_growth_one_month', ascending=False)
    sorted_df.to_csv('data/scan.csv', index=False)
    print("Scan completed.")

def apply_filter(chunk):
    return chunk.apply(filter_stocks, axis=1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scan.py <max_price>")
        sys.exit(1)

    try:
        max_price = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid price.")
        sys.exit(1)
    
    dataframe = pd.read_csv("data/pre_scan.csv")
    dataframe = dataframe[dataframe["currentPrice"] < max_price]
    dataframe = dataframe[dataframe["currentPrice"] != 0]

    scan(dataframe)
