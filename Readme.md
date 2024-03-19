# QStock-Screener

### Pre-Scan

The `pre_scan` function reads a NASDAQ CSV file to identify stocks. It specifically targets stocks from the United States and calculates their prices. These prices are later used to filter stocks based on account size. As this script is primarily used for initial data preparation, it typically doesn't need to be run frequently.

To execute the script, simply run:

```bash
python pre-scan.py
