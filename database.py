import finnhub
import pandas as pd
from datetime import datetime
import time

# Connect to Finnhub.io with API key
finnhub_client = finnhub.Client(api_key="cg7of21r01qgl488q6jgcg7of21r01qgl488q6k0")


# Function to retrieve stock prices for the stock input from the user
# stock param is the ticker input from the user
# start_date (MM-DD-YYYY) param is the date of how far the user wants to pull historical data from
# return a dataframe containing the historical stock prices
def retrieve_stock_prices(stock, start_date):
    # split the input date for month, day, year retrieval
    date_string = start_date.split('-')

    # split the string to get int values for month, day, year
    start_month = int(date_string[0])
    start_day = int(date_string[1])
    start_year = int(date_string[2])

    # convert start_date to datetime
    start_dt = datetime(start_year, start_day, start_month, 0, 0)

    # store start_date as UNIX timestamp
    start_ts = int(time.mktime(start_dt.timetuple()))

    # get current time
    current_day = datetime.today()

    # get current time timestamp
    current_ts = int(time.mktime(current_day.timetuple()))

    # create lists to store data retrieved from API calls
    open = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['o']
    close = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['c']
    high = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['h']
    low = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['l']
    volume = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['v']
    ts = finnhub_client.stock_candles(stock, 'D', start_ts, current_ts)['t']

    # convert timestamps into dates
    dates = []
    for timestamp in ts:
        date_string = str(datetime.fromtimestamp(timestamp))
        date_to_add = date_string.split(' ')
        dates += [date_to_add[0]]


    # create dictionary to populate dataframe
    data = {
        'Date': dates,
        'Open': open,
        'Close': close,
        'High': high,
        'Low': low,
        'Volume': volume
    }

    # create dataframe with the retrieved data
    df = pd.DataFrame(data)

    print(df)

retrieve_stock_prices('AAPL', '01-01-2018')
