# QStock-Screener
This Python script scans stock data to filter out stocks based on various criteria. It utilizes Yahoo Finance API for fetching stock data and multiprocessing for efficient computation.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Pandas
- yfinance
- NumPy
- tabulate

You can install the required dependencies using pip:

```bash
pip install pandas yfinance numpy
```
## Pre-Scan

The `pre_scan` function reads a NASDAQ CSV file to identify stocks. It specifically targets stocks from the United States and calculates their prices. These prices are later used to filter stocks based on account size. As this script is primarily used for initial data preparation, it typically doesn't need to be run frequently.

To execute the script, simply run:

```bash
python scripts/pre-scan.py
```
After execution, the script will generate a new CSV file named pre_scan.csv in the data directory containing the processed data.

## Scan
```bash
python scripts/scan.py <max_price>
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

## main.py 
This Python script is designed to perform a periodic scan of stock data, filtering it based on certain criteria, and displaying the results. The script utilizes pandas for data manipulation and tabulate for formatting the displayed data.

### Usage

1. Ensure that your stock data is stored in a CSV file named `scan.csv` within the `data` directory.

2. Modify the constants in the script (`SCAN_INTERVAL_SECONDS`, `UPDATE_DISPLAY_INTERVAL_SECONDS`, `TOP_PERCENTAGE`, `TOP_COUNT`, `COLUMNS_TO_DISPLAY`) as per your requirements.

3. Run the script:

    ```bash
    python main.py
    ```

### Background Processes:

- The script initiates a background scan every 15 minutes using threading to run `scan.py`.
- It schedules the update and display of the DataFrame every 20 minutes.

### Customization

- Adjust the constants in the script to customize the scanning interval, display interval, top percentage of stocks to be displayed, and columns to be shown.

