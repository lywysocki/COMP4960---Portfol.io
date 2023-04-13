import finnhub
import pandas as pd
import datetime
import time
from Database.query import fetch_data_from_date
from Database.database import retrieve_stock_prices

# dataframe print formatting
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)

# get current unix time
now = datetime.datetime.now()
unix_now = int(time.mktime(now.timetuple()))


def time_offset(date, num_days):
    return date - num_days*86400


# ################ FOR TESTING ################ #
def get_ticker_df(ticker):
    finnhub_client = finnhub.Client(api_key="cfj73ghr01que34nr220cfj73ghr01que34nr22g")

    #df = pd.DataFrame(finnhub_client.stock_candles(symbol, 'D', time_offset(unix_now, 730), unix_now))
    df = pd.DataFrame(finnhub_client.stock_candles(ticker, 'D', time_offset(unix_now, 1600), unix_now))

    years = []
    months = []
    days = []

    for timestamp in df["t"]:
        date_string = str(datetime.datetime.fromtimestamp(timestamp))
        date_to_add = date_string.split(' ')
        sub_date_to_add = date_to_add[0].split('-')
        years += [sub_date_to_add[0]]
        months += [sub_date_to_add[1]]
        days += [sub_date_to_add[2]]

    data = {
        'Year': years,
        'Month': months,
        'Day': days,
        'Close': df["c"]
    }

    return pd.DataFrame(data)


# #################### END TESTING ########################### #
#tickerdf = get_ticker_df("AAPL")


# dataframe length must be greater than requested num_days
def trading_days_ago(dataframe, num_days):
    days_ago = len(dataframe)-1-num_days
    return dataframe["Year"][days_ago], dataframe["Month"][days_ago], dataframe["Day"][days_ago]


# get the "period" sma at date x_days_ago
def get_sma(dataframe, x_days_ago, period):
    sma = 0

    count = 0
    # get the value x days from the last index of the dataframe
    index = len(dataframe) - 1 - x_days_ago
    while count < period:
        sma += dataframe["Close"][index]
        index -= 1
        count += 1

    return sma/period


# determines whether there have been any sma crosses in the last 50 trading days
def sma_cross(dataframe, x_days_ago):
    golden_cross = 0
    death_cross = 0

    count = x_days_ago
    while count < 50:

        # 50, 200 sma for yesterday and today
        sma50 = get_sma(dataframe, count, 50)
        sma501 = get_sma(dataframe, count+1, 50)
        sma200 = get_sma(dataframe, count, 200)
        sma2001 = get_sma(dataframe, count+1, 200)

        if sma2001 > sma501 and sma50 > sma200:
            golden_cross += 1

        elif sma2001 < sma501 and sma50 < sma200:
            death_cross += 1
        count += 1

    return golden_cross, death_cross


# multiplier to gold/death cross slope results?
def slope(ema50_slope, ema200_slope):
    ret = 1

    # if the stock is increasing or decreasing too fast, predict flattening
    if (ema200_slope >= 70 and ema50_slope >= 15) or (ema200_slope <= -70 and ema50_slope <= -15):
        ret = ema200_slope * .1
    elif (ema200_slope >= 50 and ema50_slope >= 10) or (ema200_slope <= -50 and ema50_slope <= -10):
        ret = ema200_slope * .2
    elif (ema200_slope >= 40 and ema50_slope >= 10) or (ema200_slope <= -40 and ema50_slope <= -10):
        ret = ema200_slope * .25

    elif (ema200_slope >= 30 and ema50_slope >= 5) or (ema200_slope <= -30 and ema50_slope <= -5):
        ret = ema200_slope * .45
    elif (ema200_slope >= 20 and ema50_slope >= 4) or (ema200_slope <= -20 and ema50_slope <= -4):
        ret = ema200_slope * .65

    # if a stock has increased or decreased too much and 50 sma has opposite slope, weigh 200 sma
    # this can be seen as a dip, trend continues
    elif (ema200_slope >= 70 and ema50_slope <= -15) or (ema200_slope <= -70 and ema50_slope >= 15):
        ret = ema200_slope * .2
    elif (ema200_slope >= 50 and ema50_slope <= -10) or (ema200_slope <= -50 and ema50_slope >= 10):
        ret = ema200_slope * .25
    elif (ema200_slope >= 40 and ema50_slope <= -10) or (ema200_slope <= -40 and ema50_slope >= 10):
        ret = ema200_slope * .3

    elif (ema200_slope >= 30 and ema50_slope <= -5) or (ema200_slope <= -30 and ema50_slope >= 5):
        ret = ema200_slope * .45
    elif (ema200_slope >= 20 and ema50_slope <= -4) or (ema200_slope <= -20 and ema50_slope >= 4):
        ret = ema200_slope * .65

    # if 50 sma volatile but 200 is not, heavily weigh 50 sma
    # if 200 sma slope positive and 50 sma slope positive
    elif (ema200_slope >= 0 and ema50_slope >= 40) or (ema200_slope <= 0 and ema50_slope <= -40):
        ret = ema50_slope * .25
    elif (ema200_slope >= 0 and ema50_slope >= 30) or (ema200_slope <= 0 and ema50_slope <= -30):
        ret = ema50_slope * .45
    elif (ema200_slope >= 0 and ema50_slope >= 20) or (ema200_slope <= 0 and ema50_slope <= -20):
        ret = ema50_slope * .6

    # if 50 sma is volatile and 200 sma opposite sign
    # if 200 slope positive and 50 slope negative
    elif (ema200_slope >= 0 and ema50_slope <= -40) or (ema200_slope <= 0 and ema50_slope >= 40):
        ret = ema50_slope * .25
    elif (ema200_slope >= 0 and ema50_slope <= -30) or (ema200_slope <= 0 and ema50_slope >= 30):
        ret = ema50_slope * .45
    elif (ema200_slope >= 0 and ema50_slope <= -20) or (ema200_slope <= 0 and ema50_slope >= 20):
        ret = ema50_slope * .6

    else:
        ret = (ema50_slope * .7) + (ema200_slope * .3)


    # if the 50 sma is too volatile
    # elif (ema50_slope >= 30) or (ema50_slope <= -30):
    # if 200 is negative and 50 is -30, weight 200 more, flattening
    # elif ema200_slope >= 0 and ema50_slope >= 30

    return ret


