import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import yfinance as yf
import pyodbc
from connect import connect_to_azure
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import ta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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


def rsi_macd_chart(selected_symbol):
    query = "SELECT [date],[close] FROM Stocks WHERE symbol = '%s'" % selected_symbol 
    df = pd.read_sql(query, conn)
    # df.to_csv('./rsi_macd.csv', index=0)
    # df = pd.read_csv("./rsi_macd.csv") 
    df['date']=pd.to_datetime(df['date'])
    df = df.set_index('date')
    #RSI
    change = df["close"].diff()
    change.dropna(inplace=True)

    # Create two copies of the Closing price Series
    change_up = change.copy()
    change_down = change.copy()

    change_up[change_up<0] = 0
    change_down[change_down>0] = 0

    # Verify that we did not make any mistakes
    change.equals(change_up+change_down)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(14).mean()
    avg_down = change_down.rolling(14).mean().abs()

    rsi = 100 * avg_up / (avg_up + avg_down)
    rsi[df.index[0]] = 0.0
    rsi = rsi.sort_index()
    # new_row = pd.DataFrame([0.0], index=(df.index[0]))
    # rsi = pd.concat([new_row, rsi]).sort_index()
    rsi = rsi.fillna(0)
    # print(rsi)

    #MACD
    macd_object = ta.trend.MACD(df['close'])
    df['MACD'] = macd_object.macd()
    df['MACD_Signal'] = macd_object.macd_signal()
    df['MACD_Diff'] = macd_object.macd_diff()

    # Identify starting points of bullish and bearish trends
    df['Bullish_Run_Start'] = (df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1))
    df['Bearish_Run_Start'] = (df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1))
    # print(type(rsi.index[0]))

    # Identify gold and death cross points
    df['Golden_Cross'] = (df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1))
    df['Death_Cross'] = (df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1))

    # Create two charts on the same figure.
    plt.figure(figsize=(10,8))
    ax1 = plt.subplot2grid((13, 1), (0, 0), rowspan = 3, colspan = 1)
    ax2 = plt.subplot2grid((13, 1), (5, 0), rowspan = 3, colspan = 1)
    ax3 = plt.subplot2grid((13, 1), (10, 0), rowspan = 3, colspan = 1)
    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    
    # First chart:
    # Plot the closing price on the first chart
    ax1.set_title('RSI and MACD')
    # df['label'] = np.where((rsi<70)&(rsi>30), 1, -1)
    df['label'] = np.where((rsi<70), 1, -1)
    def plot_func(group):
        color = 'r' if (group['label'] < 0).all() else 'g'
        lw = 2.0
        ax1.plot(group.index, group.close, c=color, linewidth=lw)

    df.groupby((df['label'].shift() * df['label'] < 0).cumsum()).apply(plot_func)

    ax1.scatter(df.index[df['Bullish_Run_Start']], df['close'][df['Bullish_Run_Start']], marker='^', color='#FFD700', label='Start Bullish Run' ,zorder=2.5)
    ax1.scatter(df.index[df['Bearish_Run_Start']], df['close'][df['Bearish_Run_Start']], marker='v', color='#7e1300', label='Start Bearish Run' ,zorder=2.5)
    ax1.legend()

    # Second chart
    # Plot the RSI
    ax2.set_title('Relative Strength Index')
    ax2.plot(rsi, color='orange', linewidth=1)
    # Add two horizontal lines, signalling the buy and sell ranges.
    # Oversold
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

    # Third chart
    # Plot the MACD
    ax3.set_title('Moving Average Convergence/Divergence')
    # fast line: 12days EMA - 26days EMA
    # EMA: higher weighting on recent price SMA: same weighting
    ax3.plot(df['MACD'], label='MACD Line', color='blue', alpha=0.5, linewidth=1)
    # slow line
    ax3.plot(df['MACD_Signal'], label='Signal Line', color='red', alpha=0.5, linewidth=1)
    ax3.bar(df.index, df['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)

    # Markers for bullish and bearish crossover
    ax3.scatter(df.index[df['Golden_Cross']], df['MACD'][df['Golden_Cross']], marker='^', color='g', label='Bullish Crossover')
    ax3.scatter(df.index[df['Death_Cross']], df['MACD'][df['Death_Cross']], marker='v', color='r', label='Bearish Crossover')
    ax3.legend()
    # Display the charts
    plt.show()
    # return fig


# rsi_macd_chart('2888.HK')


