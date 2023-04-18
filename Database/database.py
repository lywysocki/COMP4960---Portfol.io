import finnhub
import pandas as pd
from datetime import datetime
import time
from Database.stock_tickers import stock_tickers

# Connect to Finnhub.io with API key
finnhub_client = finnhub.Client(api_key="cg7of21r01qgl488q6jgcg7of21r01qgl488q6k0")


# Function to retrieve stock prices for the stock input from the user
# stock param is the ticker input from the user
# start_date (MM-DD-YYYY) param is the date of how far the user wants to pull historical data from
# return a dataframe containing the historical stock prices
# the dataframe columns are Date, Open, High, Low, Close

# example:
# retrieve_stock_prices('AAPL', '01-01-2018')
# returns a dataframe from January 1st, 2018 to current date containing the open, high, low, and close price for the
# input stock for each day
#             Date      Open     Close      High       Low
# 0     2018-01-01   42.5400   43.0650   43.0750   42.3150
# 1     2018-01-02   43.1325   43.0575   43.6375   42.9900
# 2     2018-01-03   43.1350   43.2575   43.3675   43.0200
# 3     2018-01-04   43.3600   43.7500   43.8425   43.2625
# 4     2018-01-07   43.5875   43.5875   43.9025   43.4825

# to manipulate the data:
# mydf = retrieve_stock_prices('AAPL', '01-01-2018')
# close_price = mydf['Close']

# to loop through dataframe:
# for i in range (len(mydf)):
#   each_close_price = mydf.iloc[i]['Close']
#   print(each_close_price)
def retrieve_stock_prices(stock, start_date):
    # split the input date for month, day, year retrieval
    date_string = start_date.split('-')

    # split the string to get int values for month, day, year
    start_month = int(date_string[0])
    start_day = int(date_string[1])
    start_year = int(date_string[2])

    # convert start_date to datetime
    start_dt = datetime(start_year, start_month, start_day, 0, 0)

    # store start_date as UNIX timestamp
    start_ts = int(time.mktime(start_dt.timetuple()))

    # get current time
    current_day = datetime.today()

    # get current time timestamp
    current_ts = int(time.mktime(current_day.timetuple()))

    # make an API call to gather necessary data
    stock_price_data = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)

    # create lists to store data retrieved from API call
    try:
        open = stock_price_data['o']
        close = stock_price_data['c']
        high = stock_price_data['h']
        low = stock_price_data['l']
        ts = stock_price_data['t']

        # lists to contain date breakdowns

        # convert timestamps into dates
        dates = []
        for timestamp in ts:
            # convert the POSIX timestamp to a more understandable DateTime
            date_string = datetime.fromtimestamp(timestamp)
            # date_to_add = date_string.split(' ')
            dates.append(date_string)  # += [date_to_add[0]]

        # create dictionary to populate dataframe
        data = {
            # 'Date': dates,
            'Open': open,
            'Close': close,
            'High': high,
            'Low': low
        }

        # create dataframe with the retrieved data and index of the DateTimes
        df = pd.DataFrame(data=data, index=pd.DatetimeIndex(data=dates))

        return df
    except KeyError:
        print(f'Error Caught. SKIPPING {stock}. Index: {stock_tickers.index(stock)}')
        pass

    pass


# function to display current day market data to the user
# this function will be called to display market information in our UI underneath the graph
def market_data(stock):
    # make API calls for each method needed to retrieve data
    quote = finnhub_client.quote(stock)
    financials = finnhub_client.company_basic_financials(stock, 'all')['metric']

    # pointers to store all necessary market data for a stock
    open = quote['o']
    high = quote['h']
    low = quote['l']
    curr = quote['c']
    year_high = financials.get('52WeekHigh')
    year_low = financials.get('52WeekLow')
    market_cap = financials.get('marketCapitalization')
    pe = financials.get('peNormalizedAnnual')
    dividend = financials.get('dividendPerShareAnnual')

    # store all pointers in a dictionary to write to dataframe
    data = {
        'Open': open,
        'High': high,
        'Low': low,
        'Current Price': curr,
        'Mkt Cap': market_cap,
        'P/E Ratio': pe,
        'Div Yield': dividend,
        '52-wk High': year_high,
        '52-wk Low': year_low
    }

    # loop to check if a value is None Type
    # if value is None Type change to '--' to represent no data
    # if value is a special case with additional formatting, add it
    # else format the number to two decimal places
    for k, v in data.items():
        if v is None:
            data[k] = '--'
        elif k == 'Mkt Cap':
            data[k] = f'{v}M'
        elif k == 'Div Yield':
            data[k] = f'{v}%'
        else:
            data[k] = f'{v:.2f}'

    return data


# function to write retrieved data to database
def write_to_db(stock, start_date):
    # split the input date for month, day, year retrieval
    date_string = start_date.split('-')

    # split the string to get int values for month, day, year
    start_month = int(date_string[0])
    start_day = int(date_string[1])
    start_year = int(date_string[2])

    # convert start_date to datetime
    start_dt = datetime(start_year, start_month, start_day, 0, 0)

    # store start_date as UNIX timestamp
    start_ts = int(time.mktime(start_dt.timetuple()))

    # get current time
    current_day = datetime.today()

    # get current time timestamp
    current_ts = int(time.mktime(current_day.timetuple()))

    try:
        # make an API call to gather necessary data
        stock_price_data = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)
    except finnhub.exceptions.FinnhubAPIException:
        time.sleep(60)
        stock_price_data = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)

    # create lists to store data retrieved from API call
    try:
        open = stock_price_data['o']
        close = stock_price_data['c']
        high = stock_price_data['h']
        low = stock_price_data['l']
        ts = stock_price_data['t']

        # lists to contain date breakdowns
        days = []
        months = []
        years = []

        # convert timestamps into day, month, year
        for timestamp in ts:
            date_string = str(datetime.fromtimestamp(timestamp))
            date_to_add = date_string.split(' ')
            sub_date_to_add = date_to_add[0].split('-')
            years += [sub_date_to_add[0]]
            months += [sub_date_to_add[1]]
            days += [sub_date_to_add[2]]

        # create dictionary to populate dataframe
        data = {
            'Year': years,
            'Month': months,
            'Day': days,
            'Open': open,
            'Close': close,
            'High': high,
            'Low': low
        }

        # create dataframe with the retrieved data
        df = pd.DataFrame(data)

        return df
    except KeyError:
        print(f'Error Caught. SKIPPING {stock}. Index: {stock_tickers.index(stock)}')
        pass

    pass
