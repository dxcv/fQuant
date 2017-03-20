# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:55:29 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Trading import get_daily_hfq
import GlobalSettings as gs
import Constants as c
import Utilities as u

def getDailyHFQ(stock_id, is_index, date_start, date_end, time_to_market = None):
    # Download
    df = get_daily_hfq(stock_id=stock_id, is_index=is_index, date_start=date_start, 
                       date_end=date_end, time_to_market=time_to_market)
    df.sort_index(ascending=True,inplace=True) # date is set to index
    if gs.is_debug:
        print(df.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(df):
        u.to_csv(df, c.path_dict['lshq'], c.file_dict['lshq'] % u.stockFileName(stock_id, is_index))

def loadDailyHFQ(stock_id, is_index):
    fullpath = c.fullpath_dict['lshq'] % u.stockFileName(stock_id, is_index)

    # Ensure data file is available
    if not u.hasFile(fullpath):
        print('Require LSHQ of %s!' % u.stockFileName(stock_id, is_index))
        return None

    # Read data file
    df = u.read_csv(fullpath)
    return df

def validDailyHFQ(stock_id, is_index, force_update):
    if force_update == True:
        return False

    else:
        return u.hasFile(c.fullpath_dict['lshq'] % u.stockFileName(stock_id, is_index))