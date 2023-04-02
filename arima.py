import pandas as pd
import numpy as np
from database import retrieve_stock_prices
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
from sklearn.metrics import mean_squared_error
# import warnings
# warnings.filterwarnings("ignore")

# gets dataframe for a specific stock
def get_data(ticker, date):
    df = retrieve_stock_prices(ticker, date)

    return df[['Date', 'Close']].copy()

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
    train_data, test_data = dataset[0:int(len(dataset) * 0.7)], dataset[int(len(dataset) * 0.7):]
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


df = get_data("SCHW", "03-03-2003")
# forcast_one_step(df.Close)


from statsmodels.tsa.stattools import acf

# Create Training and Test
train, test = df.Close[0:int(len(df.Close)*0.7)], df.Close[int(len(df.Close)*0.7):]
# Build Model
# model = ARIMA(train, order=(3,2,1))
model = ARIMA(train, order=(get_p_value(df.Close), get_d_value(df.Close), get_q_value(df.Close)))
fitted = model.fit()

# Forecast
fc, se, conf = fitted.forecast(get_p_value(df.Close), alpha=0.05)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc, index=test.index)
lower_series = pd.Series(conf[:, 0], index=test.index)
upper_series = pd.Series(conf[:, 1], index=test.index)

# Plot
plt.figure(figsize=(12,5), dpi=100)
plt.plot(train, label='training')
plt.plot(test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series,
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()




# train_data, test_data = df.Close[0:int(len(df.Close)*0.7)], df.Close[int(len(df.Close)*0.7):]
#
# model = ARIMA(train_data, order=(get_p_value(df.Close), get_d_value(df.Close), get_q_value(df.Close)))
# fitted = model.fit()
# fitted.plot_predict(dynamic=False)
# plt.show()
# # Forecast
# forcast, se, conf_int = fitted.forecast(10, alpha=0.05)  # 95% conf
#
# # Make as pandas series
# forcast_series = pd.Series(forcast, index=test_data.index)
# lower_bound = pd.Series(conf_int[:, 0], index=test_data.index)
# upper_bound = pd.Series(conf_int[:, 1], index=test_data.index)
#
# # Plot
# plt.figure(figsize=(10,7), dpi=100)
# plt.plot(train_data, label='training')
# plt.plot(test_data, 'g:', label='actual')
# plt.plot(forcast_series,'b--', label='forecast')
# plt.fill_between(lower_bound.index, lower_bound, upper_bound ,
#                  color='b', alpha=.2)
# plt.plot(lower_bound, color= 'y',label='Confidence Interval Upper bound ')
# plt.plot(upper_bound, color= 'y',label='Confidence Interval Lower bound ')
# plt.title('Forecast vs Actuals')
# plt.legend(loc='upper left', fontsize=8)
# plt.show()