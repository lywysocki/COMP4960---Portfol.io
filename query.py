import time
from datetime import datetime
import mysql.connector
import pandas as pd
from stock_tickers import stock_tickers

# connect to the localhost database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyN3wP4ssw0rd",
    database="djangodatabase"
)

# pointer to execute SQL commands
mycursor = mydb.cursor()


# function to get next valid date from database if not in database table
# date param is the date input from the user
# results param is the list of tuples containing data from each row from the database table
# returns the index of the tuple the date is affiliated with
def get_date(date, results):
    # split the input date into a list of size 3
    date_string = date.split('-')
    # pull month
    month = date_string[0]
    # pull day
    day = date_string[1]
    # pull year
    year = date_string[2]

    # list of all tuples that have a date greater than or equal to desired date
    possible_dates = []

    # search through results list to find the tuple's index with the input date
    for data in results:
        # track the id, year, month, and day as int values to compare to user input date
        data_id = data[0]
        data_year = data[1]
        data_month = data[2]
        data_day = data[3]

        # pointer to the index in the results list of the input date
        index = 0

        # track the id corresponding to the row
        row_id = 0

        # if date exists in database return index
        if data_year == year and data_month == month and data_day == day:
            index = results.index(data)
            return index

        # if the date does not exist get the closest date
        if data_year == year and data_month == month:
            row_id = int(data[0])

        if data_id >= row_id:
            possible_dates += [data]

    # loop through the possible dates list to get the index of the closest date
    for data in possible_dates:
        # store the day from tuple as int for comparison
        data_day = int(data[3])
        # store input day as int for comparison
        int_day = int(day)

        if data_day >= int_day:
            index = results.get(data)
            break

    return index


# Function to fetch data from database from input date and on
# param: stock is the user input stock ticker
# param: data is the user input data (string MM-DD-YYYY)
def fetch_data_from_date(stock, date):
    # create table name to search for
    table = stock + "_table"
    # SQL command to pull data from all columns and rows in respective table
    mycursor.execute(f"SELECT * FROM {table}")
    # Saves the returned data as a list of tuples. Each tuple represents a row from the table.
    # Each tuple contains the data from the returned row in proper order.
    results = mycursor.fetchall()

    # store the length of the results list
    length = len(results)

    # store the index of the date to start at
    # index = get_date(date, results)

    # pointers for each key's value in the desired data dictionary
    ids = []
    desired_year = []
    desired_month = []
    desired_day = []
    desired_open = []
    desired_high = []
    desired_low = []
    desired_close = []

    # loop through the results list from the found index to the end of the list
    for i in range(0, length):
        current_tuple = results[i]
        ids += [current_tuple[0]]
        desired_year += [current_tuple[1]]
        desired_month += [current_tuple[2]]
        desired_day += [current_tuple[3]]
        # convert each value being added to the list into a float value to eliminate type error
        desired_open += [float(current_tuple[4])]
        desired_high += [float(current_tuple[5])]
        desired_low += [float(current_tuple[6])]
        desired_close += [float(current_tuple[7])]

    # dictionary to stored the desired data lists and convert to a dataframe
    desired_data = {
        'ID': ids,
        'Year': desired_year,
        'Month': desired_month,
        'Day': desired_day,
        'Open': desired_open,
        'High': desired_high,
        'Low': desired_low,
        'Close': desired_close
    }

    # convert the dictionary to a dataframe
    df = pd.DataFrame(desired_data)

    # return df
    return results


# Function to fetch the closing prices for the input stock from database from input date and on
# param: stock is the user input stock ticker
# param: data is the user input data (string MM-DD-YYYY)
def fetch_close_from_date(stock, date):
    # split the input date into a list of size 3
    date_string = date.split('-')
    # pull month
    month = int(date_string[0])
    # pull day
    day = int(date_string[1])
    # pull year
    year = int(date_string[2])

    # create table name to search for
    table = stock + "_table"
    # SQL command to pull data from all columns and rows in respective table
    mycursor.execute(f"SELECT * FROM {table}")
    # Saves the returned data as a list of tuples. Each tuple represents a row from the table.
    # Each tuple contains the data from the returned row in proper order.
    results = mycursor.fetchall()

    # store the length of the results list
    length = len(results)

    # search through results list to find the tuple's index with the input date
    for data in results:
        # track the year, month, and day as int values to compare to user input date
        data_year = int(data[0])
        data_month = int(data[1])
        data_day = int(data[2])

        # pointer to the index in the results list of the input date
        index = 0

        # pointers to create strings and check if equal
        # data_year_string, year_string = f"{year}", f"{year}"
        #
        # if data_month < 10:
        #     data_month_string = f"0{data_month}"
        # else:
        #     data_month_string = f"{data_month}"
        #
        # if data_day < 10:
        #     data_day_string = f"0{data_day}"
        # else:
        #     data_day_string = f"{data_day}"
        #
        # if month < 10:
        #     month_string = f"0{month}"
        # else:
        #     month_string = f"{month}"
        #
        # if day < 10:
        #     day_string = f"0{day}"
        # else:
        #     day_string = f"{day}"

        # check to see if the dates match
        # while data_year_string in data:
        #     if data_month_string in data:
        #         if data_day_string in data:
        #             print(data_day_string)
        #             # store the index
        #             print(index)
        #             index = results.index(data)
        #             break
        #         else:
        #             data_day += 1
        #     else:
        #         data_month += 1

    # pointer for the close key's value in the desired data dictionary
    desired_close = []
    # pointer for the desired date in the desired data dictionary
    desired_dates = []

    # loop through the results list from the found index to the end of the list
    for i in range(index, length):
        current_tuple = results[i]
        # gather desired year, month, and day
        desired_year = current_tuple[1]

        if int(current_tuple[2]) < 10:
            desired_month = f"0{current_tuple[2]}"
        else:
            desired_month = current_tuple[2]

        if int(current_tuple[3]) < 10:
            desired_day = f"0{current_tuple[3]}"
        else:
            desired_day = current_tuple[3]

        # convert to YYYY-MM-DD format
        # desired_date = f"{desired_year}-{desired_month}-{desired_day}"

        # convert to timestamp
        dt = datetime(int(desired_year), int(desired_month), int(desired_day), 0, 0)
        # timestamp = int(time.mktime(dt.timetuple()))

        # add the date to the list
        desired_dates.append(dt)

        # convert the value being added to the list into a float value to eliminate type error
        desired_close += [float(current_tuple[6])]

    # dictionary to stored the desired data lists and convert to a dataframe
    desired_data = {
        'Close': desired_close
    }
    # convert the dictionary to a dataframe
    df = pd.DataFrame(data=desired_data, index=pd.DatetimeIndex(data=desired_dates))

    return df
#
# stocks = {}
# no_table = []
# for stock in stock_tickers[4000:]:
#     table = stock + '_table'
#     try:
#         mycursor.execute(f"SELECT * FROM {table}")
#         results = mycursor.fetchall()
#         stocks[table] = results
#     except mysql.connector.errors.ProgrammingError:
#         no_table += [stock]
#
# # print(stocks)
# print(no_table)

# print(fetch_close_from_date('AAPL', '03-30-2023'))
