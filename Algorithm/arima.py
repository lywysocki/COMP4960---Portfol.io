import numpy as np
from Algorithm.Algorithm2 import prediction_slope
from Algorithm.query import fetch_close_from_date

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from pmdarima.arima.utils import ndiffs
from sklearn import metrics
from datetime import date
from dateutil.relativedelta import *
import warnings

warnings.filterwarnings("ignore")


# gets the d value for ARIMA model~~
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


# gets the p value for ARIMA model
def get_p_value(dataset):
    # use Akaike's Information Criterion for selecting predictors of regression
    aic_result = arma_order_select_ic(dataset, ic=["aic"], trend="n")
    # p = order of the Auto Regressive term
    # the number of lags used as predictors
    return aic_result['aic_min_order'][0]


# gets the q value for ARIMA model
def get_q_value(dataset):
    # use Akaike's Information Criterion for selecting predictors of regression
    aic_result = arma_order_select_ic(dataset, ic=["aic"], trend="n")
    # q = moving average
    # number of lagged forcast errors that should go into the model
    return aic_result['aic_min_order'][1]


# create a differenced series based on inputted dataset
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        diff.append(dataset[i] - dataset[i - interval])
    return np.array(diff)


# invert differenced value
def inverse_difference(history, y_hat, interval=1):
    return y_hat + history[-interval]


# evaluates accuracy of the predictions via the average of mean squared error, root-mean-square error,
# and mean absolute percentage error
def timeseries_evaluation_metrics_func(true_data, pred_data):
    def mean_absolute_percentage_error(data, pred):
        data, pred = np.array(data), np.array(pred)
        return np.mean(np.abs((data - pred) / data)) * 100

    MSE = metrics.mean_absolute_error(true_data, pred_data)
    RMSE = np.sqrt(metrics.mean_squared_error(true_data, pred_data))
    MAPE = mean_absolute_percentage_error(true_data, pred_data)
    # NOTE: THIS IS THE CONFIDENCE VALUE
    return f'{(100 - ((MSE + RMSE + MAPE) / 3)):.2f}'


# based on an inputted number of months, returns the past date of months ago
def get_date(num):
    return (date.today() - relativedelta(days=+num)).strftime('%m-%d-%Y')


# prediction min, max, num days in prediction
def recommendation(last_historical_price, last_prediction_price, p_min, p_max, p_days):
    # BUY / SELL / HOLD recommendation
    rec = ""

    # slope between current date and last prediction date
    percent_difference = (last_prediction_price / last_historical_price - 1) * 100

    # daily slope between current date and last prediction date
    daily_percent = percent_difference / p_days

    # difference between prediction max and last prediction date
    max_difference = (last_prediction_price / p_max - 1) * 100

    # difference between prediction min and last prediction date
    min_difference = (last_prediction_price / p_min - 1) * 100

    # if the daily percent is annualized 15% growth and the last prediction is down 10% from prediction high
    if daily_percent > .06 and max_difference < -10:
        rec = "BUY"
    elif daily_percent > .03 and max_difference < 0:
        rec = "BUY"
    elif daily_percent > .06 and max_difference > 10:
        rec = "HOLD"
    elif daily_percent > .03 and max_difference >= 0:
        rec = "HOLD"
    else:
        rec = "SELL"

    return rec


# outputs a graph of predicted stock closing prices
# needs ~1.5 years of historical data to create a prediction
# only a graph of historical data will be produced in 1.5 years of historical data is not available
# generates and saves a graph figure, returns confidence in prediction
def forecast(ticker, num_hist_days , pred_days):
    # gets dataframe for a specific stock starting from a specific date
    #dataset = retrieve_stock_prices(ticker, get_date(num_hist_days))
    dataset = fetch_close_from_date(ticker, get_date(num_hist_days))
    # gets dataframe for a specific stock's historical data for forcast predictions
    #dataset_hist_for_pred = retrieve_stock_prices(ticker, '01-01-2000')
    dataset_hist_for_pred = fetch_close_from_date(ticker, '01-01-2000')
    #graph_path = os.path.abspath("./stockmath/static/graph.png")
    graph_path = 'C:\\Users\\Henry\\PycharmProjects\\COMP4960---PortfolioFinal2\\stockmath\\static\\graph.png'

    try:
        # seasonal difference
        x = dataset_hist_for_pred.values
        days_in_year = 365
        differenced = difference(x, days_in_year)

        # fit model
        model = ARIMA(differenced, order=(get_p_value(differenced), get_d_value(differenced), get_q_value(differenced)))
        model_fit = model.fit()

        num_of_pred_days = pred_days

        # Create dates for prediction (the x-axis)
        temp = []
        current_date = dataset_hist_for_pred.index.values[-1]
        for i in range(num_of_pred_days):
            temp.append(np.datetime64(current_date) + np.timedelta64(1, 'D'))
            current_date = temp[i]
        dates2 = np.array(temp)

        # multi-step forecast of future stock prices
        hist = x.tolist()
        for y_hat in model_fit.forecast(steps=num_of_pred_days):
            if inverse_difference(hist, y_hat, days_in_year) < 0:
                hist.append(abs(inverse_difference(hist, y_hat, days_in_year)))
            else:
                hist.append(inverse_difference(hist, y_hat, days_in_year))
        Y = hist[len(x):]

        # Adding sma prediction slope to arima
        slope = 1 + prediction_slope(ticker)

        # highest value in prediction graph
        prediction_max = Y[0]
        # lowest value in prediction graph
        prediction_min = Y[0]

        # Modifies the Y slope and finds the largest/smallest values
        for i in range(1, len(Y)):
            Y[i] *= slope
            if Y[i] > prediction_max:
                prediction_max = Y[i]
            if Y[i] < prediction_min:
                prediction_min = Y[i]

        last_historical_price = dataset.values[-1]
        last_prediction_price = Y[len(Y) - 1]

        rec = recommendation(last_historical_price, last_prediction_price, prediction_max, prediction_min, pred_days)
        print(rec)


        # new dataset that houses hist_data to test against accuracy of prediction
        test_data = dataset_hist_for_pred[int(len(dataset_hist_for_pred) - num_of_pred_days):]
        accuracy = timeseries_evaluation_metrics_func(test_data, Y)

        # graphs the historical data and the forecast/prediction
        plt.figure(figsize=(11, 5))
        plt.title(ticker)
        plt.xlabel('Dates')
        plt.ylabel('Closing Prices')
        # plots: (x values, y values, color of line, key label)
        plt.plot(dataset.index.values, dataset.values, 'slategray', label='Historical Price')
        plt.plot(dates2, Y, 'palevioletred', label='Predicted Price')
        plt.legend()
        # plt.show()
        plt.savefig(graph_path)
        return accuracy
    except ValueError:
        plt.figure(figsize=(11, 5))
        plt.title(ticker)
        plt.xlabel('Dates')
        plt.ylabel('Closing Prices')
        plt.plot(dataset.index.values, dataset.values, 'pink', label='Historical Price')
        plt.legend()
        # plt.show()
        plt.savefig(graph_path)
        raise ValueError("Not enough historical data to make an accurate prediction")