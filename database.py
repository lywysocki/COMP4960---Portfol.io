import finnhub
import pandas as pd
from datetime import datetime
import datetime
import time
import plotly.express as px
from stock_tickers import stock_tickers

# Connect to Finnhub.io with API key
finnhub_client = finnhub.Client(api_key="cg7of21r01qgl488q6jgcg7of21r01qgl488q6k0")


# Function to check the input date is valid
def is_valid_date(date):
    # lists containing months and there relative amount of days
    days31 = [1, 3, 5, 7, 8, 10, 12]
    days30 = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # pointers for day, month, year, and current year
    date_list = date.split('-')
    day = date_list[0]
    month = date_list[1]
    year = date_list[2]
    curr_date = datetime.date.today()
    curr_year = curr_date.year

    # check to ensure valid date
    if not day.isnumeric() or not month.isnumeric() or not year.isnumeric():
        return False
    if int(day) > 31:
        return False
    if int(month) > 12:
        return False
    if int(year) > int(curr_year):
        return False
    if int(day) == 31 and int(month) not in days31:
        return False
    if int(day) == 30 and int(month) not in days30:
        return False
    if int(day) == 29 and int(month) == 2 and int(year) % 4 != 0:
        return False

    return True


# Function to obtain user input
def get_input():
    ticker = input("Enter the stock ticker: ")
    while ticker not in stock_tickers:
        ticker = input("Please enter a valid stock: ")

    historical_date = input("What date would you like data to date back to (DD-MM-YYYY): ")

    while not is_valid_date(historical_date):
        historical_date = input("Please enter a valid date (DD-MM-YYYY): ")
        is_valid_date(historical_date)

    return ticker, historical_date


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

    fig = px.line(df, x="Date", y="Close", title="Test")
    fig.show()


# function to display current day market data to the user
def market_data():
    # 52WeekHigh
    # 52WeekLow
    # marketCapitalization
    # peNormalizedAnnual
    # dividendPerShareAnnual
    # Open
    # High
    # Low

    open = finnhub_client.quote('AAPL')['o']
    high = finnhub_client.quote('AAPL')['h']
    low = finnhub_client.quote('AAPL')['l']
    year_high = finnhub_client.company_basic_financials('AAPL', 'all')['metric'].get('52WeekHigh')
    year_low = finnhub_client.company_basic_financials('AAPL', 'all')['metric'].get('52WeekLow')
    market_cap = finnhub_client.company_basic_financials('AAPL', 'all')['metric'].get('marketCapitalization') * 1000000
    pe = finnhub_client.company_basic_financials('AAPL', 'all')['metric'].get('peNormalizedAnnual')
    dividend = finnhub_client.company_basic_financials('AAPL', 'all')['metric'].get('dividendPerShareAnnual')

    data = {
        'Open': open,
        'High': high,
        'Low': low,
        'Mkt Cap': market_cap,
        'P/E Ratio': pe,
        'Div Yield': dividend,
        '52-wk High': year_high,
        '52-wk Low': year_low
    }

    # df = pd.DataFrame(data)

    print(data)


market_data()
