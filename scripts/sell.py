import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from tabulate import tabulate
import os



def calculate_adr_20(hist):
    adr_pct = 100 * ((hist['High'] / hist['Low']).mean() - 1)
    return adr_pct

# Function to calculate stop loss
def calculate_stop_loss(symbol,start_date, atr_multiplier=1):
    # Get historical data for the symbol
    stock = yf.Ticker(symbol)
    purchase_date = datetime.strptime(start_date, "%m/%d/%Y")
    # calculate one month before purchase date
    historical_data = stock.history(start=purchase_date - timedelta(days=30), end=purchase_date)
    adr_pct_20_days = calculate_adr_20(historical_data.tail(20))
    stop_loss_price = stock.info["currentPrice"] - (stock.info["currentPrice"] * adr_pct_20_days / 100)
    return stop_loss_price

def sell_strategy_day(symbol,start_date,quantity):
  purchase_date = datetime.strptime(start_date, "%m/%d/%Y")
  days_since_purchase = (datetime.today() - purchase_date).days
  if days_since_purchase >= 3 and days_since_purchase <= 5:
    return f"SELL {int(quantity/3)} to {int(quantity/2)} of the position and move stop loss to break even."
  return "HOLD"
    
def is_close_below_moving_average(stock_symbol, moving_average_period):
    # Fetch historical data for the stock
    stock = yf.Ticker(stock_symbol)
    historical_data = stock.history(period="max")
    
    # Calculate the moving average
    historical_data['Moving_Average'] = historical_data['Close'].rolling(window=moving_average_period).mean()
    
    last_date = historical_data.tail(1)

    if float(last_date['Close']) < float(last_date['Moving_Average']):
      return True  # Close below moving average
    return False
  
def is_price_below_stop_loss(stock_symbol, stop_loss_price):
    stock = yf.Ticker(stock_symbol)
    current_price = stock.info["currentPrice"]
    if current_price < stop_loss_price:
        return True
    return False

# Function to display DataFrame
def display_dataframe(df):
    table = tabulate(df, headers='keys', tablefmt='fancy_grid')
    os.system('clear')
    print(table)

# Read stock data from CSV
stock_data = pd.read_csv('holding.csv')
for index, row in stock_data.iterrows():
    stop_loss_price = calculate_stop_loss(row['symbol'], row['purchase_date'])
    stock_data.loc[index, "stop_loss"] = stop_loss_price
    stock_data.loc[index, "below_stop_loss"] = is_price_below_stop_loss(row['symbol'], stop_loss_price)
    stock_data.loc[index, "below_mv_10"] = is_close_below_moving_average(row['symbol'], 10)
    stock_data.loc[index, "below_mv_20"] = is_close_below_moving_average(row['symbol'], 20)
    decision = sell_strategy_day(row['symbol'], row['purchase_date'], row['quantity'])
    if stock_data.loc[index, "below_stop_loss"] or stock_data.loc[index, "below_mv_10"] or stock_data.loc[index, "below_mv_20"]:
        decision = "SELL ALL"
    stock_data.loc[index, "Decision"] = decision

display_dataframe(stock_data)

