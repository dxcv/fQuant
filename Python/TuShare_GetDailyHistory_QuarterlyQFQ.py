# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:34:06 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import pandas as pd
import numpy as np
import datetime as dt

#
# Get Daily History Parameters
#
stock_ids  = ['300059','600036']
is_indexs  = [False,False]
year_start = 2005
year_end   = 2016
path_datacenter = '../DataCenter/'

#
# Utility Functions
#
def getQuarterStartDay(quarter):
    return 1

def getQuarterEndDay(quarter):
    if quarter == 1 or quarter == 4:
        return 31
    else:
        return 30

def getQuarterStartMonth(quarter):
    return (quarter-1)*3 + 1

def getQuarterEndMonth(quarter):
    return quarter*3

def getQuarterDate(year, quarter):
    return str(year)+'-'+str(getQuarterEndMonth(quarter))+'-'+str(getQuarterEndDay(quarter))

#
# Load Stock Basics
#
basics = pd.read_csv(path_datacenter+'StockBasics'+'.csv',encoding='utf-8')
basics.set_index('code', inplace=True)
print(basics.head(10))

# Check Start Date and End Date
if year_end < year_start:
    print('Start year should be no later than end year!')
    raise SystemExit

# Prepare Daily Data Frame
data_columns = ['open','high','close','low','volume','amount']
data_columns_number = len(data_columns)
data_index = []
for year in range(year_start, year_end+1):
    for quarter in range(1, 5):
        quarter_date = getQuarterDate(year, quarter)
        data_index.append(quarter_date)
print(data_index)
data_index_number = len(data_index)

# Init all elements to NaN
data_init = np.random.randn(data_index_number * data_columns_number)
for i in range(data_index_number * data_columns_number):
    data_init[i] = np.nan
df = pd.DataFrame(data_init.reshape(data_index_number, data_columns_number),
                  index = data_index, columns = data_columns)
df.index.names = ['date']

#
# Iterate Over All Stocks
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    is_index = is_indexs[i]

    # Extract Stock Time-to-Market
    timeToMarket = basics.loc[int(stock_id), 'timeToMarket'] #上市日期YYYYMMDD
    print(timeToMarket)

    date = pd.to_datetime(timeToMarket, format='%Y%m%d')
    print(date.year, date.month, date.day)
    date_timeToMarket = dt.date(date.year, date.month, date.day)

    # Break start date and end date into quarters
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            quarter_start = dt.date(year, getQuarterStartMonth(quarter), getQuarterStartDay(quarter))
            quarter_end = dt.date(year, getQuarterEndMonth(quarter), getQuarterEndDay(quarter))

            if quarter_start < date_timeToMarket:
                quarter_start = date_timeToMarket

            if quarter_start > quarter_end:
                continue

            # Fetch HFQ daily data for each quarter
            # Use HFQ and FQ_Factor to calculate QFQ daily data
            stock_data = ts.get_h_data(stock_id, index=is_index,
                                       start=quarter_start.strftime('%Y-%m-%d'),
                                       end=quarter_end.strftime('%Y-%m-%d'),
                                       autype='hfq', drop_factor=False)
            # Handle stop-trading quarter
            if len(stock_data) == 0: # stock_data == None or 
                index = getQuarterDate(year, quarter)
                for column in ['open','high','close','low','volume','amount']:
                    df.loc[index,column] = np.nan
            else: # Normal case - at least one trading day in the quarter
                print(stock_data.head(5))
    
                # Resample to quarterly based data
                period_type = 'Q'
                period_stock_data = stock_data.resample(period_type).first()
                if len(period_stock_data) == 0: # Ignore empty quarterly data
                    continue
                print(len(period_stock_data))
    
                period_stock_data['open']   = stock_data['open'].resample(period_type).first()
                period_stock_data['high']   = stock_data['high'].resample(period_type).max()
                period_stock_data['close']  = stock_data['close'].resample(period_type).last()
                period_stock_data['low']    = stock_data['low'].resample(period_type).min()
                period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()
                period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()
                period_stock_data['factor'] = stock_data['factor'].resample(period_type).last()
    
                # Fill data frame
                index = getQuarterDate(year, quarter)
                fq_factor = period_stock_data['factor'][0]
                for column in ['open','high','close','low']:
                    df.loc[index,column] = period_stock_data[column][0] / fq_factor
                df.loc[index, 'volume'] = period_stock_data['volume'][0] # Not touch it
                df.loc[index, 'amount'] = period_stock_data['amount'][0]

    # Save to CSV File
    df.to_csv(path_datacenter+'StockData_QuarterlyQFQ_'+stock_id+'.csv',encoding='utf-8')
























