# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 18:00:21 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

import sys
sys.path.append('..')

from Data.Fundamental import get_stock_basics
from Data.FinanceSummary import get_finance_summary
import Common.GlobalSettings as gs
import Common.Constants as c
import Common.Utilities as u

def getStockBasics():
    # Download Stock Basics
    basics = get_stock_basics()
    if gs.is_debug:
        print(basics.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(basics):
        u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])

def loadStockBasics():
    # Ensure data file is available
    fullpath = c.fullpath_dict['basics']
    if not u.hasFile(fullpath):
        print('Require Stock Basics: %s!' % fullpath)
        return None

    basics = u.read_csv(fullpath)
    return basics

def validStockBasics(force_update):
    if force_update == True:
        return False
    else:
        return u.hasFile(c.fullpath_dict['basics'])

def getFinanceSummary(stock_id):
    # Download Finance Summary for Given Stock
    fs = get_finance_summary(stock_id)
    if gs.is_debug:
        print(fs.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(fs):
        u.to_csv(fs, c.path_dict['finsum'], c.file_dict['finsum'] % stock_id)

def loadFinanceSummary(stock_id):
    # Ensure data file is available
    fullpath = c.fullpath_dict['finsum'] % stock_id
    if not u.hasFile(fullpath):
        print('Require Finance Summary of %s!' % fullpath)
        return None

    fs = u.read_csv(fullpath)
    return fs

def validFinanceSummary(stock_id, force_update):
    if force_update == True:
        return False
    else:
        return u.hasFile(c.fullpath_dict['finsum'] % stock_id)