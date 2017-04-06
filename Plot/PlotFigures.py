# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:25:05 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u

from Data.GetFundamental import loadStockBasics
from PlotTiming import plotTiming
from PlotHPE import plotHPE

###############################################################################

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

def plotTimingFigures(stock_list=c.index_list, is_index=True):
    for stock_id in stock_list:
        plotTiming(stock_id, is_index)

###############################################################################

plotFigureHPE()
plotTimingFigures()
