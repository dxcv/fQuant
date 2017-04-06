# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:25:05 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Constants as c

from PlotTiming import plotTiming

def plotTimingFigures(stock_list=c.index_list, is_index=True):
    for stock_id in stock_list:
        plotTiming(stock_id, is_index)

plotTimingFigures()
