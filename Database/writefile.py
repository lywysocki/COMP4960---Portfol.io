from stock_tickers import stock_tickers
from query import fetch_data_from_date
import pickle

# Separates the list of stocks into 8 different dictionaries to store the data for each stock from the database
# This is used for exporting the database to allow for local set up on other machines
part1 = {}
part2 = {}
part3 = {}
part4 = {}
part5 = {}
part6 = {}
part7 = {}
part8 = {}
part9 = {}
part10 = {}
part11 = {}
part12 = {}
part13 = {}
part14 = {}
part15 = {}

for i in range(0, len(stock_tickers)):
    table = stock_tickers[i] + "_table"
    result = fetch_data_from_date(stock_tickers[i], '01-01-2018')

    if i <= 500:
        part1[table] = result

    if 500 < i <= 1000:
        part2[table] = result

    if 1000 < i <= 1500:
        part3[table] = result

    if 1500 < i <= 2000:
        part4[table] = result

    if 2000 < i <= 2500:
        part5[table] = result

    if 2500 < i <= 3000:
        part6[table] = result

    if 3000 < i <= 3500:
        part7[table] = result

    if 3500 < i <= 4000:
        part8[table] = result

    if 4000 < i <= 4500:
        part9[table] = result

    if 4500 < i <= 5000:
        part10[table] = result

    if 5000 < i <= 5500:
        part11[table] = result

    if 5500 < i <= 6000:
        part12[table] = result

    if 6000 < i <= 6500:
        part13[table] = result

    if 6500 < i <= 7000:
        part14[table] = result

    if 7000 < i < len(stock_tickers):
        part15[table] = result

# Creates the files that the different dictionaries will write to in bytes
file1 = open('file1.txt', 'wb')
file2 = open('file2.txt', 'wb')
file3 = open('file3.txt', 'wb')
file4 = open('file4.txt', 'wb')
file5 = open('file5.txt', 'wb')
file6 = open('file6.txt', 'wb')
file7 = open('file7.txt', 'wb')
file8 = open('file8.txt', 'wb')
file9 = open('file9.txt', 'wb')
file10 = open('file10.txt', 'wb')
file11 = open('file11.txt', 'wb')
file12 = open('file12.txt', 'wb')
file13 = open('file13.txt', 'wb')
file14 = open('file14.txt', 'wb')
file15 = open('file15.txt', 'wb')

# Dumps all the bytes from the dictionaries to the respective files
pickle.dump(part1, file1)
pickle.dump(part2, file2)
pickle.dump(part3, file3)
pickle.dump(part4, file4)
pickle.dump(part5, file5)
pickle.dump(part6, file6)
pickle.dump(part7, file7)
pickle.dump(part8, file8)
pickle.dump(part9, file9)
pickle.dump(part10, file10)
pickle.dump(part11, file11)
pickle.dump(part12, file12)
pickle.dump(part13, file13)
pickle.dump(part14, file14)
pickle.dump(part15, file15)

# Closes connection to each file
file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()
file7.close()
file8.close()
file9.close()
file10.close()
file11.close()
file12.close()
file13.close()
file14.close()
file15.close()