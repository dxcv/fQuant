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
from Plot.PlotTiming import plot_timing
from Plot.PlotIndex import plot_index, plot_index_series
from Plot.PlotHPE import plot_HPE
from Plot.PlotCoefficient import plot_coefficient_price

###############################################################################

def plotHPE(period = 'M', ratio = 'PE'):
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
        plot_HPE(stock_id = stock_id, period = period, ratio = ratio)

def plotTiming(stock_list=c.index_list, is_index=True):
    for stock_id in stock_list:
        plot_timing(stock_id, is_index)

def plotIndex(index_names):
    for index_name in index_names:
        plot_index(index_name, 'HS300')
    plot_index_series(index_names, 'FeiYan_Series', 'HS300')

def plotCoefficient(stock_ids, allprice, postfix, series_name, benchmark_name):
    plot_coefficient_price(stock_ids, allprice, postfix, series_name, benchmark_name)

def plotRelativity():
    pass

###############################################################################
