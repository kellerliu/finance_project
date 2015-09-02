
"""
-J , Aug 30 2015, 10:04m

Schema use python
Schema 4 uses python 3.4    """

import csv
import sys
import datetime
import time
import sqlite3


conn = sqlite3.connect('data.db')
c = conn.cursor()


# Create table, only run once
c.execute("DROP TABLE IF EXISTS highFreqQuote")

c.execute(
    '''CREATE TABLE highFreqQuote
       (time_string text, 
        stock text, 
        message text,
        bid_price float,
        ask_price float,
        bid_size int,
        ask_size int)
    ''')

c.execute("DROP TABLE IF EXISTS highFreqTrade")

c.execute(
    '''CREATE TABLE highFreqTrade
       (time_string text, 
        stock text, 
        message text,
        trade_price float,
        trade_size int)
    ''')


with open('sample.taq.csv', 'r', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter = ',')
    count = 0
    for row in spamreader:
        count += 1
        
        if len(row) != 7:
            print("line number: ", count,
                  ", elements: ", len(row),
                  ", content: ", row)
        else:
            valid = True;

            # 1. Validate time
            timeString = row[0];
            try:
                # This is to validate the time format, will get error with bad data
                datetimeInfo = datetime.datetime.strptime(timeString,"%H%M%S.%f")
                # time = datetimeInfo.time();
                # print(time.hour, time.minute, time.second, time.microsecond);
            except:
                print("line ", count, ", wrong time:", timeString);
                valid = False;

            # 2. Validate stock               
            stock = row[1];
            if (stock != "JPM") & (stock != "SLB") & (stock != "WFC") & (stock != "NOV"):
                valid = False;
                print("line ", count, ", wrong stock:", stock);

            # 3. Validate message type
            message = row[2];
            if (message != "Q") & (message != "T") :
                valid = False;
                print("line ", count, ", wrong message:", message);

            # 4. Validate quote message
            if message == "Q":
                bidPrice = float(row[3]);
                askPrice = float(row[4]);
                bidSize = int(row[5]);
                askSize = int(row[6]);
                
                # 4.1 Validate bid price and ask price
                if (bidPrice <= 0) |(askPrice <= 0) | (bidPrice > askPrice):
                    valid = False;
                    print("line ", count, ", wrong bid ask price:", bidPrice, askPrice);

                if (bidSize < 0) | (askSize < 0):
                    valid = False;
                    print("line ", count, ", wrong bid ask size:", bidSize, askSize);

                # 4.2 save to db
                if valid:
                #c.execute("INSERT INTO highFreqQuote VALUES ('" + timeString +"','"+ stock +"','"+message+"','"+bidPrice+"', '"+askPrice+"','"+bidSize+"','"+askSize+"')")

                 c.execute("INSERT INTO highFreqQuote VALUES ('" + timeString +"','"+ stock +"','"+message+"','"+1+"', '"+askPrice+"','"+bidSize+"','"+askSize+"')")


            # 5. Validate trade message
            if message == "T":
                tradePrice = float(row[3]);
                tradeSize = int(row[4]);

                if (tradePrice <= 0) |(tradeSize <= 0) :
                    valid = False;
                    print("line ", count, ", wrong trade message:", tradePrice, tradeSize);

                if valid:
                    c.execute("INSERT INTO highFreqTrade VALUES ('" +timeString+"','"+stock+"','"+message+"','"+tradePrice+"', '"+tradeSize+"')")

                    
        
            """
            print ("data row", count,
                   "time", row[0],
                   "stock", row[1],
                   "message", row[2],
                   "bid_price", row[3],
                   "ask_price", row[4],
                   "bid_size", row[5],
                   "ask_size", row[6])"""
            
            # Insert a row of data


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


