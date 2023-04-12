import pandas as pd
import numpy as np
from Database.database import retrieve_stock_prices
from Algorithm.Algorithm2 import prediction_slope
from Database.query import fetch_data_from_date
from Database.query import fetch_close_from_date

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from pmdarima.arima.utils import ndiffs
import warnings
warnings.filterwarnings("ignore")


# gets dataframe for a specific stock
def get_data(ticker, date, offset):

    df = retrieve_stock_prices(ticker, date, offset)
    return fetch_close_from_date(ticker, date)
    #return df['Close']


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


# dataset2 = dataset - x days for backtesting purpose
def forcast(ticker, num_of_pred_days):

    dataset = get_data(ticker, "01-01-2020", 0)
    dataset2 = get_data(ticker, "01-01-2020", 90)

    try:
        # seasonal difference
        x = dataset2.values
        # print(x)
        days_in_year = 365
        differenced = difference(x, days_in_year)

        # fit model
        model = ARIMA(differenced, order=(get_p_value(differenced), get_d_value(differenced), get_q_value(differenced)))
        model_fit = model.fit()

        # Creates dates for prediction (the x-axis)
        temp = []
        current_date = dataset2.index.values[-1]
        for i in range(num_of_pred_days):
            temp.append(np.datetime64(current_date) + np.timedelta64(1, 'D'))
            current_date = temp[i]
            #print(current_date)
        dates2 = np.array(temp)

        # multi-step forecast
        hist = x.tolist()
        for yhat in model_fit.forecast(steps=num_of_pred_days):
            hist.append(inverse_difference(hist, yhat, days_in_year))
        # print(hist[len(x):])
        Y = hist[len(x):]

        slope = 1 + prediction_slope(ticker)

        # add Y modification here?
        for i in range(1, len(Y)):
            Y[i] *= slope
        print(Y)

        # graphs the historical data and the forecast/prediction
        plt.figure(figsize=(11, 5))
        plt.xlabel('Dates')
        plt.ylabel('Closing Prices')
        # plots (x, y, color, key label)

        plt.plot(dataset.index.values, dataset.values, 'pink', label='Historical Price')
        plt.plot(dataset2.index.values, dataset2.values, 'green', label='Historical Price')

        plt.plot(dates2, Y, 'blue', label='Predicted Price')
        plt.legend()
        plt.show()
    except ValueError:
        plt.figure(figsize=(11, 5))
        plt.xlabel('Dates')
        plt.ylabel('Closing Prices')
        plt.plot(dataset.index.values, dataset.values, 'pink', label='Historical Price')
        plt.legend()
        plt.show()
        print("Not enough historical data to make an accurate prediction")
