# QStock-Screener
This Python script scans stock data to filter out stocks based on various criteria. It utilizes Yahoo Finance API for fetching stock data and multiprocessing for efficient computation.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Pandas
- yfinance
- NumPy

You can install the required dependencies using pip:

```bash
pip install pandas yfinance numpy
```
## Pre-Scan

The `pre_scan` function reads a NASDAQ CSV file to identify stocks. It specifically targets stocks from the United States and calculates their prices. These prices are later used to filter stocks based on account size. As this script is primarily used for initial data preparation, it typically doesn't need to be run frequently.

To execute the script, simply run:

```bash
python pre-scan.py
```
After execution, the script will generate a new CSV file named pre_scan.csv in the data directory containing the processed data.

## Scan
```bash
python scan.py <max_price>
```
Replace <max_price> with the maximum price you want to filter the stocks by.


### Description
The script performs the following tasks:

Fetches historical stock data using Yahoo Finance API.
Calculates various indicators such as Average Daily Range (ADR), Average Volume, Price Growth, etc.
Filters out stocks based on predefined criteria.
Utilizes multiprocessing for parallel processing to improve performance.
### Input Data
Ensure you have a CSV file named pre_scan.csv in the data directory. This file should contain stock data with columns such as 'Symbol', 'currentPrice', etc.
### Output
The script generates a CSV file named scan.csv in the data directory, containing the filtered stocks based on the specified criteria.
