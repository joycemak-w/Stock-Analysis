import requests
import pandas as pd
import schedule
import time
from datetime import datetime
import yfinance as yf
import pyodbc
from dotenv import load_dotenv, dotenv_values 
from connect import connect_to_azure

conn = pyodbc.connect(connect_to_azure())
cursor = conn.cursor()
stock_name = ["STAN", "HSBC", "BOC"]
symbols = ["2888.HK", "0005.HK", "2388.HK"]
# tickers = yf.Tickers("2888.HK 0005.HK 0939.HK 3988.HK 0023.HK D05.SI CHCJY 3968.HK O39.SI 0011.HK 5876.TW") # x交通 https://zh-yue.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E9%8A%80%E8%A1%8C%E4%B8%80%E8%A6%BD
# conn = sqlite3.connect('stock_database.db')
# cursor = conn.cursor()

# Create table for SQL Server
def create_table():
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Stocks' AND xtype='U')
    CREATE TABLE Stocks (
        [index]  INT        IDENTITY (1, 1) NOT NULL,
        [date]   DATETIME      NULL,
        [open]   REAL          NULL,
        [close]  REAL          NULL,
        [volume] INT           NULL,
        [symbol] NVARCHAR (50) NOT NULL,
        PRIMARY KEY CLUSTERED ([index] ASC)
    );
    ''')
    conn.commit()

def fetch_stock_data():
    data = pd.DataFrame()
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        stock_data = ticker.history(period="1y")
        stock_data['symbol'] = symbol
        data = pd.concat([data, stock_data])
    dates = []
    for d in data.index:
        date = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S%z').date()
        dates.append(date)
        
    # Clean and transform the data
    data = data.reset_index()
    data['Date'] = dates
    data = data.drop(['High', 'Low', 'Dividends', 'Stock Splits'], axis=1)
    data = data.rename(columns={'Date': 'date', 'Open': 'open', 'Close': 'close', 'Volume': 'volume', 'symbol': 'symbol'}).fillna(0)
    # print(data.isnull().sum())
    # Load the data into the SQL Server database

    # data.to_sql('Stocks', conn, index=True, if_exists='replace')

    for index, row in data.iterrows():
        # cursor.execute('''
        #     INSERT INTO Stocks ([date], [open], [close], [volume], [symbol]) VALUES (?, ?, ?, ?, ?);
        # ''', row['date'], row['open'], row['close'], row['volume'], row['symbol'])
        cursor.execute('''
            BEGIN
            IF NOT EXISTS (SELECT * FROM Stocks 
                            WHERE [date] = ?
                            AND [symbol] = ?)
            BEGIN
                INSERT INTO Stocks ([date], [open], [close], [volume], [symbol])
                VALUES (?, ?, ?, ?, ?)
            END
            END
        ''', row['date'], row['symbol'], row['date'], row['open'], row['close'], row['volume'], row['symbol'])

    conn.commit()

def main():
    create_table()
    # interval = input("Enter the interval in minutes (default is 1): ")
    # interval = int(interval) if interval.isdigit() else 1
    interval = 1440

    schedule.every(interval).minutes.do(fetch_stock_data)
    
    print(f"Scheduler started. Fetching stock data every {interval} minute(s).")
    
    fetch_stock_data()
    print("First fetching success.")
    while True:
        schedule.run_pending()
        time.sleep(1)
    # fetch_stock_data()

if __name__ == "__main__":
    main()


