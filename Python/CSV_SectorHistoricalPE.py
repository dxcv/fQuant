# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:11:26 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd
import ConstantData as cd
import StockUtility as su
import FileUtility as fu
from QuarterlyQFQ import get_quarterly_qfq
from FinanceSummary import get_finance_summary
from HistoricalPE import get_historical_pe

#
# Get Sector Historical PE Parameters
#
sector     = '银行'
is_index   = False
year_start = 2005
year_end   = 2016

#
# Load Sector Stocks Data
#
stocks = pd.read_csv(cd.path_datacenter + cd.file_sectorstocks % sector, encoding='utf-8')
stocks['code'] = stocks['code'].map(lambda x:str(x).zfill(6))
if cd.is_debug:
    print(stocks.head(10))
stocks_number = len(stocks)

#
# Download Stock Quarterly QFQ Data & Stock Finance Summary Data
#
for i in range(stocks_number):
    stock_id = str(stocks['code'][i])
    date_timeToMarket = su.timeToMarket2(sector_stocks = stocks, stock_id = stock_id)
    
    # Get Stock Quarterly QFQ Data
    if not fu.hasFile(cd.path_datacenter, cd.file_quarterlyqfq % stock_id):
        # Download QFQ Data
        df = get_quarterly_qfq(stock_id = stock_id, is_index = is_index, year_start = year_start,
                               year_end = year_end, time_to_market = date_timeToMarket)
        # Save to CSV File
        df.to_csv(cd.path_datacenter + (cd.file_quarterlyqfq % stock_id), encoding='utf-8')

    # Get Stock Finance Summary Data
    if not fu.hasFile(cd.path_datacenter, cd.file_financesummary % stock_id):
        # Download Finance Summary Data
        df = get_finance_summary(stock_id)
        # Save to CSV file
        df.to_csv(cd.path_datacenter + (cd.file_financesummary % stock_id), encoding='utf-8')

#
# Analyze Historical PE for Sector Stocks
#
sector_hpe = pd.DataFrame()
for i in range(stocks_number):
    stock_id = str(stocks['code'][i])
    hpe = get_historical_pe(stock_id = stock_id, year_start = year_start, year_end = year_end)

    # Output Stock HPE Results
    if cd.is_debug:
        print(hpe.head(10))
    hpe.to_excel(cd.path_datacenter + (cd.file_historicalpe % stock_id))

    # Aggregate Sector HPE Data
    if i == 0:
        sector_hpe['date'] = hpe.index
        sector_hpe.set_index('date', inplace = True)

    print(hpe['pe_close'])
    sector_hpe['pe_' + stock_id] = hpe['pe_close']
    print(sector_hpe['pe_' + stock_id])

    # Output Sector Stocks HPE Results
    sector_hpe.to_excel(cd.path_datacenter + (cd.file_historicalpe % sector))









