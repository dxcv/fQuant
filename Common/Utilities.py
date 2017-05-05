# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:12:25 2017

@author: freefrom
"""

import os
import datetime as dt
import pandas as pd
import numpy as np
import Common.GlobalSettings as gs
import Common.Constants as c

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
    if gs.is_debug:
        print('Save File: %s' % path+file)

# Wrapper of DataFrame.read_csv() with Default Settings
def read_csv(fullpath, index_col=None, encoding=gs.encoding):
    if gs.is_debug:
        print('Read File: %s' % fullpath)
    if not hasFile(fullpath):
        return None
    else:
        return pd.read_csv(fullpath, index_col=index_col, encoding=encoding)

# Wrapper of matplotlib.pyplot.savefig() Function
def saveFigure(plt, path, file):
    ensurePath(path)
    plt.savefig(path+file)
    if gs.is_debug:
        print('Save Figure: %s' % path+file)

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

# Return the Date in type of datetime.date(YYYY-mm-dd) of a Given Quarter (1-4) of a Given Year
def quarterDate(year, quarter):
    return dt.date(year, quarterEndMonth(quarter), quarterEndDay(quarter))

# Return the Date in type of str('YYYY-mm-dd') of a given quarter (1-4) of a given year
def quarterDateStr(year, quarter):
    return str(dt.date(year, quarterEndMonth(quarter), quarterEndDay(quarter)))
#    return str(year)+'-'+str(quarterEndMonth(quarter)).zfill(2)+'-'+str(quarterEndDay(quarter)).zfill(2)

def today():
    return dt.datetime.today().date()

def tomorrow():
    date = dt.datetime.now() + dt.timedelta(days = 1)
    return date.date()

def yesterday():
    date = dt.datetime.now() + dt.timedelta(days = -1)
    return date.date()

def yearOfToday():
    return dt.datetime.today().year

def monthOfToday():
    return dt.datetime.today().month

def dayOfToday():
    return dt.datetime.today().day

def hourOfToday():
    return dt.datetime.today().hour

def dayLastYear():
    return today() + dt.timedelta(-365)

def dayLastWeek(days=-7):
    return today() + dt.timedelta(days)

# Return quarter of a given date
def quarterOfDate(date):
    return int((date.month-1) / 3) + 1

# Return quarter end date of a given date
def quarterEndOfDay(date):
    quarter = quarterOfDate(date)
    return dt.date(date.year, quarterEndMonth(quarter), quarterEndDay(quarter))

# Break start date and end date on a yearly basis
def breakByYear(start_date, end_date):
    start_year = start_date[0:4]
    end_year = end_date[0:4]
    first_day = '-01-01'
    last_day = '-12-31'
    dates = [start_date, start_year+last_day]
    for year in range(int(start_year)+1,int(end_year)):
        dates.append(str(year)+first_day)
        dates.append(str(year)+last_day)
    if end_year > start_year:
        dates.append(end_year+first_day)
        dates.append(end_date)
    return dates

###############################################################################

#
# Stock Utilities
#

# Return Formated Date (from YYYYmmdd to YYYY-mm-dd)
def formatDateYYYYmmddInt64(date):
    try:
        d = pd.to_datetime(date, format='%Y%m%d')
    except:
        return c.magic_date
    #return '%(year)04d-%(month)02d-%(day)02d' % {'year':d.year, 'month':d.month, 'day':d.day}
    return str(dt.date(d.year, d.month, d.day))

# Return Formated Date (from YYYYmmdd to YYYY-mm-dd)
def formatDateYYYYmmddStr(date):
    try:
        d = dt.datetime.strptime(date, '%Y%m%d')
    except:
        return c.magic_date_YYYYmmdd_str
    return d.strftime('%Y-%m-%d')

# Return Date (from string YYYY-mm-dd)
def dateFromStr(date):
    if isValidDate(date):
        date = pd.to_datetime(date, format='%Y-%m-%d')
        return dt.date(date.year, date.month, date.day)
    else:
        return None

# Return Next Day (from string YYYY-mm-dd)
def nextDayFromStr(date):
    if isValidDate(date):
        date = pd.to_datetime(date, format='%Y-%m-%d')
        next_day = date + dt.timedelta(days = 1)
        return dt.date(next_day.year, next_day.month, next_day.day)
    else:
        return None

# Return Previous Day (from string YYYY-mm-dd)
def prevDayFromStr(date):
    if isValidDate(date):
        date = pd.to_datetime(date, format='%Y-%m-%d')
        prev_day = date + dt.timedelta(days = -1)
        return dt.date(prev_day.year, prev_day.month, prev_day.day)
    else:
        return None

# Return String (from datetime.date)
def dateToStr(date):
    return str(date)

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

# Return Stock ID
def stockID(stock_id):
    return str(stock_id).zfill(6)

###############################################################################

#
# DataFrame Utilities
#

def createDataFrame(row_number, columns):
    column_number = len(columns)

    # Init all elements to NaN
    data_init = np.random.randn(row_number * column_number)
    for i in range(row_number * column_number):
        data_init[i] = np.nan

    # Create DataFrame
    df = pd.DataFrame(data_init.reshape(row_number, column_number),
                       index = None, columns = columns)
    return df

###############################################################################
#
# Misc Utilities
#

def isNoneOrEmpty(df):
    return (df is None) or (len(df) == 0)

def isValidDate(date):
    return date != c.magic_date

def stockFileName(stock_id, is_index):
    index = 'Index_' if is_index==True else 'Stock_'
    return index+stock_id
















