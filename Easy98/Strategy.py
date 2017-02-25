# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:28:37 2017

@author: freefrom
"""

import GlobalSettings as gs
import Constants as c
import Utilities as u
from GetTrading import loadDailyHFQ
import pandas as pd
import numpy as np

bar_range_long = 21
bar_range_short = 13
r_range = 20

def strategyAncleXu(stock_id):
    # Ensure Stock LSHQ Data File is Available
    fullpath = c.fullpath_dict['lshq'] % stock_id
    if not u.hasFile(fullpath):
        print('Require LSHQ of Stock %s!' % stock_id)
        raise SystemExit

    # Load HFQ(LSHQ) Data
    lshq = loadDailyHFQ(stock_id)
    lshq_number = len(lshq)
    if lshq_number == 0:
        print('No LSHQ Data Available!')
        raise SystemExit

    # Convert to QFQ Data
    fq_factor = lshq['factor'][lshq_number-1]
    for i in range(lshq_number):
        for column in ['open','high','close','low']:
            lshq.ix[i, column] = lshq.ix[i, column] / fq_factor

    # Drop Factor
    lshq.drop('factor', axis=1, inplace=True)

    # Sort Index
    lshq.sort_values('date', inplace=True)
    if gs.is_debug:
        print(lshq.head(10))

    # Calculate Long Range High/Low
    lshq['range_high_long'] = 0.0
    lshq['range_low_long'] = 0.0
    for i in range(lshq_number):
        index_beg = (i-bar_range_long) if (i-bar_range_long) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'range_high_long'] = np.max(lshq['high'][index_beg:index_end])
        lshq.ix[i, 'range_low_long']  = np.min(lshq['low'][index_beg:index_end])

    # Calculate Short Range High/Low
    lshq['range_high_short'] = 0.0
    lshq['range_low_short'] = 0.0
    for i in range(lshq_number):
        index_beg = (i-bar_range_short) if (i-bar_range_short) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'range_high_short'] = np.max(lshq['high'][index_beg:index_end])
        lshq.ix[i, 'range_low_short']  = np.min(lshq['low'][index_beg:index_end])

    # Calculate R and Avg(R)
    lshq['R'] = 0.0
    lshq['Avg_R'] = 0.0
    for i in range(lshq_number):
        prev_close = lshq.ix[i-1, 'close'] if i > 0 else lshq.ix[i, 'open']
        high = lshq.ix[i, 'high']
        low = lshq.ix[i, 'low']
        lshq.ix[i, 'R'] = np.max([np.abs(high-low), np.abs(high-prev_close), np.abs(low-prev_close)])
        index_beg = (i-r_range) if (i-r_range) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'Avg_R'] = np.mean(lshq['R'][index_beg:index_end])

    # Save to CSV File
    u.to_csv(lshq, c.path_dict['strategy'], c.file_dict['sty_xu'] % stock_id)

    # Run Strategy
    lshq['long_open'] = False
    lshq['long_close'] = False
    lshq['short_open'] = False
    lshq['short_close'] = False
    has_long_open = False
    has_short_open = False
    event_index = []
    for i in range(lshq_number):
        close = lshq.ix[i, 'close']
        range_high_long = lshq.ix[i, 'range_high_long']
        range_low_long = lshq.ix[i, 'range_low_long']
        range_high_short = lshq.ix[i, 'range_high_short']
        range_low_short = lshq.ix[i, 'range_low_short']
        has_event = False
        if has_long_open == False:
            if close > range_high_long: # Long Open
                lshq.ix[i, 'long_open'] = True
                has_long_open = True
                has_event = True
        else:
            if close < range_low_short:
                lshq.ix[i, 'long_close'] = True
                has_long_open = False
                has_event = True
        if has_short_open == False:
            if close < range_low_long: # Short Open
                lshq.ix[i, 'short_open'] = True
                has_short_open = True
                has_event = True
        else:
            if close > range_high_short:
                lshq.ix[i, 'short_close'] = True
                has_short_open = False
                has_event = True
        if has_event:
            event_index.append(i)

    # Strategy Statistics
    stats = lshq.ix[event_index, ['date','close','long_open','long_close','short_open','short_close']]
    if gs.is_debug:
        print(stats.head(10))
    stats_number = len(stats)
    long_number = 0
    short_number = 0
    long_open_date = []
    long_open_price = []
    long_close_date = []
    long_close_price = []
    short_open_date = []
    short_open_price = []
    short_close_date = []
    short_close_price = []
    for i in range(stats_number):
        index = stats.index[i]
        print('Type is:', type(stats.ix[index, 'long_open']))
        if stats.ix[index, 'long_open'] == True: # Long Open
            long_open_date.append(stats.ix[index, 'date'])
            long_open_price.append(stats.ix[index, 'close'])
        if stats.ix[index, 'long_close'] == True: # Long Close
            long_close_date.append(stats.ix[index, 'date'])
            long_close_price.append(stats.ix[index, 'close'])
            long_number = long_number + 1
        if stats.ix[index, 'short_open'] == True: # Short Open
            short_open_date.append(stats.ix[index, 'date'])
            short_open_price.append(stats.ix[index, 'close'])
        if stats.ix[index, 'short_close'] == True: # Short Close
            short_close_date.append(stats.ix[index, 'date'])
            short_close_price.append(stats.ix[index, 'close'])
            short_number = short_number + 1

    # Profit Statistics
    long_profit = []
    total_long_profit = 0.0
    for i in range(long_number):
        profit = long_close_price[i] - long_open_price[i]
        long_profit.append(profit)
        total_long_profit = total_long_profit + profit
    short_profit = []
    total_short_profit = 0.0
    for i in range(short_number):
        profit = short_open_price[i] - short_close_price[i]
        short_profit.append(profit)
        total_short_profit = total_short_profit + profit
    print('\nStrategy Complete:')
    print('Total Long Trading = %04d, Total Long Profit = %.2f' % (long_number, total_long_profit))
    print('Total Short Trading = %04d, Total Short Profit = %.2f' % (short_number, total_short_profit))
    print('Total Trading = %04d, Total Profit = %.2f' % (long_number + short_number, total_long_profit + total_short_profit))
    for i in range(long_number):
        print('  B%04d, Open (%s) = %4.2f, Close (%s) = %4.2f, Profit = %4.2f' % (i+1, long_open_date[i], long_open_price[i], long_close_date[i], long_close_price[i], long_profit[i]))
    print('  -------------------------------------------------------------------')
    for i in range(short_number):
        print('  S%04d, Open (%s) = %4.2f, Close (%s) = %4.2f, Profit = %4.2f' % (i+1, short_open_date[i], short_open_price[i], short_close_date[i], short_close_price[i], short_profit[i]))

    # Trading Dataframe
    data_index_number = long_number+short_number
    data_columns=['type','open_date','open_price','close_date','close_price','profit']
    data_columns_number = len(data_columns)
    data_init = np.random.randn(data_index_number * data_columns_number)
    for i in range(data_index_number * data_columns_number):
        data_init[i] = np.nan
    data_index = []
    for i in range(data_index_number):
        data_index.append(i)
    trading = pd.DataFrame(data_init.reshape(data_index_number, data_columns_number),
                           index = data_index, columns = data_columns)
    for i in range(long_number):
        trading.ix[i,'type'] = 'B%04d'%(i+1)
        trading.ix[i,'open_date'] = long_open_date[i]
        trading.ix[i,'open_price'] = long_open_price[i]
        trading.ix[i,'close_date'] = long_close_date[i]
        trading.ix[i,'close_price'] = long_close_price[i]
        trading.ix[i,'profit'] = long_profit[i]
    for i in range(short_number):
        trading.ix[i+long_number,'type'] = 'S%04d'%(i+1)
        trading.ix[i+long_number,'open_date'] = short_open_date[i]
        trading.ix[i+long_number,'open_price'] = short_open_price[i]
        trading.ix[i+long_number,'close_date'] = short_close_date[i]
        trading.ix[i+long_number,'close_price'] = short_close_price[i]
        trading.ix[i+long_number,'profit'] = short_profit[i]

    # Save to CSV File
    u.to_csv(trading, c.path_dict['strategy'], c.file_dict['styres_xu'] % stock_id)