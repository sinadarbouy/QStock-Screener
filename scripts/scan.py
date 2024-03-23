import yfinance as yf
import pandas as pd
import multiprocessing
import numpy as np
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def calculate_adr_20(hist):
    adr_pct = 100 * (hist['High'] / hist['Low']).mean() - 1
    return adr_pct

def calculate_average_volume(stock_symbol):
    stock_data = yf.Ticker(stock_symbol).history(period="30d")
    avg_volume = stock_data['Volume'].mean()
    return avg_volume

def check_move_higher(symbol):
    stock_data = yf.Ticker(symbol).history(period="3mo")
    percentage_change = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
    return percentage_change

def is_10_below_20(ticker):
    ticker['MA10'] = ticker['Close'].rolling(window=10).mean()
    ticker['MA20'] = ticker['Close'].rolling(window=20).mean()
    ticker['10_below_20'] = ticker['MA10'] < ticker['MA20']
    return int(ticker['10_below_20'].tail(10).sum() > 5)

def is_higher_low(ticker):
    ticker['higher_low'] = ticker['Low'].tail(5).diff() > 0
    return int(ticker['higher_low'].tail(5).sum() > 2)
  
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
      if logging.getLogger().isEnabledFor(logging.DEBUG):
        print(f"Exception processing {ticker['Symbol']}: {e}")
      return pd.Series([None]*9, index=['Symbol','adr_pct_20_days', 'volume_dollars_1day', 'price_growth_one_month', 'move_higher_3_months_percent', 'avg_volume_10_days', 'volume_cal', 'is_10_below_20_mv_10_days', 'is_higher_low_5_days'])
    
    return pd.Series([ticker["Symbol"],adr_pct_20_days, volume_dollars_1day, price_growth_one_month, percentage_change_3months, avg_volume_10_days, volume_cal, is_10_below_20_mv_10_days, is_higher_low_5_days], 
                     index=['Symbol','adr_pct_20_days', 'volume_dollars_1day', 'price_growth_one_month', 'move_higher_3_months_percent', 'avg_volume_10_days', 'volume_cal', 'is_10_below_20_mv_10_days', 'is_higher_low_5_days'])

def scan_chunk(chunk):
    return chunk.apply(filter_stocks, axis=1)

def scan(dataframe):
    num_cores = multiprocessing.cpu_count()
    chunks = np.array_split(dataframe, num_cores)
    
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(scan_chunk, chunks)
        
    result_df = pd.concat(results)
    result_df = result_df.dropna()
    result_df = result_df[result_df['move_higher_3_months_percent'] >= 30]
    sorted_df = result_df.sort_values(by='price_growth_one_month', ascending=False)
    sorted_df.to_csv('data/scan.csv', index=False)
    print("Scan completed.")

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
    dataframe = dataframe[(dataframe["currentPrice"] < max_price) & (dataframe["currentPrice"] != 0)]

    scan(dataframe)
