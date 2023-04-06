from stock_tickers import stock_tickers
from query import fetch_data_from_date
import pickle
import mysql.connector

storage = {}
for stock in stock_tickers:
    table = stock + "_table"
    result = fetch_data_from_date(stock, '01-01-2018')
    storage[table] = result

file = open('database.txt', 'wb')

pickle.dump(storage, file)
file.close()

with open('database.txt', 'rb') as handle:
    data = handle.read()

d = pickle.loads(data)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password'
)

mycursor = mydb.cursor()

mycursor.execute('CREATE DATABASE djangodb')
mydb.commit()

for key in d.keys():
    mycursor.execute(f'CREATE TABLE IF NOT EXISTS {key} (Year VARCHAR(255), Month VARCHAR(255), Day VARCHAR(255), Open DECIMAL(65,2), High DECIMAL(65,2), Low DECIMAL(65,2), Close DECIMAL(65,2))')
    mydb.commit()

    for entry in d.get(key):
        year = entry[0]
        month = entry[1]
        day = entry[2]
        open = entry[3]
        high = entry[4]
        low = entry[5]
        close = entry[6]

        mycursor.execute(f"INSERT INTO {key} VALUES ({year}, {month}, {day}, {open}, {high}, {low}, {close})")
        mydb.commit()

