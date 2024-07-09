import pandas as pd
from tabulate import tabulate
import threading
import subprocess
import os
from config.config import Config

# Constants
SCAN_INTERVAL_SECONDS = 120  # 15 minutes
UPDATE_DISPLAY_INTERVAL_SECONDS = 360  # 20 minutes
TOP_PERCENTAGE = 0.27
COLUMNS_TO_DISPLAY = ['Symbol', 'price_growth_one_month', 'avg_volume_10_days', 'volume_cal']

# Function to read and preprocess DataFrame
def read_and_preprocess_dataframe():
    dataframe = pd.read_csv("data/scan.csv")
    dataframe[['volume_dollars_1day', 'avg_volume_10_days', 'volume_cal']] = dataframe[
        ['volume_dollars_1day', 'avg_volume_10_days', 'volume_cal']
    ].apply(pd.to_numeric, errors='coerce')
    return dataframe

# Function to filter DataFrame
def filter_dataframe(dataframe,volume_dollars_1day):
    filtered_df = dataframe[dataframe['volume_dollars_1day'] > volume_dollars_1day]
    # filtered_df = filtered_df[filtered_df['is_10_below_20_mv_10_days'] == 0]
    # filtered_df = filtered_df[filtered_df['is_higher_low_5_days'] == 1]
    top_count = int(TOP_PERCENTAGE * len(filtered_df))
    if top_count == 0 :
        return filtered_df[:][COLUMNS_TO_DISPLAY]
    else:
        return filtered_df[:top_count][COLUMNS_TO_DISPLAY]

# Function to display DataFrame
def display_dataframe(df):
    table = tabulate(df, headers='keys', tablefmt='fancy_grid')
    os.system('clear')
    print(table)

# Function to update and display DataFrame
def update_and_display(volume_dollars_1day):
    df = filter_dataframe(read_and_preprocess_dataframe(),volume_dollars_1day)
    display_dataframe(df)

# Function to run `scan.py` in the background every 15 minutes
def run_scan(max_price):
    threading.Timer(SCAN_INTERVAL_SECONDS, run_scan,max_price).start()
    subprocess.Popen(["python3", "scripts/scan.py", f"${max_price}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to schedule the update and display every 20 minutes
def schedule_update_and_display(volume_dollars_1day):
    threading.Timer(UPDATE_DISPLAY_INTERVAL_SECONDS, schedule_update_and_display).start()
    update_and_display(volume_dollars_1day)

def main():
    config = Config()
    max_price = config.get_setting("MAX_PRICE")
    volume_dollars_1day = config.get_setting("VOLUME_DOLLARS_1DAY")
    # Start the background scan
    run_scan(max_price)
    # Start scheduling update and display
    schedule_update_and_display(volume_dollars_1day)

if __name__ == "__main__":
    main()
