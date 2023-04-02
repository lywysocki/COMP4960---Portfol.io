import pandas as pd
import numpy as np
from database import retrieve_stock_prices
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
from sklearn.metrics import mean_squared_error

# gets dataframe for a specific stock
df = retrieve_stock_prices("META", "03-03-2003")

df = df[['Date', 'Close']].copy()

# # uses Augmented Dicky Fuller test to see if stock series is stationary
# dftest = adfuller(df.Close.dropna())

# # the more negative the ADF stat, the stronger the rejection of the hypothesis
# print(f"ADF Stat: {dftest[0]}")
# # if p-value < .5 then we time series is stationary
# # if p-value > .5 then order of differencing needs to be found (d !=0)
# print(f"p-value: {dftest[1]}")
# print('Critical Values:')
# for key, value in dftest[4].items():
#     print('\t%s: %.3f' % (key, value))

def get_d_value(dataset):
    # uses Augmented Dicky Fuller test to see if stock series is stationary
    dftest = adfuller(dataset)
    # time series is stationary when p-value < 0.05 and adf < critical value
    # when time series is stationary, d = 0
    if (dftest[1] < 0.05 and dftest[0] < dftest[4].get('1%') and
            dftest[0] < dftest[4].get('5%') and dftest[0] < dftest[4].get('10%')):
        return 0
    # if time series is not stationary, then d needs to be calculated
    else:
        # differencing value (d)
        # an auto correlation function plot can find d value
        return ndiffs(dataset, test="adf")

def get_p_value(dataset):
    # use Akaike's Information Criterion for selecting predictors of regression
    aic_result = arma_order_select_ic(dataset, ic=["aic"], trend="n")
    # p = order of the Auto Regressive term
    # the number of lags used as predictors
    return aic_result['aic_min_order'][0]

def get_q_value(dataset):
    # use Akaike's Information Criterion for selecting predictors of regression
    aic_result = arma_order_select_ic(dataset, ic=["aic"], trend="n")
    # q = moving average
    # number of lagged forcast errors that should go into the model
    return aic_result['aic_min_order'][1]

print(f"d value: {get_d_value(df.Close)}")
print(f"p value: {get_p_value(df.Close)}")
print(f"q value: {get_q_value(df.Close)}")

# uses p, d, and q values to
# ar.L1, ar.L2, and ar.L3 are the lag variables
# model = ARIMA(df.Close, order=(p,d,q), enforce_stationarity=False, enforce_invertibility=False)
# fitted = model.fit()
# print(fitted.summary())

# graph's the test and train portions of the closing data
train_data, test_data = df.Close[0:int(len(df.Close)*0.7)], df.Close[int(len(df.Close)*0.7):]
# plt.figure(figsize=(10,6))
# plt.grid(True)
# plt.xlabel('Dates')
# plt.ylabel('Closing Prices')
# plt.plot(df.Close, 'green', label='Train data')
# plt.plot(test_data, 'blue', label='Test data')
# plt.legend()
# plt.show()

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

# forcast plot -- NEEDS WORK
# fc, se, conf = fitted.forecast(321, alpha=0.05)
# fc_series = df.Close(fc, index=test_data.index)
# lower_series = df.Close(conf[:, 0], index=test_data.index)
# upper_series = df.Close(conf[:, 1], index=test_data.index)
# # Plot
# plt.figure(figsize=(10,5), dpi=100)
# plt.plot(train_data, label='training data')
# plt.plot(test_data, color = 'blue', label='Actual Stock Price')
# plt.plot(fc_series, color = 'orange',label='Predicted Stock Price')
# plt.fill_between(lower_series.index, lower_series, upper_series,
#                  color='k', alpha=.10)
# plt.title('Stock Price Prediction')
# plt.xlabel('Time')
# plt.ylabel('Stock Price')
# plt.legend(loc='upper left', fontsize=8)
# plt.show()


# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)


# invert differenced value
def inverse_difference(history, y_hat, interval=1):
    return y_hat + history[-interval]

def forcast_one_step(dataset):
    # seasonal difference
    x = dataset.values
    days_in_year = 365
    differenced = difference(x, days_in_year)
    # fit model
    model = ARIMA(differenced, order=(get_p_value(differenced), get_d_value(differenced) , get_q_value(differenced)))
    model_fit = model.fit()
    # one-step forecast - forcast for the next time step in series
    forecast = model_fit.forecast()[0]
    # invert the differenced forecast to something usable
    forecast = inverse_difference(x, forecast, days_in_year)
    print(f"One-Step Forecast: {forecast}")

forcast_one_step(df.Close)