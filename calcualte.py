import yfinance as yf
import numpy as np

def calculate_adr_20(hist):
  sum = 0
  for i in range(0,20):
    sum = sum + hist['High'][i]/hist['Low'][i]

  adr_pct = 100 * (sum/20 - 1)
  return adr_pct

  
# Example of using the formula for a specific stock (AAPL in this case)
stock = yf.Ticker('VKTX')
hist = stock.history(period='20d')

if len(hist) >= 20:
    adr_pct_20_days = calculate_adr_pct(hist)
    expression_value = calculate_expression(hist.tail(20))
    average_daily_range_percentage = calculate_average_daily_range(hist.tail(20))

    print("ADR % 20 days:", adr_pct_20_days)
    print("average_daily_range_percentage:", average_daily_range_percentage)
else:
    print("Insufficient data to calculate ADR % 20 days.")
