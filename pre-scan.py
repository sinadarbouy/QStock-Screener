import yfinance as yf
import pandas as pd

def calculate_price(ticker):
  stock = yf.Ticker(ticker["Symbol"])
  try:
    currentPrice = stock.info["currentPrice"]
    return currentPrice
  except:
    return 0

def pre_scan():
  
  # making dataframe  
  df = pd.read_csv("data/nasdaq_screener_1710370048684.csv")
  # Filtering based on Country column
  US_df = df[df['Country'] == 'United States']

  US_df = US_df[~US_df.iloc[:, 0].str.contains("\^")]
  print("pre scan start:",len(US_df))
  US_df['currentPrice'] =US_df.apply(calculate_price, axis=1)
  US_df.to_csv('data/pre_scan.csv', index=False)
  
  print("Pre-scan completed. Total entries after pre-scan:", len(US_df))

pre_scan()
