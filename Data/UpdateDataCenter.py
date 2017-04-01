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
from GetFundamental import getFinanceSummary, validFinanceSummary
from GetTrading import getDailyHFQ, validDailyHFQ
from GetCommodity import getCommodityPrice, extractCommodityPrice, loadCommodityList
from GetClassifying import getIndustrySina, getConceptSina, getArea
from GetClassifying import getSME, getGEM, getST
from GetClassifying import getHS300, getSZ50, getZZ500
from GetClassifying import getTerminated, getSuspended, getCXG, loadCXG
from GetClassifying import extractIndustrySina, extractConceptSina, extractArea
from GetClassifying import getStockList, loadStockList

import sys
sys.path.append('..')
import Common.Utilities as u
import Common.Constants as c
import Common.GlobalSettings as gs

#
# Update Data Center Parameters
#
date_start = dt.date(2005, 1, 1)
date_end = u.today()
date_cxg = '2016-01-01'

###############################################################################

#
# Update Data Center Functions
#
def updateStockBasics():
    getStockBasics()
    cleanStockBasics()

def cleanStockBasics():
    basics = loadStockBasics()
    print(basics.head(10))

    # Format columns
    basics['code'] = basics['code'].map(lambda x:str(x).zfill(6))
    basics['timeToMarket'] = basics['timeToMarket'].map(u.formatDateYYYYmmddInt64)
    if gs.is_debug:
        basics_number = len(basics)
        for i in range(basics_number):
            if basics.loc[i,'timeToMarket'] == c.magic_date:
                print(i, type(basics.loc[i,'timeToMarket']),
                      basics.loc[i,'timeToMarket'], basics.loc[i,'code'])

    # Filter out invalid timeToMarket stocks
    basics_nottm = basics[basics.timeToMarket == c.magic_date]
    basics = basics[basics.timeToMarket != c.magic_date]

    # Save to CSV File
    u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])
    u.to_csv(basics_nottm, c.path_dict['basics'], c.file_dict['basics_nottm'])

def updatePriceStock(incremental = False):
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
        getDailyHFQ(stock_id=stock_id, is_index=False, date_start=time_to_market,
                    date_end=date_end, time_to_market=time_to_market, incremental=incremental)
        print('Update Price:', stock_id)

def updatePriceIndex(incremental = False):
    for index_id in c.index_list:
        getDailyHFQ(stock_id=index_id, is_index=True, date_start=date_start,
                    date_end=date_end, time_to_market=None, incremental=incremental)
        print('Update Price:', index_id)

def updatePriceCXG(incremental = False):
    # Check pre-requisite
    cxg = loadCXG()
    if u.isNoneOrEmpty(cxg):
        print('Need to have CXG data!')
        raise SystemExit

    # Iterate over all CXG stocks
    cxg_number = len(cxg)
    print('Number of CXG:',cxg_number)
    for i in range(cxg_number):
        stock_id = u.stockID(cxg.ix[i,'code'])
        time_to_market = u.dateFromStr(cxg.loc[i,'timeToMarket'])
        getDailyHFQ(stock_id=stock_id, is_index=False, date_start=time_to_market,
                    date_end=date_end, time_to_market=time_to_market, incremental=incremental)
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

        # Check if valid data file already exists
        if not validFinanceSummary(stock_id, force_update):
            getFinanceSummary(stock_id)
            print('Update Finance Summary:', stock_id)

def updateClassifying():
    getIndustrySina()
    getConceptSina()
    getArea()
    getSME()
    getGEM()
    getST()
    getHS300()
    getSZ50()
    getZZ500()
    getCXG(date_cxg)
    getTerminated()
    getSuspended()
    extractIndustrySina()
    extractConceptSina()
    extractArea()

def updateCommodity(force_update = True):
    com_list = loadCommodityList()
    com_number = len(com_list)
    for i in range(com_number):
        code = com_list.iloc[i,1]
        getCommodityPrice(code)
        extractCommodityPrice(code,'报价机构')

###############################################################################

#
# Update Data Center Entries
#

# Full Weekly Update
def updateWeekly():
    updateStockBasics()
    updatePriceStock()
    updatePriceIndex()
    updateFinanceSummary()
    updateClassifying()
    updateCommodity()

# Incremental Daily Update
def updateDaily():
    updateStockBasics()
    updatePriceStock(True)

# Incremental Update for CXG
def updateCXG():
    updateStockBasics()
    getCXG(date_cxg)
    updatePriceCXG(True)

def updateStock(stock_id, date_start, date_end):
    getDailyHFQ(stock_id=stock_id, is_index=False, date_start=date_start,
                date_end=date_end)
    print('Update Price:', stock_id)

###############################################################################

#updateCXG()
#updateStock('002340', date_start, date_end)
updateDaily()