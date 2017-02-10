# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 18:00:21 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Fundamental import get_stock_basics
import GlobalSettings as gs
import Constants as c
import Utilities as u

def getStockBasics():
    # Download Stock Basics
    basics = get_stock_basics()
    if gs.is_debug:
        print(basics.head(10))

    # Save to CSV File
    u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])

def loadStockBasics():
    basics = u.read_csv(c.fullpath_dict['basics'])
    return basics


