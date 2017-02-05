# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:34:06 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
from QuarterlyQFQ import get_quarterly_qfq
import ConstantData as cd
import StockUtility as su

#
# Get Quarterly QFQ Parameters
#
stock_ids  = ['300059','600036','000002','002024']
is_indexs  = [False,False,False,False]
year_start = 2005
year_end   = 2016

#
# Load Stock Basics
#
basics = su.loadStockBasics()

#
# Iterate Over All Stocks
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    is_index = is_indexs[i]

    # Extract Stock Time-to-Market
    date_timeToMarket = su.timeToMarket(stock_basics = basics, stock_id = stock_id)
    df = get_quarterly_qfq(stock_id = stock_id, is_index = is_index, year_start = year_start,
                           year_end = year_end, time_to_market = date_timeToMarket)

    # Save to CSV File
    df.to_csv(cd.path_datacenter + (cd.file_quarterlyqfq % stock_id), encoding='utf-8')

























