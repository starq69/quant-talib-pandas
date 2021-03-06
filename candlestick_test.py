#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


pdf = pd.read_csv('/home/starq/REP/DATA/FINANCE/Quotazioni/KONE.csv'
                                 ,usecols=['Date','Open', 'High', 'Low', 'Close', 'Volume']
                                 ,parse_dates=['Date'],infer_datetime_format=True
                                 ,index_col='Date')



import matplotlib
import matplotlib.pyplot as plt   
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from mpl_finance import candlestick_ohlc


def pandas_candlestick_ohlc (dat, stick = "day", adj = False, otherseries = None):
    """
    thanks to Curtis MILLER
    https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/
    
    :param dat  : pandas DataFrame object with datetime64 index, and float columns "Open", "High", 
                  "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. 
                  Valid string inputs include "day", "week", "month", and "year", ("day" default), 
                  and any numeric input indicates the number of trading days included in a period
    :param adj  : A boolean indicating whether to use adjusted prices
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that 
                        hold other series to be plotted as lines

    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    #dayFormatter = DateFormatter('%d') #starq69 comment

    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    fields = ["Open", "High", "Low", "Close"]
    if adj:
        fields = ["Adj. " + s for s in fields]

    transdat = dat.loc[:,fields]
    transdat.columns = pd.Index(["Open", "High", "Low", "Close"])

    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
            grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                           index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365
        else: # starq69
            raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3]},
                                       index = [group.index[0]]))

    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    #print('fields : {}'.format(fields))
    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')

    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                      plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                      colorup = "green", colordown = "red", width = stick * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    # starq69
    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()

    plt.show()




def pandas_candlestick_ohlc_ex(dat, file_name=None, start_date=None, end_date=None, stick="day", adj=False, otherseries=None):
    """
    thanks to Curtis MILLER
    https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/

    :param dat  : pandas DataFrame object with datetime64 index, and float columns "Open", "High", 
                  "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. 
                  Valid string inputs include "day", "week", "month", and "year", ("day" default), 
                  and any numeric input indicates the number of trading days included in a period
    :param adj  : A boolean indicating whether to use adjusted prices
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that 
                        hold other series to be plotted as lines

    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)  # major ticks on the mondays
    alldays = DayLocator()  # minor ticks on the days
    transdat = None #starq69

    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    fields = ["Open", "High", "Low", "Close"]
    if adj:
        fields = ["Adj. " + s for s in fields]

    # starq69
    if start_date is not None and end_date is not None:
        transdat = dat.loc[start_date:end_date, fields]
    else:
        transdat = dat.loc[:, fields]

    transdat.columns = pd.Index(["Open", "High", "Low", "Close"])

    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1  # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1])  # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month)  # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0])  # Identify years
            grouped = transdat.groupby(list(set(["year", stick])))  # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [],
                                    "Close": []})  # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                       "High": max(group.High),
                                                       "Low": min(group.Low),
                                                       "Close": group.iloc[-1, 3]},
                                                      index=[group.index[0]]))
            if stick == "week":
                stick = 5
            elif stick == "month":
                stick = 30
            elif stick == "year":
                stick = 365
        else:  # starq69
            raise ValueError(
                'Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame(
            {"Open": [], "High": [], "Low": [], "Close": []})  # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                   "High": max(group.High),
                                                   "Low": min(group.Low),
                                                   "Close": group.iloc[-1, 3]},
                                                  index=[group.index[0]]))

    else:
        raise ValueError(
            'Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')

    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax, list(
        zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
            plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                     colorup="green", colordown="red", width=stick * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:, otherseries].plot(ax=ax, lw=1.3, grid=True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    # starq69
    # figManager = plt.get_current_fig_manager()
    # figManager.window.showMaximized()

    #plt.show()
    if file_name is not None:
        plt.savefig(file_name)


print('matplotlib: {}'.format(matplotlib.__version__))

pandas_candlestick_ohlc_ex(pdf, start_date='01-01-2013', end_date='01-01-2014', adj=False, stick='week')