import pandas as pd
import numpy as np
from database import retrieve_stock_prices
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs

# gets dataframe for a specific stock
df = retrieve_stock_prices("META", "03-03-2003")

df = df[['Date', 'Close']].copy()

# uses Augmented Dicky Fuller test to see if stock series is stationary
dftest = adfuller(df.Close.dropna())
# the more negative the ADF stat, the stronger the rejection of the hypothesis
print(f"ADF Stat: {dftest[0]}")
# if p-value < .5 then we time series is stationary
# if p-value > .5 then order of differencing needs to be found (d !=0)
print(f"p-value: {dftest[1]}")
print('Critical Values:')
for key, value in dftest[4].items():
    print('\t%s: %.3f' % (key, value))

# time series is stationary when p-value < 0.05 and adf < critical value
# when time series is stationary, d = 0
if (dftest[1] < 0.05 and dftest[0] < dftest[4].get('1%') and
        dftest[0] < dftest[4].get('5%') and dftest[0] < dftest[4].get('10%')):
    d = 0
# if time series is not stationary, then d needs to be calculated
else:
    # differencing value (d)
    # an auto correlation function plot can find d value
    d = ndiffs(df.Close, test="adf")

print("d value:", d)

# use Akaike's Information Criterion for selecting predictors of regression
aic_result = arma_order_select_ic(df.Close, ic=["aic"], trend="n")

# p = order of the Auto Regressive term
# the number of lags used as predictors
p = aic_result['aic_min_order'][0]
print("p value:", p)

# q = moving average
# number of lagged forcast errors that should go into the model
q = aic_result['aic_min_order'][1]
print("q value:", q)

# Outputs graph of time series
# fig = px.line(df, x='Date', y='Close')
# fig.update_xaxes(rangeslider_visible=True)
# fig.show()


# train_data, test_data = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]
# training_data = train_data['Close'].values
# test_data = test_data['Close'].values
# history = [x for x in training_data]
# model_predictions = []
# N_test_observations = len(test_data)

model = ARIMA(df.Close, order=(p,d,q))
fitted = model.fit()
print(fitted.summary())


train_data, test_data = df.Close[0:int(len(df.Close)*0.7)], df.Close[int(len(df.Close)*0.7):]
plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel('Dates')
plt.ylabel('Closing Prices')
plt.plot(df.Close, 'green', label='Train data')
plt.plot(test_data, 'blue', label='Test data')
plt.legend()
plt.show()

# model_autoARIMA = auto_arima(df.Close, start_p=0, start_q=0,
#                       test='adf',       # use adftest to find optimal 'd'
#                       max_p=p, max_q=q, # maximum p and q
#                       m=1,              # frequency of series
#                       d=None,           # let model determine 'd'
#                       seasonal=False,   # No Seasonality
#                       start_P=0,
#                       D=0,
#                       trace=True,
#                       error_action='ignore',
#                       suppress_warnings=True,
#                       stepwise=True)
# print(model_autoARIMA.summary())
# model_autoARIMA.plot_diagnostics(figsize=(15,8))
# plt.show()

# model = ARIMA(df.Close, order=(2,1,2))
# fitted = model.fit()
# print(fitted.summary())

# model_fit.plot_predict(dynamic=False)
# plt.show()
