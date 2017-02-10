# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:12:25 2017

@author: freefrom
"""

import os
import datetime as dt
import pandas as pd
import GlobalSettings as gs
import Constants as c

###############################################################################

#
# File Utilities
#

# If a Given File with Full Path Exists
def hasFile(full_path):
    return os.path.isfile(full_path)

# If a Given Path Exists
def hasPath(path):
    return os.path.exists(path)

# Create Folder if Non-Exists
def ensurePath(path):
    if not hasPath(path):
        os.makedirs(path)

# Wrapper of DataFrame.to_csv() with Additional Folder Checks
def to_csv(df, path, file, encoding=gs.encoding):
    ensurePath(path)
    df.to_csv(path+file, encoding=encoding)

# Wrapper of DataFrame.read_csv() with Default Settings
def read_csv(fullpath, encoding=gs.encoding):
    return pd.read_csv(fullpath, encoding=encoding)

###############################################################################

#
# Date Utilities
#

# Return the Start Day of a Given Quarter (1-4)
def quarterStartDay(quarter):
    return 1

# Return the End Day of a Given Quarter (1-4)
def quarterEndDay(quarter):
    if quarter == 1 or quarter == 4:
        return 31
    else:
        return 30

# Return the Start Month of a Given Quarter (1-4)
def quarterStartMonth(quarter):
    return (quarter-1)*3 + 1

# Return the End Month of a Given Quarter (1-4)
def quarterEndMonth(quarter):
    return quarter*3

# Return the Date (YYYY-mm-dd) of a Given Quarter (1-4) of a Given Year
def quarterDate(year, quarter):
    return str(year)+'-'+str(quarterEndMonth(quarter)).zfill(2)+'-'+str(quarterEndDay(quarter)).zfill(2)

###############################################################################

#
# Stock Utilities
#

# Return Formated Date (from YYYYmmdd to YYYY-mm-dd)
def formatDateYYYYmmddInt64(date):
    try:
        d = pd.to_datetime(date, format='%Y%m%d')
    except:
        return c.magic_date_YYYYmmdd_str
    return '%(year)04d-%(month)02d-%(day)02d' % {'year':d.year, 'month':d.month, 'day':d.day}

# Return Formated Date (from YYYYmmdd to YYYY-mm-dd)
def formatDateYYYYmmddStr(date):
    try:
        d = dt.datetime.strptime(date, '%Y%m%d')
    except:
        return c.magic_date_YYYYmmdd_str
    return d.strftime('%Y-%m-%d')

#
## Load Stock Basics CSV File and Return DataFrame
#def loadStockBasics(path_basics = cd.path_datacenter, file_basics = cd.file_stockbasics):
#    stock_basics = None
#    if fu.hasFile(path = path_basics, file = file_basics):
#        stock_basics = pd.read_csv(path_basics + file_basics, encoding='utf-8')
#        stock_basics.set_index('code', inplace=True)
#        if cd.is_debug:
#            print(stock_basics.head(10))
#    return stock_basics

# Extract Stock Time-to-Market from Stock Basics Data
def timeToMarket(stock_basics, stock_id):
    d = None
    if (not stock_basics is None) and (stock_id in stock_basics.index): # Assume 'code' is index
        date = stock_basics.loc[stock_id, 'timeToMarket'] #上市日期YYYYMMDD
        if gs.is_debug:
            print(date)

        date = pd.to_datetime(date, format='%Y%m%d')
        if gs.is_debug:
            print(date.year, date.month, date.day)
        d = dt.date(date.year, date.month, date.day)
    return d

# Extract Stock Time-to-Market from Sector Stocks Data
def timeToMarket2(sector_stocks, stock_id):
    d = None
    if (not sector_stocks is None) and (stock_id in sector_stocks.index): # Assume 'code' is index
        date = sector_stocks.loc[stock_id, 'timeToMarket'] #上市日期YYYYMMDD
        if gs.is_debug:
            print(date)

        date = pd.to_datetime(date, format='%Y%m%d')
        if gs.is_debug:
            print(date.year, date.month, date.day)
        d = dt.date(date.year, date.month, date.day)
    return d

###############################################################################





















