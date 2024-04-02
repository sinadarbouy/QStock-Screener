import yfinance as yf

def calculate_adr_20(hist):
    adr_pct = 100 * ((hist['High'] / hist['Low']).mean() - 1)
    return adr_pct

# Function to calculate stop loss
def calculate_stop_loss(symbol, atr_multiplier=1):
    # Get historical data for the symbol
    stock = yf.Ticker(symbol)
    historical_data = stock.history(period="2mo")
    adr_pct_20_days = calculate_adr_20(historical_data.tail(20))
    stop_loss_price = stock.info["currentPrice"] - (stock.info["currentPrice"] * adr_pct_20_days / 100)
    return stop_loss_price

# Example usage:
symbol = "VST"  # Replace with your desired stock symbol
stop_loss = calculate_stop_loss(symbol)
print(f"Sample stop-loss price: ${stop_loss:.2f}")
