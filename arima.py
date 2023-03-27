import pandas as pd
import numpy as np
import plotly.express as px

#download stock price data from github repository
df = pd.read_csv("https://github.com/lywysocki/COMP4960---Portfol.io/blob/c503849912586b67eac84e1c580be5deb19dc57e/1%20Year%20Historical%20Financials/AAPL_Financials.csv")
df.head()

#convert dataset into time series
df.index = pd.to_datetime(df["Date"])
df.head()
df.index
y = np.log(df["Close Price"])
y.plot()