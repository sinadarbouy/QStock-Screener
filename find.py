import pandas as pd
dataframe.cs
dataframe['volume_dollars_1day'] = pd.to_numeric(dataframe['volume_dollars_1day'], errors='coerce')
df = dataframe[dataframe['volume_dollars_1day'] > 20000]
# Select the top 27% of the data
top_27_percent_df = sorted_df.head(top_27_percent)
top_27_percent_df.to_csv('top_27_percent_df.csv', index=False)
print(top_27_percent_df)
