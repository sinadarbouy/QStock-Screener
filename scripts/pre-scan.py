import yfinance as yf
import pandas as pd
import multiprocessing
import numpy as np

def calculate_price(ticker):
    stock = yf.Ticker(ticker["Symbol"])
    try:
        currentPrice = stock.info["currentPrice"]
        return currentPrice
    except:
        return 0

def calculate_prices_for_chunk(chunk):
    return chunk.apply(calculate_price, axis=1)

def pre_scan():
    # Making dataframe  
    df = pd.read_csv("data/nasdaq_screener_1710370048684.csv")
    
    # Filtering based on Country column
    US_df = df[df['Country'] == 'United States']
    
    # Remove rows with symbols containing "^"
    US_df = US_df[~US_df.iloc[:, 0].str.contains("\^")]
    
    print("Pre scan start:", len(US_df))
    
    # Split dataframe into chunks
    num_cores = multiprocessing.cpu_count()
    chunks = np.array_split(US_df, num_cores)
    
    # Create a multiprocessing Pool
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(calculate_prices_for_chunk, chunks)
    
    # Concatenate results
    US_df['currentPrice'] = pd.concat(results, ignore_index=True)
    
    # Save the result to CSV
    US_df.to_csv('data/pre_scan.csv', index=False)
    
    print("Pre-scan completed. Total entries after pre-scan:", len(US_df))

if __name__ == '__main__':
    pre_scan()
