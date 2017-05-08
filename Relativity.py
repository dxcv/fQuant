# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:46:33 2017

@author: freefrom
"""

from Strategy.RelativityStrategy import strategyRelativity, analyzeRelativity
from Strategy.Common import updateCommonData, loadAllStocks, loadAllIndex
from Strategy.Common import updateAllIndex, updateSamplePriceAllIndex
from Data.UpdateDataCenter import updateStockBasics, updatePriceStock, updatePriceIndex
from Plot.PlotFigures import plotRelativity

import Common.Utilities as u
import Common.Constants as c

# Strategy Parameters
benchmark_id = '000300'
#date_start = '2005-01-01' # Long Term
date_start = '2016-01-01' # Short Term
date_end = '2017-04-30'
period = 'M'
#completeness_threshold = '8.05%'
completeness_threshold = '80.00%' # 1350 / 42.7%
top_number = 10

# Update Data Center
update_data = False
if update_data:
    updatePriceIndex(True)
    updateAllIndex()
    for period in ['D','W','M']:
        updateSamplePriceAllIndex(benchmark_id, period)

# Run Strategy
run_strategy = True
if run_strategy:
    all_index = loadAllIndex()
    strategyRelativity(benchmark_id, all_index, True, date_start, date_end, period)

# Analyze Strategy Results
common_postfix = '_'.join([benchmark_id, date_start, date_end, period])
analyze_strategy = False
if analyze_strategy:
    analyzeRelativity()

# Plot Strategy Results
plot_strategy = False
if plot_strategy:
    plotRelativity()