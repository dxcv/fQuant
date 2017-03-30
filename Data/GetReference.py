# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:30:03 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Reference import get_rzrq_sh, get_rzrq_sz
from Reference import get_rzrq_sh_details, get_rzrq_sz_details
import pandas as pd
import sys
sys.path.append('..')
import Common.GlobalSettings as gs
import Common.Constants as c
import Common.Utilities as u

def getRZRQMarketSH(start_date, end_date):
    # Download RZRQ Data of SH Market
    rzrq_sh = get_rzrq_sh(start_date, end_date)

    # Process RZRQ Market Data
    rzrq_sh.set_index('date',inplace=True)
    rzrq_sh.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sh.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sh):
        u.to_csv(rzrq_sh, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Market_SH')

def getRZRQMarketSZ(start_date, end_date, index):
    # Download RZRQ Data of SZ Market
    rzrq_sz = get_rzrq_sz(start_date, end_date)

    # Process RZRQ Market Data
    rzrq_sz.set_index('date',inplace=True)
    rzrq_sz.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sz.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sz):
        u.to_csv(rzrq_sz, c.path_dict['rzrq'], c.file_dict['rzrq'] % ('Market_SZ_%s'%index))

def getRZRQDetailsSH(start_date, end_date):
    # Download RZRQ Stock Data of SH Market
    rzrq_sh_details = get_rzrq_sh_details(start_date, end_date)

    # Process RZRQ Stock Data of SH Market
    rzrq_sh_details.set_index('date', inplace=True)
    rzrq_sh_details.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sh_details.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sh_details):
        u.to_csv(rzrq_sh_details, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Details_SH')

def getRZRQDetailsSZ(start_date, end_date):
    # Download RZRQ Stock Data of SZ Market
    rzrq_sz = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SZ')
    date_number = len(rzrq_sz)
    for i in range(date_number):
        date = rzrq_sz.ix[i,'date']
        rzrq_sz_details = get_rzrq_sz_details(date)
        rzrq_sz_details.set_index('date', inplace=True)
        if gs.is_debug:
            print(rzrq_sz_details.head(10))
        if not u.isNoneOrEmpty(rzrq_sz_details):
            u.to_csv(rzrq_sz_details, c.path_dict['rzrq'], c.file_dict['rzrq'] % ('Details_SZ_'+date))

def mergeRZRQMarket():
    rzrq_sh = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SH')
    rzrq_sz = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SZ')
    rzrq = pd.merge(rzrq_sh, rzrq_sz, how='inner', on='date')
    rzrq.set_index('date',inplace=True)
    rzrq.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq.head(10))
    if not u.isNoneOrEmpty(rzrq):
        u.to_csv(rzrq, c.path_dict['lshq'], c.file_dict['lshq'] % 'Market_Total')

###############################################################################

date_start = '2010-03-31'
date_end = '2017-03-28'
#getRZRQMarketSH(date_start,date_end)
dates = u.breakByYear(date_start, date_end)
print(dates)
dates_number = int(len(dates) / 2)
for i in range(dates_number):
    getRZRQMarketSZ(dates[i*2],dates[i*2+1],i)
#mergeRZRQMarket()