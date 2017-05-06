# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:00:55 2017

@author: freefrom
"""

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
import Common.GlobalSettings as gs

#
# Normalize Price Data by Divided by Mean * Std
#
# The reason not use (price-mean)/std is due to this will generate negative numbers.
# Negative numbers will cause problem for the following relative to first valid price calculation.
# A percentage based price representation requires all price should be positive.
# So finally I choose to use (price/mean)/std as the normalization method.
#
def normalize_price(price):
    mean = price.mean()
    std = price.std()
    price = price.map(lambda x: (x-mean)/std)
    price_min = price.min()
    price = price.map(lambda x: (x-price_min + 1.0))
    return price

def plot_coefficient_price(stock_ids, allprice, postfix, series_name, benchmark_name):
    # If want to debug benchmark only (without stocks), set below flag to True.
    debug_benchmark_only = False

    # Extract Stock Prices and Normalize Them
    row_number = len(allprice)
    stock_number = len(stock_ids)
    columns = ['date', benchmark_name]
    if not debug_benchmark_only:
        for i in range(stock_number):
            stock_id = u.stockID(stock_ids[i])
            columns.append(stock_id)
    prices = u.createDataFrame(row_number, columns)
    prices['date'] = allprice['date']
    prices[benchmark_name] = allprice['close']
    if not debug_benchmark_only:
        for i in range(stock_number):
            stock_id = u.stockID(stock_ids[i])
            prices[stock_id] = allprice['close_'+stock_id]
    if debug_benchmark_only:
        print('Original Price')
        print(prices)

    # Normalize Price
    for i in range(1, len(columns)):
        column = columns[i]
        prices[column] = normalize_price(prices[column])
    if debug_benchmark_only:
        print('Normalized Price')
        print(prices)

    # Calculate Relative Price w.r.t. First Valid Price
    for i in range(1, len(columns)):
        column = columns[i]
        row = -1
        for j in range(row_number):
            if not np.isnan(prices.ix[j,column]): # Find first valid price
                row = j
                break
        if row != -1:
            if debug_benchmark_only:
                print('Row =', row)
            ref_price = prices.ix[row,column] # Need to be cached in the first place as it will be normalized to one later.
            for j in range(row, row_number):
                cur_price = prices.ix[j,column]
                if not np.isnan(cur_price):
                    prices.ix[j,column] = 1.0 + (cur_price-ref_price)/ref_price
    if debug_benchmark_only:
        print('Relative Price')
        print(prices)

    # Plot Figure
    fig = plt.figure(figsize=(32, 18), dpi=72, facecolor="white")
    axes = plt.subplot(111)
    axes.cla() # Clear Axes

    # Define Font
    font = {'family' : 'serif',
            'color'  : 'black',
            'weight' : 'normal',
            'size'   : 18,
    }

    # Plot Sub-figure 1
    title = '%s vs. %s' % (series_name, benchmark_name)
    plt.title(title, fontdict=font)
    axes.set_xlabel('', fontdict=font)
    axes.set_ylabel('Ratio', fontdict=font)
    prices.plot(x='date', y=benchmark_name, ax=axes, color='grey', lw=2.0, ls='--')
    if not debug_benchmark_only:
        for i in range(stock_number):
            column = u.stockID(stock_ids[i])
            prices.plot(x='date', y=column, ax=axes)

    # Common Format for Both Sub-figures
    axes.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

    # Save Figure
    fig_key = 'fig_coef'
    fig_path = c.path_dict[fig_key]
    fig_name = '_'.join([postfix, series_name, 'vs', benchmark_name, u.dateToStr(u.today())])
    fig_file = c.file_dict[fig_key] % fig_name
    u.saveFigure(fig, fig_path, fig_file)