# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:07:44 2017

@author: freefrom
"""

from Data.UpdateDataCenter import updatePriceIndex
from Strategy.TimingStrategy import runStrategyPriceFollow, mergePriceFollow
from Plot.PlotFigures import plotTiming

import Common.Constants as c

#
# All-in-one entry for daily report of timing
#
updatePriceIndex(True)
runStrategyPriceFollow()
plotTiming()

#
# Test for single functionality
#
#mergePriceFollow(stock_list=c.index_list, is_index = True, threshold_list=[0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33])