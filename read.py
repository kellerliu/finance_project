
"""
-J , Aug 30 2015, 10:04m

Schema use python
Schema 2 uses python 3.4    """

'''
import os
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        print(os.path.join(root, name))

    for name in dirs:
        print(os.path.join(root, name))
'''

import csv
import sys
import datetime
import time
import sqlite3

        
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create table, only run once
c.execute("DROP TABLE IF EXISTS factorLoading")

c.execute(
    '''CREATE TABLE factorLoading
       (ticker   TEXT,
        capitalization     REAL)
    ''')

with open('factor_loading.csv', 'r', newline='') as csvfile:    
    spamreader = csv.reader(csvfile, skipinitialspace=True, delimiter = ',')
    count = 0
    header = next(spamreader)
    print("header:", header)

    for row in spamreader:
        count += 1
        ticker = row[1].strip()
        cap = row[37]

        c.execute("INSERT INTO factorLoading VALUES ('"
                  +ticker+"','"
                  +cap+"')")

    print(count, " lines")

'''
# check insertion    
c.execute("SELECT COUNT() FROM factorLoading")
countRow = c.fetchone()
print(countRow)
'''

c.execute("SELECT ticker FROM factorLoading "
          + "ORDER BY capitalization DESC "
          + "LIMIT 1000")




# Create table, only run once
c.execute("DROP TABLE IF EXISTS priceData")

c.execute(
    '''CREATE TABLE priceData
       (symid    TEXT,
        ticker   TEXT,
        open     REAL,
        high     REAL,
        low      REAL,
        close    REAL,
        volume   INTEGER	,
        adjClose REAL,
        date     TEXT)
    ''')


path = "price_data_2013"
import os
for root, dirs, files in os.walk(path, topdown=False):
    for filename in files:
        date = filename.split('.')[1]
        
        with open(path+'/'+filename, 'r', newline='') as file:
            spamreader = csv.reader(file, delimiter = '\t')
            header = next(spamreader)
            count = 0
            for row in spamreader:
                count += 1
                if len(row) != 8:
                    print(count, ",", len(row))
                else:
                    c.execute("INSERT INTO priceData VALUES ('"
                              +row[0]+"','"+row[1]+"','"+row[2]+"','"
                              +row[3]+"','"+row[4]+"','"+row[5]+"','"
                              +row[6]+"','"+row[7]+"','"+date+"')")

                
            # print(filename, count)



# check db
c.execute("SELECT ticker, COUNT(ticker) FROM priceData "
          + "GROUP BY ticker "
          + "HAVING COUNT(ticker) == 21")
rows = c.fetchall()
count = 0
for row in rows:
    if (row[1] == 21):
        count += 1

print(count);


# get ticker in top 1000, also has complete data


c.execute(" SELECT DISTINCT ticker FROM priceData ")

print("here")
rows = c.fetchall()
count = 0
for row in rows:
    count += 1

print(count);

c.execute(" SELECT DISTINCT ticker FROM priceData "
          + " WHERE "
          + " ticker IN "
          + " (SELECT ticker FROM factorLoading "
          + " ORDER BY capitalization DESC "
          + " LIMIT 1000) "
          + " AND ticker IN "
          + " (SELECT ticker FROM (SELECT ticker, COUNT(ticker) FROM priceData "
          + "  GROUP BY ticker "
          + "  HAVING COUNT(ticker) == 21) )")

print("here")
rows = c.fetchall()
count = 0
for row in rows:
    count += 1

print(count);

'''
# check db
c.execute("SELECT symid, adjClose, date FROM priceData ORDER BY symid, date")
firstRow = c.fetchone()
preSymid = firstRow[0]
preAdjClose = firstRow[1]

rows = c.fetchall()
count = 0
for row in rows:
    currentSymid = row[0]
    currentAdjClose = row[1]
    currentDate = row[2]

    if currentSymid == preSymid:
    print(currentSymid,  currentDate, (currentAdjClose - preAdjClose)/preAdjClose )
        preAdjClose = currentAdjClose
        count += 1

    else:
        if(count != 20):
            print(preSymid)
        
        preSymid = currentSymid
        preAdjClose = currentAdjClose           
        count = 0

'''
        
# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


