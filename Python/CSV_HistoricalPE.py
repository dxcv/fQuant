# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:28:29 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
from HistoricalPE import get_historical_pe
import ConstantData as cd

#
# Historical PE Parameters
#
stock_ids  = ['300059','600036','000002','002024']
year_start = 2005
year_end   = 2016

#
# Iteratively Calculate Historical PE
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    hpe = get_historical_pe(stock_id = stock_id, year_start = year_start, year_end = year_end)

    # Output Results
    if cd.is_debug:
        print(hpe.head(10))
    hpe.to_excel(cd.path_datacenter + (cd.file_historicalpe % stock_id))
























