# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:54:12 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts

#
# Get Fundamental Parameters
#
path_datacenter = '../DataCenter/'

#
# Get and Save Stock Basics
#
basics = ts.get_stock_basics()
basics.to_csv(path_datacenter+'StockBasics'+'.csv',encoding='utf-8')

#
# Get and Save Report Data
#
for year in range(2005, 2017):
    for quarter in range(1, 5):
        report = ts.get_report_data(year, quarter)
        postfix = '_'+str(year)+'Q'+str(quarter)
        report.to_csv(path_datacenter+'ReportData'+postfix+'.csv',encoding='utf-8')