# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 16:34:28 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts

#
# Get Daily History Parameters
#
stock_id   = '000300'
is_index   = True
start_date = '2005-04-08'
end_date   = '2016-12-30'

#
# Fetch Stock Data
#
df = ts.get_stock_basics()
#start_date = df.ix[stock_id]['timeToMarket'] #上市日期YYYYMMDD

df = ts.get_h_data(stock_id, index=is_index, start=start_date, end=end_date, autype=None)
df = df.sort_index(0)
number_df = len(df)
if number_df == 0:
    raise SystemExit
#print(df.head(10))

#
# Save to CSV File
#
df.to_csv('D:/DataCenter/PythonData/'+stock_id+'.csv')