import pandas as pd

dataframe = pd.read_csv("currentPrice.csv")
print(len(dataframe))
dataframe = dataframe[dataframe["currentPrice"] < 170]
print(len(dataframe))
dataframe = dataframe[dataframe["currentPrice"] != 0]
print(len(dataframe))
