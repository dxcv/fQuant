# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:07:44 2017

@author: freefrom
"""

from Data.UpdateDataCenter import updatePriceIndex
from Strategy.TimingStrategy import runStrategyPriceFollow
from Plot.PlotFigures import plotTiming

#
# All-in-one entry for daily report of timing
#
updatePriceIndex(True)
runStrategyPriceFollow()
plotTiming()

#
# Test for single functionality
#