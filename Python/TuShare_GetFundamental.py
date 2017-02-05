# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:54:12 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import ConstantData as cd

#
# Get Fundamental Parameters
#

#
# Get and Save Stock Basics
#
basics = ts.get_stock_basics()
basics.to_csv(cd.path_datacenter+cd.file_stockbasics, encoding='utf-8')

#
# Get and Save Report Data
#
for year in range(2005, 2017):
    for quarter in range(1, 5):
        report = ts.get_report_data(year, quarter)
        postfix = str(year)+'Q'+str(quarter)
        report.to_csv(cd.path_datacenter + (cd.file_reportdata % postfix), encoding='utf-8')

#
# Get and Save Report Data
#
for year in range(2005, 2017):
    for quarter in range(1, 5):
        profit = ts.get_profit_data(year, quarter)
        postfix = str(year)+'Q'+str(quarter)
        profit.to_csv(cd.path_datacenter + (cd.file_profitdata % postfix), encoding='utf-8')