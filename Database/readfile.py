from stock_tickers import stock_tickers
# from query import fetch_data_from_date
import pickle
import mysql.connector

# part1 = {}
# part2 = {}
# part3 = {}
# part4 = {}
# part5 = {}
# part6 = {}
# part7 = {}
# part8 = {}
# for i in range(0, len(stock_tickers)):
#     table = stock_tickers[i] + "_table"
#     result = fetch_data_from_date(stock_tickers[i], '01-01-2018')
#
#     if i <= 1000:
#         part1[table] = result
#
#     if 1000 < i <= 2000:
#         part2[table] = result
#
#     if 2000 < i <= 3000:
#         part3[table] = result
#
#     if 3000 < i <= 4000:
#         part4[table] = result
#
#     if 4000 < i <= 5000:
#         part5[table] = result
#
#     if 5000 < i <= 6000:
#         part6[table] = result
#
#     if 6000 < i <= 7000:
#         part7[table] = result
#
#     if 7000 < i < len(stock_tickers):
#         part8[table] = result
#
# file1 = open('file1.txt', 'wb')
# file2 = open('file2.txt', 'wb')
# file3 = open('file3.txt', 'wb')
# file4 = open('file4.txt', 'wb')
# file5 = open('file5.txt', 'wb')
# file6 = open('file6.txt', 'wb')
# file7 = open('file7.txt', 'wb')
# file8 = open('file8.txt', 'wb')
#
# pickle.dump(part1, file1)
# pickle.dump(part2, file2)
# pickle.dump(part3, file3)
# pickle.dump(part4, file4)
# pickle.dump(part5, file5)
# pickle.dump(part6, file6)
# pickle.dump(part7, file7)
# pickle.dump(part8, file8)
# file1.close()
# file2.close()
# file3.close()
# file4.close()
# file5.close()
# file6.close()
# file7.close()
# file8.close()

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

d1 = pickle.loads(data1)
d2 = pickle.loads(data2)
d3 = pickle.loads(data3)
d4 = pickle.loads(data4)
d5 = pickle.loads(data5)
d6 = pickle.loads(data6)
d7 = pickle.loads(data7)
d8 = pickle.loads(data8)

all_data = {}
all_data.update(d1)
all_data.update(d2)
all_data.update(d3)
all_data.update(d4)
all_data.update(d5)
all_data.update(d6)
all_data.update(d7)
all_data.update(d8)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Portfol.io2023'
)

mycursor = mydb.cursor()

mycursor.execute('CREATE DATABASE djangodatabase')
mydb.commit()

mycursor.execute('USE djangodatabase')
mydb.commit()

for key in all_data.keys():
    mycursor.execute(f'CREATE TABLE IF NOT EXISTS {key} (Year VARCHAR(255), Month VARCHAR(255), Day VARCHAR(255), Open DECIMAL(65,2), High DECIMAL(65,2), Low DECIMAL(65,2), Close DECIMAL(65,2))')
    mydb.commit()

    for entry in all_data.get(key):
        year = entry[0]
        month = entry[1]
        day = entry[2]
        open = entry[3]
        high = entry[4]
        low = entry[5]
        close = entry[6]

        mycursor.execute(f"INSERT INTO {key} VALUES ({year}, {month}, {day}, {open}, {high}, {low}, {close})")
        mydb.commit()
# print(len(all_data.keys()))
