import time
from database import write_to_db
from stock_tickers import stock_tickers
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Portfol.io2023",
    database="djangodatabase"
)

mycursor = mydb.cursor()

# List to keep track of what tables cannot load data from the API call
without_tables = []

# Code to populate each table with daily data for the past 5 years (2018)
counter = 0
index = 0
for x in range(0, len(stock_tickers)):
    if counter == 60:
        time.sleep(60)
        counter = 0
    else:
        counter += 1
        try:
            data = write_to_db(stock_tickers[x], '01-01-2018')
            i = 0
            table_name = stock_tickers[x] + "_table"
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (Year VARCHAR(255), Month VARCHAR(255), Day VARCHAR(255), Open DECIMAL(65,2), High DECIMAL(65,2), Low DECIMAL(65,2), Close DECIMAL(65,2))")
            mydb.commit()

            for i in range(len(data)):
                # pointers to grab data from returned dataframe
                year = data.iloc[i]['Year']
                month = data.iloc[i]['Month']
                day = data.iloc[i]['Day']
                open = data.iloc[i]['Open']
                high = data.iloc[i]['High']
                low = data.iloc[i]['Low']
                close = data.iloc[i]['Close']

                mycursor.execute(f"INSERT INTO {table_name} VALUES ({year}, {month}, {day}, {open}, {high}, {low}, {close})")

                mydb.commit()

            print(x)
        except TypeError:
            without_tables += [stock_tickers[x]]
            continue

# for stock in stock_tickers:
#     table = stock +"_table"
#     mycursor.execute(f"DELETE FROM {table}")
#     mydb.commit()
