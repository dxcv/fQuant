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
        path = c.path_dict['qfq'] % period
        file = c.file_dict['qfq'] % (period, stock_id)
        u.to_csv(df, path, file)

def loadQFQ(stock_id, period):
    path = c.path_dict['qfq'] % period
    file = c.file_dict['qfq'] % (period, stock_id)

    df = u.read_csv(path+file)
    return df

def calcHPE(stock_id, period, ratio):
    # Calculate HPE DataFrame
    df = calc_hpe(stock_id, period, ratio)
    if gs.is_debug:
        print(df.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(df):
        key = 'hpe' if ratio == 'PE' else 'hep'
        path = c.path_dict[key] % period
        file = c.file_dict[key] % (period, stock_id)
        u.to_csv(df, path, file)

def loadHPE(stock_id, period, ratio):
    key = 'hpe' if ratio == 'PE' else 'hep'
    path = c.path_dict[key] % period
    file = c.file_dict[key] % (period, stock_id)

    df = u.read_csv(path+file)
    return df

