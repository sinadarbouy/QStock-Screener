import pandas as pd
from tabulate import tabulate
import sched
import time
import threading
import subprocess


def update_dataframe():
  dataframe = pd.read_csv("data/scan.csv")
  dataframe['volume_dollars_1day'] = pd.to_numeric(dataframe['volume_dollars_1day'], errors='coerce')
  dataframe['avg_volume_10_days'] = pd.to_numeric(dataframe['avg_volume_10_days'], errors='coerce')
  dataframe['volume_cal'] = pd.to_numeric(dataframe['volume_cal'], errors='coerce')
  dataframe_volume_dollars_1day_20000 = dataframe[dataframe['volume_dollars_1day'] > 20000]
  dataframe_volume_dollars_1day_20000_is_10_below_20_mv_10_days_0 = dataframe_volume_dollars_1day_20000[dataframe_volume_dollars_1day_20000['is_10_below_20_mv_10_days'] ==0]
  top_27_percent = int(0.27 * len(dataframe_volume_dollars_1day_20000_is_10_below_20_mv_10_days_0))
  finaldataframe = dataframe_volume_dollars_1day_20000_is_10_below_20_mv_10_days_0.head(top_27_percent)
  return finaldataframe[:40]

# Function to display DataFrame in a beautiful way
def display_dataframe(df):
    table = tabulate(df, headers='keys', tablefmt='fancy_grid')
    print(table)

# Function to update the dataframe and display it
def update_and_display():
    df = update_dataframe()
    display_dataframe(df)
    
# Function to run `scan.py` in the background every 15 minutes
def run_scan():
    threading.Timer(900, run_scan).start()
    subprocess.Popen(["/opt/homebrew/bin/python3", "scan.py", "170" ],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 
# Function to schedule the update and display every 20 minutes
def schedule_update_and_display():
    threading.Timer(1200, schedule_update_and_display).start()
    update_and_display()

# Start the background scan
run_scan()

# Start scheduling update and display
schedule_update_and_display()
