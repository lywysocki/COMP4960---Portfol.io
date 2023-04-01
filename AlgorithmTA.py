import finnhub
import pandas as pd
import datetime
import time

# dataframe print formatting
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)

# get current unix time
now = datetime.datetime.now()
unix_now = int(time.mktime(now.timetuple()))

finnhub_client = finnhub.Client(api_key="cfj73ghr01que34nr220cfj73ghr01que34nr22g")

# ticker to analyze
ticker = "META"


# returns a unix date num_days calendar days ago
def time_offset(date, num_days):
    return date - num_days*86400


# returns a unix date x trading days ago, where x is offset
# number of trading days between two dates must be greater than offset
def trading_days_ago(date_from, date_to, offset):
    df = pd.DataFrame(finnhub_client.stock_candles('SPY', 'D', date_from, date_to))["t"]
    return df[len(df) - offset]


# dataframes of spy
df_spy200 = pd.DataFrame
df_spy50 = pd.DataFrame

# dataframes of input ticker
df_ticker200 = pd.DataFrame
df_ticker50 = pd.DataFrame

fifty_days_ago = trading_days_ago(time_offset(unix_now, 100), unix_now, 50)


# returns the % change in ema from date_from to date_to
def ema(symbol, date_from, date_to, timeperiod):

    # temp is the unix timestamp of date_from - timeperiod trading days
    # timeperiod + 1 to avoid bug when date_from == date_to
    temp = trading_days_ago(time_offset(date_from, timeperiod * 2), date_from, timeperiod)

    ema_df = pd.DataFrame(finnhub_client.technical_indicator(symbol=symbol, resolution='D',
                                                             _from=temp,
                                                             to=date_to, indicator='EMA',
                                                             indicator_fields={"timeperiod": timeperiod}))

    # so far we get the date of date_from - timeperiod, dataframe from temp to current
    # reduce number of api calls by creating global dataframes
    if symbol == "SPY" and timeperiod == 200:
        global df_spy200
        df_spy200 = ema_df["ema"]
    elif symbol == "SPY" and timeperiod == 50:
        global df_spy50
        df_spy50 = ema_df["ema"]
    elif symbol == ticker and timeperiod == 200:
        global df_ticker200
        df_ticker200 = ema_df["ema"]
    elif symbol == ticker and timeperiod == 50:
        global df_ticker50
        df_ticker50 = ema_df["ema"]

    # [len(ema_df["ema"])-timeperiod-1]
    return (ema_df["ema"][len(ema_df["ema"])-1] / ema_df["ema"][timeperiod - 1] - 1) * 100, ema_df


# returns any number of bullish golden crosses or bearish death crosses in the last 50 calendar days
# df must contain ema only
def ema_cross(dataframe_200ema, dataframe_50ema):
    golden_cross = 0
    death_cross = 0

    i = len(dataframe_50ema)-1
    j = len(dataframe_200ema)-1
    while dataframe_50ema[i] != 0:

        if dataframe_200ema[j - 1] > dataframe_50ema[i] > dataframe_200ema[j]:
            death_cross += 1

        elif dataframe_200ema[j - 1] < dataframe_50ema[i] < dataframe_200ema[j]:
            golden_cross += 1

        i -= 1
        j -= 1

    return golden_cross, death_cross


# This returns the slope of the 200 ema compared between now and a year ago
ema200 = ema(ticker, time_offset(unix_now, 365), unix_now, 200)[0]
# This returns the slope of the 50 ema compared between now and 50 days ago
ema50 = ema(ticker, fifty_days_ago, unix_now, 50)[0]

spy_ema200 = ema("SPY", time_offset(unix_now, 365), unix_now, 200)[0]
spy_ema50 = ema("SPY", fifty_days_ago, unix_now, 50)[0]


print(ticker, "50", ema50)
print(ticker, "200", ema200)
print(" ")
print("SPY 200", spy_ema200)
print("SPY 50", spy_ema50)


# the number of golden or death crosses for the specified ticker
ticker_crosses = ema_cross(df_ticker200, df_ticker50)
spy_crosses = ema_cross(df_spy200, df_spy50)

print(ticker_crosses)
print(spy_crosses)


# determine a future daily slope from number of crosses
def future_slope(ema_cross_result):

    future_slope_var = 0

    if ema_cross_result[0] > 0 and ema_cross_result[1] > 0:
        total = ema_cross_result[0] + ema_cross_result[1]  # 1 + 2 = 3
        tc0 = ema_cross_result[0] / total  # 1 / 3 = .33334
        tc1 = 1 - tc0  # 1 - .34 = .66

        # weight ema50 as number of golden crosses, ema200 as number of death crosses
        future_slope_var = (ema50 * tc0 / 50) + (ema200 * tc1 / 365)

    elif ema_cross_result[0] > 0:
        # ticker golden cross
        future_slope_var = (ema50 * .7 / 50) + (ema200 * .3 / 365)

    elif ema_cross_result[1] > 0:
        # ticker death cross
        # this equation gets the daily percent difference of 50 and 200 ema, weighted dependent on direction
        future_slope_var = (ema50 * .3 / 50) + (ema200 * .7 / 365)

    # UPDATE THIS
    elif ema_cross_result[0] == 0 and ema_cross_result[1] == 0:
        future_slope_var = 0

    return future_slope_var


print(future_slope(ticker_crosses) * 50)






