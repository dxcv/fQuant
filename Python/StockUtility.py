# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:15:26 2017

@author: freefrom
"""
import datetime as dt
import pandas as pd
import FileUtility as fu
import ConstantData as cd

# Load Stock Basics CSV File and Return DataFrame
def loadStockBasics(path_basics = cd.path_datacenter, file_basics = cd.file_stockbasics):
    stock_basics = None
    if fu.hasFile(path = path_basics, file = file_basics):
        stock_basics = pd.read_csv(path_basics + file_basics, encoding='utf-8')
        stock_basics.set_index('code', inplace=True)
        if cd.is_debug:
            print(stock_basics.head(10))
    return stock_basics

# Extract Stock Time-to-Market from Stock Basics Data
def timeToMarket(stock_basics, stock_id):
    d = None
    if (not stock_basics is None) and (stock_id in stock_basics.index): # Assume 'code' is index
        date = stock_basics.loc[stock_id, 'timeToMarket'] #上市日期YYYYMMDD
        if cd.is_debug:
            print(date)

        date = pd.to_datetime(date, format='%Y%m%d')
        if cd.is_debug:
            print(date.year, date.month, date.day)
        d = dt.date(date.year, date.month, date.day)
    return d
