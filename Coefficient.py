# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:50:08 2017

@author: freefrom
"""

from Strategy.CoefficientStrategy import strategyCoefficient, analyzeCoefficient
from Strategy.CoefficientStrategy import strategyCoefficientRolling
from Strategy.Common import loadAllStocks, loadAllIndex, updateAllIndex, updateAllStocks
from Strategy.Common import updateSamplePriceAllIndex, updateSamplePriceAllStocks
from Data.UpdateDataCenter import updateStockBasics, updatePriceStock, updatePriceIndex
from Plot.PlotFigures import plotCoefficient

import Common.Utilities as u
import Common.Constants as c

# Strategy Parameters
benchmark_id = '000300'
benchmark_name = 'HS300'
date_start = '2005-01-01'
date_end = '2017-04-30'
period = 'D'
#completeness_threshold = '8.05%'
completeness_threshold = '80.00%' # 1350 / 42.7%
top_number = 10

# Update Data Center
update_data = False
if update_data:
    # Update All Index
    updatePriceIndex(True)
    updateAllIndex()
    for period in ['D','W','M']:
        updateSamplePriceAllIndex(benchmark_id, period)
    # Update All Stocks
    updateStockBasics()
    updatePriceStock(True)
    for period in ['D','W','M']:
        updateSamplePriceAllStocks(benchmark_id, period)

# Run Strategy
run_strategy = True
if run_strategy:
    strategyCoefficientRolling(benchmark_id, date_start, date_end, period, loadAllIndex(), True, 'AllIndex')
#    strategyCoefficient(benchmark_id, date_start, date_end, period, loadAllStocks(), False, 'AllStock')

# Analyze Strategy Results
analyze_strategy = False
target_name = 'AllIndex'
#target_name = 'AllStock'
common_postfix = '_'.join(['Coefficient', date_start, date_end, period, target_name, 'vs', benchmark_id])
if analyze_strategy:
    analyzeCoefficient(common_postfix, completeness_threshold, top_number)

# Plot Strategy Results
plot_strategy = False
if plot_strategy:
    path = c.path_dict['strategy']
    file = c.file_dict['strategy'] % '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllStock'])
    price_allstock = u.read_csv(path+file)
    file = c.file_dict['strategy'] % '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllIndex'])
    price_allindex = u.read_csv(path+file)

    # Generate Statistics List
    statistics = []
    for coefficient in ['Correlation', 'Beta', 'Alpha']:
        for classification in ['Positive', 'Zero', 'Negative']:
            statistics.append(classification+coefficient)
    print(statistics)

    # Plot Statistics List
    for stats in statistics:
        # Plot statistics
        file = c.file_dict['strategy'] % '_'.join([common_postfix, completeness_threshold, stats])
        data = u.read_csv(path+file)
        postfix = '_'.join(['Coefficient', date_start, date_end, period, completeness_threshold])
        plotCoefficient(data['code'], price_allstock, postfix, stats, benchmark_name)
        # Plot single stock within each statistics
        for i in range(len(data)):
            stock_id = u.stockID(data.ix[i,'code'])
            plotCoefficient([stock_id], price_allstock, postfix, 'Positive_Correlation_'+stock_id, benchmark_name)