# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:35:52 2017

@author: freefrom
"""

from HistoricalPrice import calc_qfq
from HistoricalPE import calc_hpe
import GlobalSettings as gs
import Utilities as u
import Constants as c

def calcQFQ(stock_id, period):
    # Calculate QFQ DataFrame
    df = calc_qfq(stock_id, period)
    if gs.is_debug:
        print(df.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(df):
        u.to_csv(df, c.path_map_qfq[period], c.file_map_qfq[period] % stock_id)

def loadQFQ(stock_id, period):
    df = u.read_csv(c.fullpath_map_qfq[period] % stock_id)
    return df

def calcHPE(stock_id, period):
    # Calculate HPE DataFrame
    df = calc_hpe(stock_id, period)
    if gs.is_debug:
        print(df.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(df):
        u.to_csv(df, c.path_map_hpe[period], c.file_map_hpe[period] % stock_id)

def loadHPE(stock_id, period):
    df = u.read_csv(c.fullpath_map_hpe[period] % stock_id)
    return df

