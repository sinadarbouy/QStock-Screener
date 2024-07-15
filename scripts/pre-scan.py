import yfinance as yf
import pandas as pd
import multiprocessing
import numpy as np

def calculate_price(ticker):
    try:
        stock = yf.Ticker(ticker["Symbol"])
        currentPrice = stock.info["currentPrice"]
        return currentPrice
    except:
        return 0

def calculate_prices_for_chunk(chunk):
    return chunk.apply(calculate_price, axis=1)

def pre_scan():
    # Making dataframe  
    df = pd.read_csv("data/nasdaq_screener_1720465611392.csv")

    print("Pre scan start:", len(df))
    
    # Split dataframe into chunks
    num_cores = multiprocessing.cpu_count()
    chunks = np.array_split(df, num_cores)
    
    # Create a multiprocessing Pool
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(calculate_prices_for_chunk, chunks)
    
    # Concatenate results
    df['currentPrice'] = pd.concat(results, ignore_index=True)
    
    # Save the result to CSV
    df.to_csv('data/pre_scan.csv', index=False)
    
    print("Pre-scan completed. Total entries after pre-scan:", len(df))

if __name__ == '__main__':
    pre_scan()
