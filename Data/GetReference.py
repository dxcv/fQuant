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

def getRZRQMarketSH(date_start, date_end):
    # Download RZRQ Data of SH Market
    rzrq_sh = get_rzrq_sh(date_start, date_end)

    # Process RZRQ Market Data
    rzrq_sh.set_index('date',inplace=True)
    rzrq_sh.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sh.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sh):
        u.to_csv(rzrq_sh, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Market_SH')

def getRZRQMarketSZ(date_start, date_end):
    # Download RZRQ Data of SZ Market
    rzrq_sz = pd.DataFrame()
    dates = u.breakByYear(date_start, date_end)
    print(dates)
    dates_number = int(len(dates) / 2)
    for i in range(dates_number):
        rzrq = get_rzrq_sz(dates[i*2], dates[i*2+1])
        if i == 0:
            rzrq_sz = pd.DataFrame.copy(rzrq)
        else:
            rzrq_sz = pd.concat([rzrq_sz, rzrq])

    # Process RZRQ Market Data
    rzrq_sz.set_index('date',inplace=True)
    rzrq_sz.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sz.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sz):
        u.to_csv(rzrq_sz, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Market_SZ')

def mergeRZRQMarketSZ(files_number):
    rzrq_sz = pd.DataFrame()
    for index in range(files_number):
        rzrq = u.read_csv(c.fullpath_dict['rzrq'] % ('Market_SZ_%s'%index))
        if index == 0:
            rzrq_sz = pd.DataFrame.copy(rzrq)
        else:
            rzrq_sz = pd.concat([rzrq_sz, rzrq])
    rzrq_sz.set_index('date',inplace=True)
    rzrq_sz.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sz.head(10))
    if not u.isNoneOrEmpty(rzrq_sz):
        u.to_csv(rzrq_sz, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Market_SZ')

def mergeRZRQMarket():
    rzrq_sh = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SH')
    rzrq_sz = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SZ')
    rzrq = pd.merge(rzrq_sh, rzrq_sz, how='inner', on='date')
    # Combine data from both market
    rzrq_columns = ['rzye', 'rzmre', 'rqyl', 'rqylje', 'rqmcl', 'rzrqye'] 
    for column in rzrq_columns:
        rzrq[column] = 0.0
    rzrq_number = len(rzrq)
    for row in range(rzrq_number):
        for col in rzrq_columns:
            rzrq.ix[row, col] = rzrq.ix[row, col+'_sh'] + rzrq.ix[row, col+'_sz']
    rzrq.set_index('date',inplace=True)
    rzrq.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq.head(10))
    if not u.isNoneOrEmpty(rzrq):
        u.to_csv(rzrq, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Market_Total')

###############################################################################

def getRZRQDetailsSH():
    # Download RZRQ Stock Data of SH Market
    rzrq_sh_details = pd.DataFrame()
    rzrq_sh = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SH')
    date_number = len(rzrq_sh)
    for i in range(date_number):
        date = rzrq_sh.ix[i,'date']
        rzrq = get_rzrq_sh_details(date, date)
        print(rzrq.head(10))
        if i == 0:
            rzrq_sh_details = pd.DataFrame.copy(rzrq)
        else:
            rzrq_sh_details = pd.concat([rzrq_sh_details, rzrq])
        print(rzrq_sh_details.head(10))
        rzrq.set_index('date', inplace=True)
        if not u.isNoneOrEmpty(rzrq):
            u.to_csv(rzrq, c.path_dict['rzrq'], c.file_dict['rzrq'] % ('Details_SH_%s'%date))

    # Process RZRQ Stock Data of SH Market
    rzrq_sh_details.set_index('date', inplace=True)
    rzrq_sh_details.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sh_details.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sh_details):
        u.to_csv(rzrq_sh_details, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Details_SH')

def getRZRQDetailsSZ():
    # Download RZRQ Stock Data of SZ Market
    rzrq_sz_details = pd.DataFrame()
    rzrq_sz = u.read_csv(c.fullpath_dict['rzrq'] % 'Market_SZ')
    date_number = len(rzrq_sz)
    for i in range(date_number):
        date = rzrq_sz.ix[i,'date']
        rzrq = get_rzrq_sz_details(date)
        if i == 0:
            rzrq_sz_details = pd.DataFrame.copy(rzrq)
        else:
            rzrq_sz_details = pd.concat([rzrq_sz_details, rzrq])
        rzrq.set_index('date', inplace=True)
        if not u.isNoneOrEmpty(rzrq):
            u.to_csv(rzrq, c.path_dict['rzrq'], c.file_dict['rzrq'] % ('Details_SZ_%s'%date))

    # Process RZRQ Stock Data of SZ Market
    rzrq_sz_details.set_index('date', inplace=True)
    rzrq_sz_details.sort_index(ascending=True,inplace=True)
    if gs.is_debug:
        print(rzrq_sz_details.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(rzrq_sz_details):
        u.to_csv(rzrq_sz_details, c.path_dict['rzrq'], c.file_dict['rzrq'] % 'Details_SZ')

###############################################################################

def extractRZRQDetails(market = 'SH'):
    rzrq_details = u.read_csv(c.fullpath_dict['rzrq'] % ('Details_%s' % market))
    stocks = pd.DataFrame({'code':rzrq_details['code']})
    stocks.drop_duplicates(inplace=True)
    stocks.set_index('code',inplace=True)
    stocks_number = len(stocks)
    print('RZRQ Stock Number:', stocks_number)
    for i in range(stocks_number):
        stock_id = stocks.index[i]
        rzrq = rzrq_details[rzrq_details['code'] == stock_id]
        if not u.isNoneOrEmpty(rzrq):
            rzrq.set_index('date',inplace=True)
            rzrq.sort_index(ascending=True,inplace=True)
            rzrq['code'] = rzrq['code'].map(lambda x:str(x).zfill(6))
            # Handle Missing Columns
            if market == 'SH':
#                rzrq['rqylje'] = 
                rzrq['rzrqye'] = rzrq['rzye'] + rzrq['rqylje']
#            elif market == 'SZ':
#                rzrq['rzche'] = 
#                rzrq['rqchl'] = 
            u.to_csv(rzrq, c.path_dict['rzrq'], c.file_dict['rzrq'] % ('Details_%s_%06d' % (market, stock_id)))

###############################################################################

def getRZRQMarket(date_start, date_end):
    getRZRQMarketSH(date_start,date_end)
    getRZRQMarketSZ(date_start,date_end)
    mergeRZRQMarket()

def getRZRQDetails(date_start, date_end):
    getRZRQDetailsSH()
    getRZRQDetailsSZ()
    extractRZRQDetails('SH')
    extractRZRQDetails('SZ')