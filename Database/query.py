import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password1!",
    database="djangodatabase"
)

mycursor = mydb.cursor()


# Function to fetch data from database
def fetch_data(stock):
    table = stock + "_table"
    # SQL command to pull data from all columns and rows in respective table
    mycursor.execute(f"SELECT * FROM {table}")
    # Saves the returned data as a list of tuples. Each tuple represents a row from the table.
    # Each tuple contains the data from the returned row in proper order.
    results = mycursor.fetchall()
    return results


# Function to fetch data from database from input date and on
# param: stock is the user input stock ticker
# param: data is the user input data (string MM-DD-YYYY)
def fetch_data_from_date(stock, date):
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

        # check to see if the dates match
        if data_year == year and data_month == month and data_day == day:
            # store the index
            index = results.index(data)
            #print(index)
            break

    # pointers for each key's value in the desired data dictionary
    desired_year = []
    desired_month = []
    desired_day = []
    desired_open = []
    desired_high = []
    desired_low = []
    desired_close = []

    # loop through the results list from the found index to the end of the list
    for i in range(index, length):
        current_tuple = results[i]
        desired_year += [current_tuple[0]]
        desired_month += [current_tuple[1]]
        desired_day += [current_tuple[2]]
        # convert each value being added to the list into a float value to eliminate type error
        desired_open += [float(current_tuple[3])]
        desired_high += [float(current_tuple[4])]
        desired_low += [float(current_tuple[5])]
        desired_close += [float(current_tuple[6])]

    # dictionary to stored the desired data lists and convert to a dataframe
    desired_data = {
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

    return df


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

        # check to see if the dates match
        if data_year == year and data_month == month and data_day == day:
            # store the index
            index = results.index(data)
            # print(index)
            break

    # pointers for the close key's value in the desired data dictionary
    desired_close = []

    # loop through the results list from the found index to the end of the list
    for i in range(index, length):
        current_tuple = results[i]
        # convert the value being added to the list into a float value to eliminate type error
        desired_close += [float(current_tuple[6])]

    # dictionary to stored the desired data lists and convert to a dataframe
    desired_data = {
        'Close': desired_close
    }

    # convert the dictionary to a dataframe
    df = pd.DataFrame(desired_data)

    return df
