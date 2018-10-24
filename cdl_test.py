#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas_candlestick as plotter
import numpy as np
import pandas as pd
import talib
#import datetime


def main():
    print(plotter.mpl_version())

    rng = pd.date_range(pd.Timestamp("2018-03-10 09:00"), periods=3, freq='s')
    dt = rng.strftime('%B %d, %Y, %r')
    print(type(dt))
    print(dt)
    print('date_range type is : {}'.format(type(rng)))
    print(rng)

    # caricare un dataframe (pdf) relativo ad un simbolo (SYM)
    #
    symbol = 'CSPI'
    pdf = pd.read_csv('/home/starq/REP/DATA/FINANCE/Quotazioni/' + symbol + '.csv'
                      , usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                      , parse_dates=['Date'], infer_datetime_format=True
                      , index_col='Date')

    # pdf.info(memory_usage='deep')

    # applicare le features talib CDL
    #
    pdf['CDL2CROWS'] = talib.CDL2CROWS(pdf['Open'].values, pdf['High'].values, pdf['Low'].values, pdf['Close'].values)
    '''
    pdf['CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(pdf['Open'].values, pdf['High'].values, pdf['Low'].values, pdf['Close'].values)
    pdf['CDL3INSIDE'] = talib.CDL3INSIDE(pdf['Open'].values, pdf['High'].values, pdf['Low'].values, pdf['Close'].values)
    pdf['CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(pdf['Open'].values, pdf['High'].values, pdf['Low'].values, pdf['Close'].values)
    pdf['CDL3OUTSIDE'] = talib.CDL3OUTSIDE(pdf['Open'].values, pdf['High'].values, pdf['Low'].values, pdf['Close'].values)
    '''

    # per ogni talib CDL (CDL) :
    #
    CDLs = ['CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE', 'CDL3OUTSIDE']

    for cdl_pattern in ['CDL2CROWS']:

        #  <> 0 ?
        #
        match_bull = pdf.iloc[np.where(pdf[cdl_pattern].values == 100)]
        match_bear = pdf.iloc[np.where(pdf[cdl_pattern].values == -100)]
        print('values = 100 : {}'.format(match_bull.index.size))
        print('values = -100 : {}'.format(match_bear.index.size))

        for dt in match_bull.index.values:
            '''
            print('type of index element is : {}'.format(type(dt)))
            print(dt)
            start_date  = dt - np.timedelta64(2,'D')
            end_date    =  dt + np.timedelta64(2,'D')
            start_      = str(start_date)[:10]
            end_        = str(end_date)[:10]
            print(start_ + ' : ' + end_)
            _query = "Date <= '" + end_ + "' and Date >= '" + start_ + "'"
            print(_query)

            data = pdf.query(_query)
            print(data)
            '''
            idx  = pdf.index.get_loc(dt)
            inf_ = idx - 3
            sup_ = idx + 3
            data = pdf[inf_:sup_ + 1]
            print(data)

            fn='/home/starq/REP/JOBS/2018/quant-talib-pandas/pics/' + symbol + '-' + cdl_pattern + '-bull-' + str(idx) + '.png'
            print(fn)
            plotter.pandas_candlestick_ohlc_ex(data, file_name=fn, stick=1)

        for dt in match_bear.index.values:
            idx     = pdf.index.get_loc(dt)
            inf_    = idx - 3
            sup_    = idx + 3
            data    = pdf[inf_:sup_ + 1]
            print(data)

            fn = '/home/starq/REP/JOBS/2018/quant-talib-pandas/pics/' + symbol + '-' + cdl_pattern + '-bear-' + str(idx) + '.png'
            print(fn)
            plotter.pandas_candlestick_ohlc_ex(data, file_name=fn, stick=1)


if __name__ == '__main__':
    main()
