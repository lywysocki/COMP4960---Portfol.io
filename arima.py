import pandas as pd
import numpy as np
from database import retrieve_stock_prices
import plotly.express as px
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller

# gets dataframe for a specific stock
df = retrieve_stock_prices("META", "03-03-2023")

# df = df[['Year', 'Month', 'Day', 'Close']].copy()

# print (df)

result = adfuller(df.Close.dropna())
print(f"ADF Stat: {result[0]}")
print(f"p-value: {result[1]}")



# print(df.iloc[0]['Close'])
