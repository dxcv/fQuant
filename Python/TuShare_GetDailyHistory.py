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
stock_ids  = ['000916']
is_indexs  = [True]
start_date = '2007-07-02'
end_date   = '2016-06-13'
path_datacenter = '../DataCenter/'

stock_number = len(stock_ids)
for i in range(stock_number):
    #
    # Fetch Stock Data
    #
    stock_id = stock_ids[i]
    is_index = is_indexs[i]
    df = ts.get_h_data(stock_id, index=is_index, start=start_date, end=end_date, autype=None)
    df = df.sort_index(0)
    number_df = len(df)
    if number_df == 0:
        raise SystemExit
    #print(df.head(10))
    
    #
    # Save to CSV File
    #
    df.to_csv(path_datacenter+stock_id+'.csv')