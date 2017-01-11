# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 13:51:16 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import numpy as np
import pandas as pd
import datetime as dt

#
# Relative Return Statistics Parameters
#
stock_ids  = ['000001', '399001', '000300', '399005', '399006']
bench_index= 2
is_index   = True
start_date = '2011-01-04'
end_date   = '2016-12-30'
is_debug   = True
path_datacenter = '../DataCenter/'

stock_number = len(stock_ids)
df = pd.DataFrame()
period_stock_date = [dt.date]

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

    stock_start_date = stock_data['date'][0]
    stock_end_date = stock_data['date'][stock_data_number-1]
    if stock_start_date != start_date:
        print('stock start date does not match start date!', 'stock_start_date =', stock_start_date, 'while start_date =', start_date)
    if stock_end_date != end_date:    
        print('stock end date does not match end date!', 'stock_end_date =', stock_end_date, 'while end_date =', end_date)
    
    stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y-%m-%d')
    stock_data.set_index('date', inplace=True)
    stock_data = stock_data.sort_index(0)
    if is_debug:
        print(stock_data.head(10))
        print(stock_data.tail(10))
    
    #
    # Convert Daily Data to Monthly Data
    #
    
    # Weekly='W', Monthly='M', Quarterly='Q', 5 Minutes='5min', 12 Days='12D'
    period_type = 'M'
    period_stock_data = stock_data.resample(period_type).first()
    if is_debug:
        print(period_stock_data.head(10))
        print(period_stock_data.tail(10))
    
    period_stock_data['open']   = stock_data['open'].resample(period_type).first()
    period_stock_data['high']   = stock_data['high'].resample(period_type).max()
    period_stock_data['close']  = stock_data['close'].resample(period_type).last()
    period_stock_data['low']    = stock_data['low'].resample(period_type).min()
    period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()
    period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()
    if is_debug:
        print(period_stock_data.head(10))
        print(period_stock_data.tail(10))
    
    #
    # Calculate Monthly Return Statistics
    #
    s_date = dt.datetime.strptime(start_date,'%Y-%m-%d')
    e_date = dt.datetime.strptime(end_date,'%Y-%m-%d')
    if is_debug:
        print(s_date.year, s_date.month, s_date.day)
        print(e_date.year, e_date.month, e_date.day)
    
    period_stock_data_number = len(period_stock_data)
    if is_debug:
        print('period_stock_data_number =', period_stock_data_number)
    period_stock_return = [0 for ele in range(period_stock_data_number)]
    period_stock_date = [dt.date for ele in range(period_stock_data_number)]
    
    for index in range(period_stock_data_number):
        if index == 0:
            current_open = period_stock_data['open'][index]
        else:
            current_open = period_stock_data['close'][index-1]
        current_close = period_stock_data['close'][index]
        ratio = current_close / current_open - 1
        period_stock_return[index] = ratio
        period_stock_date[index] = period_stock_data.index[index].date()
    
    #
    # Pack Statistics into DataFrame
    #
    # Init dataframe
    if (i == 0):
        df = pd.DataFrame(np.random.randn(stock_number, period_stock_data_number), index = stock_ids, columns = period_stock_date)
    # Fill the data for the current stock        
    for index in range(period_stock_data_number):
        df.loc[stock_id, period_stock_date[index]] = period_stock_return[index]

#
# Output Statistics
# 
if is_debug:
    print(df)

# Rebase based on benchmark
if (bench_index != -1):
    if (bench_index < 0) or (bench_index >= stock_number):
        print('Invalid bench_index', bench_index)
        raise SystemExit
        
    bench_id = stock_ids[bench_index]
    for stock_id in stock_ids:
        if (stock_id != bench_id): # Be careful NOT to modify bench_id data until all subtraction are done!!!
            for index in range(period_stock_data_number):
                df.loc[stock_id, period_stock_date[index]] -= df.loc[bench_id, period_stock_date[index]]
    for index in range(period_stock_data_number):
        df.loc[bench_id, period_stock_date[index]] = 0

df.to_excel(path_datacenter+bench_id+'_RelativeStrength'+'.xlsx')






























