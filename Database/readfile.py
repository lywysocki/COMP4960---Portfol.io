import pickle
import mysql.connector

# Opens each file and reads the data, saving it to a variable
with open('Database/file1.txt', 'rb') as handle:
    data1 = handle.read()

with open('Database/file2.txt', 'rb') as handle:
    data2 = handle.read()

with open('Database/file3.txt', 'rb') as handle:
    data3 = handle.read()

with open('Database/file4.txt', 'rb') as handle:
    data4 = handle.read()

with open('Database/file5.txt', 'rb') as handle:
    data5 = handle.read()

with open('Database/file6.txt', 'rb') as handle:
    data6 = handle.read()

with open('Database/file7.txt', 'rb') as handle:
    data7 = handle.read()

with open('Database/file8.txt', 'rb') as handle:
    data8 = handle.read()

with open('Database/file9.txt', 'rb') as handle:
    data9 = handle.read()

with open('Database/file10.txt', 'rb') as handle:
    data10 = handle.read()

with open('Database/file11.txt', 'rb') as handle:
    data11 = handle.read()

with open('Database/file12.txt', 'rb') as handle:
    data12 = handle.read()

with open('Database/file13.txt', 'rb') as handle:
    data13 = handle.read()

with open('Database/file14.txt', 'rb') as handle:
    data14 = handle.read()

with open('Database/file15.txt', 'rb') as handle:
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
    password='Password1!'
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
