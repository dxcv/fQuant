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
from CalcIndicators import calcQFQ, calcHPE
from GetClassifying import getIndustrySina, getConceptSina, getArea
from GetClassifying import getSME, getGEM, getST
from GetClassifying import getHS300, getSZ50, getZZ500
from GetClassifying import getTerminated, getSuspended, getCXG, loadCXG
from GetClassifying import extractIndustrySina, extractConceptSina, extractArea
from PlotFigures import plotHPE

import Utilities as u
import Constants as c
import GlobalSettings as gs

#
# Update Data Center Parameters
#
date_start = dt.date(2005, 1, 1)
date_end = u.today()
date_cxg = '2016-01-01'

update_basics = False
update_price_stock = False
update_price_index = False
update_price_cxg = True
update_financesummary = False
update_commodity = False

force_update = False

calc_qfq = False
calc_hpe = False
calc_hep = False

update_classifying = False
extract_classifying = False

plot_hpe = False
plot_hep = False

run_strategy = False

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
    basics = basics[basics.timeToMarket != c.magic_date]

    # Save to CSV File
    u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])
    u.to_csv(basics_nottm, c.path_dict['basics'], c.file_dict['basics_nottm'])

def updatePriceStock(force_update = True):
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

        # Check if valid data file already exists
        if not validDailyHFQ(stock_id, False, force_update):
            getDailyHFQ(stock_id=stock_id, is_index=False, date_start=time_to_market,
                        date_end=date_end, time_to_market=time_to_market)
            print('Update Price:', stock_id)

def updatePriceIndex(force_update = True):
    for index_id in c.index_list:
        getDailyHFQ(stock_id=index_id, is_index=True, date_start=date_start,
                    date_end=date_end, time_to_market=None)
        print('Update Price:', index_id)

def updatePriceCXG(force_update = True):
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

        # Check if valid data file already exists
        if not validDailyHFQ(stock_id, False, force_update):
            getDailyHFQ(stock_id=stock_id, is_index=False, date_start=time_to_market,
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
        # Check if valid data file already exists
        if not validFinanceSummary(stock_id, force_update):
            getFinanceSummary(stock_id)
            print('Update Finance Summary:', stock_id)

def updateCommodity(force_update = True):
    com_list = loadCommodityList()
    com_number = len(com_list)
    for i in range(com_number):
        code = com_list.iloc[i,1]
        getCommodityPrice(code)
        extractCommodityPrice(code,'报价机构')

def calculateQFQ(period = 'M'):
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    basics_number = len(basics)
    for i in range(basics_number):
        stock_id = u.stockID(basics.loc[i,'code'])
        # Calculate QFQ Data
        calcQFQ(stock_id = stock_id, period = period)

def calculateHPE(period = 'M', ratio = 'PE'):
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    basics_number = len(basics)
    for i in range(basics_number):
        stock_id = u.stockID(basics.loc[i,'code'])
        # Calculate HPE Data
        calcHPE(stock_id = stock_id, period = period, ratio = ratio)

def plotFigureHPE(period = 'M', ratio = 'PE'):
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    basics_number = len(basics)
    for i in range(basics_number):
        stock_id = u.stockID(basics.loc[i,'code'])
        # Plot HPE Data
        plotHPE(stock_id = stock_id, period = period, ratio = ratio)

def runStrategy():
    print('Run Strategy')

###############################################################################

#
# Update Data Center Entries
#
def updateWeekly():
    updateStockBasics()
    updatePriceStock()
    updatePriceIndex()
    updateFinanceSummary()
    updateCommodity()

###############################################################################

#
# Iteratively Update Databases
#
if update_basics:
    updateStockBasics(force_update)

if update_price_stock:
    updatePriceStock(force_update)

if update_price_index:
    updatePriceIndex(force_update)

if update_financesummary:
    updateFinanceSummary(force_update)

if update_commodity:
    updateCommodity(force_update)

if calc_qfq:
    for period in ['W','M','Q']:
        calculateQFQ(period)

if calc_hpe:
    for period in ['W','M','Q']:
        calculateHPE(period=period, ratio='PE')

if calc_hep:
    for period in ['W','M','Q']:
        calculateHPE(period=period, ratio='EP')

if update_classifying:
    getIndustrySina()
    getConceptSina()
    getArea()
    getSME()
    getGEM()
    getST()
    getHS300()
    getSZ50()
    getZZ500()
    getTerminated()
    getSuspended()
    getCXG(date_cxg)

if extract_classifying:
    extractIndustrySina()
    extractConceptSina()
    extractArea()

if update_price_cxg:
    updatePriceCXG(True)

if plot_hpe:
    plotFigureHPE(period='M', ratio='PE')

if plot_hep:
    plotFigureHPE(period='M', ratio='EP')

if run_strategy:
    runStrategy()



