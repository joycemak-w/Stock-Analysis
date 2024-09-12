import requests
import pandas as pd
import time
from datetime import datetime
import yfinance as yf
import pyodbc
from connect import connect_to_azure
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

conn = pyodbc.connect(connect_to_azure())
cursor = conn.cursor()
# stock_name = ["STAN", "HSBC", "BOC"]
symbols = {"2888.HK":"STAN", "0005.HK":"HSBC", "2388.HK":"BOC"}

# selected_symbol = '2888.HK'

def daily_return_chart(ax, selected_symbol):
    # # cursor.execute('''
    # #     SELECT [date],[close] FROM Stocks WHERE symbol = ?
    # # ''', selected_symbol)
    # # test = cursor.fetchall()

    query = "SELECT [date],[close] FROM Stocks WHERE symbol = '%s'" % selected_symbol 
    df = pd.read_sql(query, conn)

    # # df.to_csv('./close_p.csv', index=0)
    # df = pd.read_csv("./close_p.csv")

    df['Daily Return'] = df['close'].pct_change()
    df = df.set_index('date')
    sns.set_theme(style="whitegrid")

    # fig, ax = plt.subplots(1,1)
    # plt.figure(figsize=(12, 9))

    sns.histplot(data=df, x='Daily Return', bins=50, kde=True)
    # ax.set_xlabel(f'Daily Return')
    ax.set_ylabel('Count')
    ax.set_title(f'Daily Return of {symbols[selected_symbol]}')
    # plt.show()
    return ax

# ax = daily_return_chart()
# ax.plot()
# plt.show()

def moving_average_chart(ax, selected_symbol):
    
    query = "SELECT [date],[close] FROM Stocks WHERE symbol = '%s'" % selected_symbol 
    df = pd.read_sql(query, conn)
    # df.to_csv('./close_p.csv', index=0)
    # df = pd.read_csv("./close_p.csv")

    sns.set_theme(style="whitegrid")

    ma_day = [20,100]
    for ma in ma_day:
        column_name = f"MA for {ma} days"
        df[column_name] = df['close'].rolling(ma).mean()

    df = df.set_index('date')
    sns.set_theme(style="whitegrid")

    # fig, ax = plt.subplots(1,1)
    sns.lineplot(data=df,x='date',y='close', label='Close Price', ax=ax)
    for ma in ma_day:
        column_name = f"MA for {ma} days"
        sns.lineplot(data=df,x=df.index, y=column_name, label=column_name, ax=ax)
    # print(df.index[10])
    for i in range(1,len(df)):
        if(df['MA for 20 days'].iloc[i] >= df['MA for 100 days'].iloc[i] and df['MA for 20 days'].iloc[i-1] < df['MA for 100 days'].iloc[i-1]):
            # gold
            # print('golden: '+str(df['MA for 20 days'].iloc[i]))
            dot = plt.scatter(x=df.index[i-1],y=df['MA for 100 days'].iloc[i-1],c='y', zorder=2.5, label='Golden Cross')
            dot_info = mplcursors.cursor(dot,hover=mplcursors.HoverMode.Transient)
            dot_info.connect("add", lambda sel: (sel.annotation.set_backgroundcolor('yellow')))
            # plt.scatter(data=df,x=df.index,y='MA for 20 days', color='r')
        elif(df['MA for 20 days'].iloc[i] <= df['MA for 100 days'].iloc[i] and df['MA for 20 days'].iloc[i-1] > df['MA for 100 days'].iloc[i-1]):
            #death
            # print('death: '+str(df['MA for 20 days'].iloc[i]))
            dot = plt.scatter(x=df.index[i-1],y=df['MA for 100 days'].iloc[i-1],c='r',zorder=2.5, label='Death Cross')
            dot_info = mplcursors.cursor(dot,hover=mplcursors.HoverMode.Transient)
            dot_info.connect("add", lambda sel: (sel.annotation.set_backgroundcolor('pink')))
    ax.set_title(f'Simple Moving Average(MA) of {symbols[selected_symbol]}')
    ax.set_xlabel(None)
    ax.set_ylabel('Price')
    # ax.legend()
    # fig.tight_layout()
    return ax

# ax = moving_average_chart()
# ax.plot()
# plt.show()

def relation_pv_chart(ax,selected_symbol):
    query = "SELECT [date],[close],[volume] FROM Stocks WHERE symbol = '%s'" % selected_symbol 
    df = pd.read_sql(query, conn)
    # df.to_csv('./relation_p_v.csv', index=0)
    # df = pd.read_csv("./relation_p_v.csv")

    sns.set_theme(style="whitegrid")

    df['norm_close'] = [(x - min(df['close'])) / (max(df['close']) - min(df['close'])) for x in df['close']]
    df['norm_volume'] = [(x - min(df['volume'])) / (max(df['volume']) - min(df['volume'])) for x in df['volume']]

    df = df.set_index('date')
    sns.set_theme(style="whitegrid")

    # fig, ax = plt.subplots(1,1)
    sns.lineplot(data=df,x='date',y='norm_close', label='Close Price')
    sns.lineplot(data=df,x='date', y='norm_volume', label='Volume')
    ax.set_title(f'Relation of Close Price and Volume of {symbols[selected_symbol]}')
    ax.set_xlabel(None)
    ax.set_ylabel('Normalized Value')
    ax.legend()
    # fig.tight_layout()
    return ax

# ax = daily_return_chart('2888.HK')
# ax.plot()
# plt.show()

# fig, ax = plt.subplots(1,1)
# moving_average_chart(ax,'2888.HK')
# ax.grid(True)
# plt.show()