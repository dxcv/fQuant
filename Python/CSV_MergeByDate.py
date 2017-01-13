# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 13:24:28 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd

#
# Merge By Date Parameters
#
stock_ids  = ['UDI', 'Gold', 'Oil']
start_date = '2012-11-19'
end_date   = '2017-01-12'
is_debug   = True
path_datacenter = '../DataCenter/'

stock_number = len(stock_ids)
df = pd.DataFrame()
csv_filename = ''
suffix_1 = ''

#
# Iterative over all stocks
#
for i in range(stock_number):
    #
    # Fetch Stock Data
    #
    stock_id = stock_ids[i]
    stock_data = pd.read_csv(path_datacenter+stock_id+'.csv')
    stock_data_number = len(stock_data)
    if (stock_data_number == 0):
        print('stock', stock_id, 'does not have data!')
        raise SystemExit

    # Drop un-used columns
    stock_data.drop('open', axis=1, inplace=True)
    stock_data.drop('high', axis=1, inplace=True)
    stock_data.drop('low', axis=1, inplace=True)
    stock_data.drop('volume', axis=1, inplace=True)
    stock_data.drop('amount', axis=1, inplace=True)
    
    # Normalize the 'close' column
    close_max = stock_data['close'].max()
    close_min = stock_data['close'].min()
    print('close_max =', close_max, 'close_min =', close_min)
    for row in range(stock_data_number):
        close = stock_data.loc[row, 'close']
        stock_data.loc[row, 'close'] = (stock_data.loc[row, 'close'] - close_min) / (close_max - close_min)
    
    if (i == 0):
        df = stock_data
        suffix_1 = '_' + stock_id
    else:
        suffix_1 = ''
        df = pd.merge(df, stock_data, on='date', how='inner', suffixes=(suffix_1, '_' + stock_id))
    
    if is_debug:
        print(df.tail(10))

    csv_filename += '_' + stock_id

#
# Post-process
#
    
if is_debug:
    print(df.tail(10))
    
#
# Save to CSV File
#
df.to_excel(path_datacenter+csv_filename+'.xlsx')






