# old @ line 432 in scratch
# determine a future daily slope from number of crosses
def future_slope(sma_cross_result, ema50_slope, ema200_slope):

    future_slope_var = slope(ema50_slope, ema200_slope)

    # if there are both death and gold crosses
    if sma_cross_result[0] > 0 and sma_cross_result[1] > 0:
        total = sma_cross_result[0] + sma_cross_result[1]  # 1 + 2 = 3
        tc0 = sma_cross_result[0] / total  # 1 / 3 = .33334
        tc1 = 1 - tc0  # 1 - .34 = .66

        # weight ema50 as number of golden crosses, ema200 as number of death crosses
        future_slope_var = (ema50_slope * tc0) + (ema200_slope * tc1)

    elif sma_cross_result[0] > 0:
        # ticker golden cross
        future_slope_var += (ema50_slope * .5)

    elif sma_cross_result[1] > 0:
        # ticker death cross
        future_slope_var += (ema50_slope * .5)

    return future_slope_var


# TESTING METHOD
# return the percent change in stock price between current day and x trading days ago
# from is further away, to is recent
def percent_change(ticker, from_date_offset, to_date_offset):

    # replace with database code
    tickerdf = get_ticker_df(ticker)
    #tickerdf = fetch_data_from_date(ticker, "01-01-2020")

    index = len(tickerdf)-1  # last index of tickerdf, also most recent date

    # print(tickerdf["Close"][index-x_days_ago])
    # print(tickerdf["Close"][index])

    return (tickerdf["Close"][index-to_date_offset] / tickerdf["Close"][index-from_date_offset] - 1) * 100


# This returns the future expected slope for a given ticker over a 1-year period
def prediction_slope(ticker):
    # tickerdf = get_ticker_df(ticker)
    tickerdf = fetch_data_from_date(ticker, "01-01-2020")
    # tickerdf = retrieve_stock_prices(ticker, "01-01-2020", 0)

    # OFFSET FOR TESTING PURPOSES, starts prediction from x days ago, x = offset
    offset = 0
    # current 200, 50 sma
    ticker200sma = get_sma(tickerdf, 0+offset, 200)
    ticker50sma = get_sma(tickerdf, 0+offset, 50)

    # 200, 50 sma from 1 year ago, and 50 days ago
    ticker_200sma_1y = get_sma(tickerdf, 250+offset, 200)
    ticker_50sma_50d = get_sma(tickerdf, 50+offset, 50)

    ticker_200sma_slope = (ticker200sma / ticker_200sma_1y - 1) * 100
    ticker_50sma_slope = (ticker50sma / ticker_50sma_50d - 1) * 100

    # print(sma_cross(tickerdf, offset), "200sma:", ticker_200sma_slope, "50sma:", ticker_50sma_slope)

    return future_slope(sma_cross(tickerdf, offset), ticker_50sma_slope, ticker_200sma_slope) / 250


