# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 18:10:01 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

import datetime as dt
from GetFundamental import getStockBasics, loadStockBasics, validStockBasics
from GetFundamental import getFinanceSummary, loadFinanceSummary, validFinanceSummary
from GetTrading import getDailyHFQ, loadDailyHFQ, validDailyHFQ
import Utilities as u
import Constants as c
import GlobalSettings as gs

#
# Update Data Center Parameters
#
date_start = dt.date(2005, 1, 1)
date_end = u.today()
update_basics = False
update_price = False
update_financesummary = False

force_update = False

###############################################################################

#
# Update Data Center Functions
#
def updateStockBasics(force_update = True):
    # Chec if valid date file already exists
    if not validStockBasics(force_update):
        getStockBasics()
        cleanStockBasics()

def cleanStockBasics():
    basics = loadStockBasics()
    print(basics.head(10))

    # Format columns
    basics['timeToMarket'] = basics['timeToMarket'].map(u.formatDateYYYYmmddInt64)
    if gs.is_debug:
        basics_number = len(basics)
        for i in range(basics_number):
            if basics.loc[i,'timeToMarket'] == c.magic_date:
                print(i, type(basics.loc[i,'timeToMarket']),
                      basics.loc[i,'timeToMarket'], basics.loc[i,'code'])

    # Filter out invalid timeToMarket stocks
    basics_nottm = basics[basics.timeToMarket == c.magic_date]

    # Save to CSV File
    u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])
    u.to_csv(basics_nottm, c.path_dict['basics'], c.file_dict['basics_nottm'])

def updatePrice(force_update = True):
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    basics_number = len(basics)
    for i in range(basics_number):
        stock_id = u.stockID(basics.loc[i,'code'])
        is_index = False
        time_to_market = u.dateFromStr(basics.loc[i,'timeToMarket'])

        # Ignore No TTM Stocks (No Yet On the Market)
        if time_to_market is None:
            continue;

        # Check if valid data file already exists
        if not validDailyHFQ(stock_id, force_update):
            getDailyHFQ(stock_id=stock_id, is_index=is_index, date_start=time_to_market,
                        date_end=date_end, time_to_market=time_to_market)
            print('Update Price:', stock_id)

def updateFinanceSummary(force_update = True):
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    basics_number = len(basics)
    for i in range(basics_number):
        stock_id = u.stockID(basics.loc[i,'code'])
        time_to_market = u.dateFromStr(basics.loc[i,'timeToMarket'])

        # Ignore No TTM Stocks (No Yet On the Market)
        if time_to_market is None:
            continue;

        # Check if valid data file already exists
        if not validFinanceSummary(stock_id, force_update):
            getFinanceSummary(stock_id)
            print('Update Finance Summary:', stock_id)

###############################################################################

#
# Iteratively Update Databases
#
if update_basics:
    updateStockBasics(force_update)

if update_price:
    updatePrice(force_update)

if update_financesummary:
    updateFinanceSummary(force_update)

















