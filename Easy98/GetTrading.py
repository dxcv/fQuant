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
        u.to_csv(df, c.path_dict['lshq'], c.file_dict['lshq'] % stock_id)

def loadDailyHFQ(stock_id):
    df = u.read_csv(c.fullpath_dict['lshq'] % stock_id)
    return df

def validDailyHFQ(stock_id, force_update):
    if force_update == True:
        return False

    else:
        return u.hasFile(c.fullpath_dict['lshq'] % stock_id)
