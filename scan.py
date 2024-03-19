import yfinance as yf
import pandas as pd

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
    # Check if the percentage change is greater than 30%
    if percentage_change > 30:
        print(f"{symbol} has moved more than 30% higher in the past 3 months.")
    else:
        print(f"{symbol} hasn't moved more than 30% higher in the past 3 months.")

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
  # Increment the row count and print it
  dataframe.row_count += 1
  print("Processing row:", dataframe.row_count)
  try:
    stock = yf.Ticker(ticker["Symbol"])

    hist = stock.history(period="2mo")

    if hist.shape[0] <= 22:
      return None, None, None, None, None, None, None, None

    adr_pct_20_days = calculate_adr_20(hist.tail(20))
    if adr_pct_20_days <= 1:
        return None, None, None, None, None, None, None, None

    volume_dollars_1day = hist['Close'][0] * hist['Volume'][0] / 100
    # if volume_dollars_1day <= 3000:
    #   return pd.Series([None, None, None, None, None])
    
    # 10 days below 20 days -> no trading
    is_10_below_20_mv_10_days = is_10_below_20(hist)
    is_higher_low_5_days = is_higher_low(hist)
    
    avg_volume_10_days= stock.info['averageVolume10days']
    volume_cal= stock.info['volume']
    # avg_volume_30_days = calculate_average_volume(ticker["Symbol"]) #averageVolume10days
    # if avg_volume_30_days > stock.info["volume"] * 1.5: # This could indicate lower liquidity and potentially weaker breakout if it were to happen.
    #     return pd.Series([None, None, None, None])

    price_growth_one_month = hist['Close'][0] / min(hist['Low'][:-22])
    
    percentage_change_3months = check_move_higher(ticker["Symbol"])
    
    return adr_pct_20_days, volume_dollars_1day, price_growth_one_month, percentage_change_3months, avg_volume_10_days, volume_cal, is_10_below_20_mv_10_days, is_higher_low_5_days
  except:
    return None, None, None, None, None, None, None, None
  
  
def scan(dataframe):
  print("after prescan:",len(dataframe))
  # Initialize row_count attribute
  dataframe.row_count = 0

  dataframe[['adr_pct_20_days', 'volume_dollars_1day', 'price_growth_one_month','move_higher_3_months_percent', 'avg_volume_10_days', 'volume_cal', 'is_10_below_20_mv_10_days', 'is_higher_low_5_days']] = dataframe.apply(lambda row: filter_stocks(row), axis=1, result_type='expand')

  # Drop rows where adr_pct_20_days is None
  dataframe = dataframe[dataframe['adr_pct_20_days'].notna()]
  dataframe = dataframe[dataframe['volume_dollars_1day'].notna()]
  dataframe = dataframe[dataframe['price_growth_one_month'].notna()]
  

  dataframe = dataframe[dataframe['move_higher_3_months_percent'] >= 30]

  # Sort the DataFrame based on 'price_growth_one_month' column in descending order
  sorted_df = dataframe.sort_values(by='price_growth_one_month', ascending=False)

  # Calculate the number of rows corresponding to the top 27% of the data
  top_27_percent = int(0.27 * len(sorted_df))

  sorted_df.to_csv('data/scan.csv', index=False)

dataframe = pd.read_csv("data/pre_scan.csv")
dataframe = dataframe[dataframe["currentPrice"] < 170]
dataframe = dataframe[dataframe["currentPrice"] != 0]
scan(dataframe)
# pre_scan()
