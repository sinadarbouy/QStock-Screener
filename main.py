import pandas as pd
from tabulate import tabulate
import threading
import subprocess

# Constants
SCAN_INTERVAL_SECONDS = 900  # 15 minutes
UPDATE_DISPLAY_INTERVAL_SECONDS = 1200  # 20 minutes
TOP_PERCENTAGE = 0.27
TOP_COUNT = 40
COLUMNS_TO_DISPLAY = ['Symbol', 'price_growth_one_month', 'avg_volume_10_days', 'volume_cal']

# Function to read and preprocess DataFrame
def read_and_preprocess_dataframe():
    dataframe = pd.read_csv("data/scan.csv")
    dataframe[['volume_dollars_1day', 'avg_volume_10_days', 'volume_cal']] = dataframe[
        ['volume_dollars_1day', 'avg_volume_10_days', 'volume_cal']
    ].apply(pd.to_numeric, errors='coerce')
    return dataframe

# Function to filter DataFrame
def filter_dataframe(dataframe):
    filtered_df = dataframe[dataframe['volume_dollars_1day'] > 20000]
    filtered_df = filtered_df[filtered_df['is_10_below_20_mv_10_days'] == 0]
    top_count = int(TOP_PERCENTAGE * len(filtered_df))
    return filtered_df.head(top_count)[:TOP_COUNT][COLUMNS_TO_DISPLAY]

# Function to display DataFrame
def display_dataframe(df):
    table = tabulate(df, headers='keys', tablefmt='fancy_grid')
    print(table)

# Function to update and display DataFrame
def update_and_display():
    df = filter_dataframe(read_and_preprocess_dataframe())
    display_dataframe(df)

# Function to run `scan.py` in the background every 15 minutes
def run_scan():
    threading.Timer(SCAN_INTERVAL_SECONDS, run_scan).start()
    subprocess.Popen(["/opt/homebrew/bin/python3", "scripts/scan.py", "170"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to schedule the update and display every 20 minutes
def schedule_update_and_display():
    threading.Timer(UPDATE_DISPLAY_INTERVAL_SECONDS, schedule_update_and_display).start()
    update_and_display()

# Start the background scan
run_scan()

# Start scheduling update and display
schedule_update_and_display()
