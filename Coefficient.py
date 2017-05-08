# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:50:08 2017

@author: freefrom
"""

from Strategy.CoefficientStrategy import strategyCoefficient, analyzeCoefficient
from Strategy.Common import updateCommonData
from Data.UpdateDataCenter import updateStockBasics, updatePriceStock, updatePriceIndex
from Plot.PlotFigures import plotCoefficient

import Common.Utilities as u
import Common.Constants as c

# Strategy Parameters
benchmark_id = '000300'
date_start = '2005-01-01'
date_end = '2017-05-03'
period = 'M'
#completeness_threshold = '8.05%'
completeness_threshold = '80.00%' # 1350 / 42.7%
top_number = 10

# Update Data Center
update_data = False
if update_data:
    updateStockBasics()
    updatePriceStock(True)
    updatePriceIndex(True)
    updateCommonData(benchmark_id, period)

# Run Strategy
run_strategy = False
if run_strategy:
    strategyCoefficient(benchmark_id, date_start, date_end, period)

# Analyze Strategy Results
common_postfix = '_'.join([benchmark_id, date_start, date_end, period])
analyze_strategy = False
if analyze_strategy:
    analyzeCoefficient(common_postfix, completeness_threshold, top_number)

# Plot Strategy Results
plot_strategy = True
if plot_strategy:
    path = c.path_dict['strategy']
    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllStock', common_postfix])
    allstock = u.read_csv(path+file)
    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllPrice', common_postfix])
    allprice = u.read_csv(path+file)
    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', common_postfix])
    allcoef = u.read_csv(path+file)

    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', common_postfix, completeness_threshold, 'Positive_Correlation'])
    positive_correlation = u.read_csv(path+file)
    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', common_postfix, completeness_threshold, 'Zero_Correlation'])
    zero_correlation = u.read_csv(path+file)
    file = c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', common_postfix, completeness_threshold, 'Negative_Correlation'])
    negative_correlation = u.read_csv(path+file)

    #print(allstock.head(10))
    #print(allprice.head(10))
    #print(allcoef.head(10))
    #print(positive_correlation.head(10))
    #print(zero_correlation.head(10))
    #print(negative_correlation.head(10))

    common_postfix = '_'.join([benchmark_id, date_start, date_end, period, completeness_threshold])
    plotCoefficient(positive_correlation['code'], allprice, common_postfix, 'PositiveCorrelation', 'HS300')
    plotCoefficient(zero_correlation['code'], allprice, common_postfix, 'ZeroCorrelation', 'HS300')
    plotCoefficient(negative_correlation['code'], allprice, common_postfix, 'NegativeCorrelation', 'HS300')

    for i in range(len(positive_correlation)):
        stock_id = u.stockID(positive_correlation.ix[i,'code'])
        plotCoefficient([stock_id], allprice, common_postfix, 'Positive_Correlation_'+stock_id, 'HS300')
    for i in range(len(zero_correlation)):
        stock_id = u.stockID(zero_correlation.ix[i,'code'])
        plotCoefficient([stock_id], allprice, common_postfix, 'Zero_Correlation_'+stock_id, 'HS300')
    for i in range(len(negative_correlation)):
        stock_id = u.stockID(negative_correlation.ix[i,'code'])
        plotCoefficient([stock_id], allprice, common_postfix, 'Negative_Correlation_'+stock_id, 'HS300')