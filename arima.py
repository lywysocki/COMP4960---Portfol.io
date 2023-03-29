import pandas as pd
import numpy as np
from database import retrieve_stock_prices
import plotly.express as px
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs

# gets dataframe for a specific stock
df = retrieve_stock_prices("META", "03-03-2003")

df = df[['Date', 'Close']].copy()

print(df)

# uses Augmented Dicky Fuller test to see if stock series is stationary
dftest = adfuller(df.Close.dropna())
# the more negative the ADF stat, the stronger the rejection of the hypothesis
print(f"ADF Stat: {dftest[0]}")
# if p-value < .5 then we time series is stationary
# if p-value > .5 then order of differencing needs to be found (d !=0)
print(f"p-value: {dftest[1]}")
print(f"# of lags: {dftest[2]}")
print('Critical Values:')
for key, value in dftest[4].items():
    print('\t%s: %.3f' % (key, value))

# time series is stationary when p-value < 0.05 and adf < critical value
# when time series is stationary, d = 0
if (dftest[1] < 0.05 and dftest[0] < dftest[4].get('1%') and
        dftest[0] < dftest[4].get('5%') and dftest[0] < dftest[4].get('10%')):
    print(f"p-value: {dftest[1]}")
    d = 0
# if time series is not stationary, then d needs to be calculated
else:
    # differencing value (d)
    # an auto correlation function plot can find d value
    d = ndiffs(df.Close, test="adf")
print(d)


res = arma_order_select_ic(df.Close, ic=["aic"], trend="n")
print(res['aic_min_order'])

# fig, ax = plt.subplots(figsize=(12,5))
# plot_acf(df.Close.to_numpy(), lags=10, ax=ax)
# plot_pacf(df.Close.to_numpy(), lags=8, method='ywm')
# plt.show()
# plot_pacf(df.Close.to_numpy(), lags=8, method='ywm')
# plt.show()

# Outputs graph of time series
# fig = px.line(df, x='Date', y='Close')
# fig.update_xaxes(rangeslider_visible=True)
# fig.show()


# p = order of the Auto Regressive term
# the number of lags used as predictors


# print(df.iloc[0]['Close'])