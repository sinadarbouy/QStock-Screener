import yfinance as yf
import mplfinance as mpf
import pandas as pd  
import pathlib
import talib as ta
import matplotlib.patches as mpatches

import yfinance as yf
import mplfinance as mpf
import pandas as pd  
import pathlib
import talib as ta
import matplotlib.patches as mpatches

import sys


def save_symbol_history_chart(symbol):
    title = f"{symbol}-{pd.Timestamp.now().date()}-{(pd.Timestamp.now() - pd.DateOffset(months=6)).date()}"
    ourpath = pathlib.Path("/Users/cna/personal/trade/plots") / f"{title}.png"
    msft = yf.Ticker(symbol)

    # get historical market data
    hist = msft.history(period="6mo",interval="1d")

    hist['RSI'] = ta.RSI(hist['Close'],timeperiod=14)
    hist['ATR'] = ta.ATR(hist['High'],hist['Low'],hist['Close'],timeperiod=14)

    style_with_mavcolors  = mpf.make_mpf_style(base_mpf_style='tradingview',mavcolors=['#1f77b4','#ff7f0e','#2ca02c'])
    apd = mpf.make_addplot(hist['RSI'],color='cyan',
                               type='scatter',panel=2)

    fig, axes = mpf.plot(hist,type='candle',mav=(10,20,50),volume=True,style=style_with_mavcolors,figsize=(18,10),addplot=apd,returnfig=True,title=title)
    # Configure chart legend and title
    ma_10 = mpatches.Patch(color='#1f77b4', label='10 Day Moving Average')
    ma_20 = mpatches.Patch(color='#ff7f0e', label='20 Day Moving Average')
    ma_50 = mpatches.Patch(color='#2ca02c', label='50 Day Moving Average')
    RSI_label = mpatches.Patch(color='cyan', label='RSI')

    axes[0].legend(handles=[ma_10, ma_20, ma_50,RSI_label], loc='upper left')
    
    
    # Save figure to file
    fig.savefig(ourpath)
    
    print('''Using the Qullamaggie breakout strategy, If you were to rank the setup from 1 to 7 (1 being bad, 7 being great), what number would you give it?where is entry?
          ''')
    print(f"volume: ${msft.info['volume']}")
    print(f"averageVolume: ${msft.info['averageVolume']}")
    print(f"averageVolume10days: ${msft.info['averageVolume10days']}")
    print(f"regularMarketVolume: ${msft.info['regularMarketVolume']}")
    print(f"averageDailyVolume10Day: ${msft.info['averageDailyVolume10Day']}")
    print(f"marketCap: ${msft.info['marketCap']}")



def main():
    # Check if there are arguments passed
    if len(sys.argv) < 2:
        print("Usage: python scan.py <symbol>")
        return

    # Retrieve the argument passed
    symbol = sys.argv[1]
    save_symbol_history_chart(symbol)

if __name__ == "__main__":
    main()
