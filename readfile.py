from stock_tickers import stock_tickers
from query import fetch_data_from_date
import pickle
import mysql.connector


# Separates the list of stocks into 8 different dictionaries to store the data for each stock from the database
# This is used for exporting the database to allow for local set up on other machines
# part1 = {}
# part2 = {}
# part3 = {}
# part4 = {}
# part5 = {}
# part6 = {}
# part7 = {}
# part8 = {}
# part9 = {}
# part10 = {}
# part11 = {}
# part12 = {}
# part13 = {}
# part14 = {}
# part15 = {}
#
# for i in range(0, len(stock_tickers)):
#     table = stock_tickers[i] + "_table"
#     result = fetch_data_from_date(stock_tickers[i], '01-01-2018')
#
#     if i <= 500:
#         part1[table] = result
#
#     if 500 < i <= 1000:
#         part2[table] = result
#
#     if 1000 < i <= 1500:
#         part3[table] = result
#
#     if 1500 < i <= 2000:
#         part4[table] = result
#
#     if 2000 < i <= 2500:
#         part5[table] = result
#
#     if 2500 < i <= 3000:
#         part6[table] = result
#
#     if 3000 < i <= 3500:
#         part7[table] = result
#
#     if 3500 < i <= 4000:
#         part8[table] = result
#
#     if 4000 < i <= 4500:
#         part9[table] = result
#
#     if 4500 < i <= 5000:
#         part10[table] = result
#
#     if 5000 < i <= 5500:
#         part11[table] = result
#
#     if 5500 < i <= 6000:
#         part12[table] = result
#
#     if 6000 < i <= 6500:
#         part13[table] = result
#
#     if 6500 < i <= 7000:
#         part14[table] = result
#
#     if 7000 < i < len(stock_tickers):
#         part15[table] = result
#
# # Creates the files that the different dictionaries will write to in bytes
# file1 = open('file1.txt', 'wb')
# file2 = open('file2.txt', 'wb')
# file3 = open('file3.txt', 'wb')
# file4 = open('file4.txt', 'wb')
# file5 = open('file5.txt', 'wb')
# file6 = open('file6.txt', 'wb')
# file7 = open('file7.txt', 'wb')
# file8 = open('file8.txt', 'wb')
# file9 = open('file9.txt', 'wb')
# file10 = open('file10.txt', 'wb')
# file11 = open('file11.txt', 'wb')
# file12 = open('file12.txt', 'wb')
# file13 = open('file13.txt', 'wb')
# file14 = open('file14.txt', 'wb')
# file15 = open('file15.txt', 'wb')
#
# # Dumps all the bytes from the dictionaries to the respective files
# pickle.dump(part1, file1)
# pickle.dump(part2, file2)
# pickle.dump(part3, file3)
# pickle.dump(part4, file4)
# pickle.dump(part5, file5)
# pickle.dump(part6, file6)
# pickle.dump(part7, file7)
# pickle.dump(part8, file8)
# pickle.dump(part9, file9)
# pickle.dump(part10, file10)
# pickle.dump(part11, file11)
# pickle.dump(part12, file12)
# pickle.dump(part13, file13)
# pickle.dump(part14, file14)
# pickle.dump(part15, file15)
#
# # Closes connection to each file
# file1.close()
# file2.close()
# file3.close()
# file4.close()
# file5.close()
# file6.close()
# file7.close()
# file8.close()
# file9.close()
# file10.close()
# file11.close()
# file12.close()
# file13.close()
# file14.close()
# file15.close()

# Opens each file and reads the data, saving it to a variable
with open('file1.txt', 'rb') as handle:
    data1 = handle.read()

with open('file2.txt', 'rb') as handle:
    data2 = handle.read()

with open('file3.txt', 'rb') as handle:
    data3 = handle.read()

with open('file4.txt', 'rb') as handle:
    data4 = handle.read()

with open('file5.txt', 'rb') as handle:
    data5 = handle.read()

with open('file6.txt', 'rb') as handle:
    data6 = handle.read()

with open('file7.txt', 'rb') as handle:
    data7 = handle.read()

with open('file8.txt', 'rb') as handle:
    data8 = handle.read()

with open('file9.txt', 'rb') as handle:
    data9 = handle.read()

with open('file10.txt', 'rb') as handle:
    data10 = handle.read()

with open('file11.txt', 'rb') as handle:
    data11 = handle.read()

with open('file12.txt', 'rb') as handle:
    data12 = handle.read()

with open('file13.txt', 'rb') as handle:
    data13 = handle.read()

with open('file14.txt', 'rb') as handle:
    data14 = handle.read()

with open('file15.txt', 'rb') as handle:
    data15 = handle.read()


# loads all the data from the files into dictionaries
d1 = pickle.loads(data1)
d2 = pickle.loads(data2)
d3 = pickle.loads(data3)
d4 = pickle.loads(data4)
d5 = pickle.loads(data5)
d6 = pickle.loads(data6)
d7 = pickle.loads(data7)
d8 = pickle.loads(data8)
d9 = pickle.loads(data9)
d10 = pickle.loads(data10)
d11 = pickle.loads(data11)
d12 = pickle.loads(data12)
d13 = pickle.loads(data13)
d14 = pickle.loads(data14)
d15 = pickle.loads(data15)

# joins all the dictionaries into one dictionary to store the data from the files
all_data = {}
all_data.update(d1)
all_data.update(d2)
all_data.update(d3)
all_data.update(d4)
all_data.update(d5)
all_data.update(d6)
all_data.update(d7)
all_data.update(d8)
all_data.update(d9)
all_data.update(d10)
all_data.update(d11)
all_data.update(d12)
all_data.update(d13)
all_data.update(d14)
all_data.update(d15)

# connects to the local host to create a new, local database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Portfol.io2023'
)

# pointer variable to connect to database to exectue SQL commands
mycursor = mydb.cursor()

# creates a new database (schema) to write tables to
mycursor.execute('CREATE DATABASE djangodatabase')
# saves the changes made to the database
mydb.commit()

# selects the newly created database to write all tables to
mycursor.execute('USE djangodatabase')
# saves the change made to use the selected database
mydb.commit()

# loops through all the keys in the dictionary containing all the data
# the keys are teh table names
# the value for each key is a list of tuples of each row containing each value for each data in each column
for key in all_data.keys():
    # creates the table for each stock we have data on and the columns necessary
    mycursor.execute(f'CREATE TABLE IF NOT EXISTS {key} (ID DECIMAL(65), Year VARCHAR(255), Month VARCHAR(255), Day VARCHAR(255), Open DECIMAL(65,2), High DECIMAL(65,2), Low DECIMAL(65,2), Close DECIMAL(65,2))')
    # saves the table in the database
    mydb.commit()

    # loops through each tuple of the value list and saves each data point accordingly to write to the table
    for entry in all_data.get(key):
        id = entry[0]
        year = entry[1]
        month = entry[2]
        day = entry[3]
        open = entry[4]
        high = entry[5]
        low = entry[6]
        close = entry[7]

        # inserts each row as intended into the table
        mycursor.execute(f"INSERT INTO {key} VALUES ({id}, {year}, {month}, {day}, {open}, {high}, {low}, {close})")
        # saves each row in the table
        mydb.commit()

