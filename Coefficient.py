# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:50:08 2017

@author: freefrom
"""

from Strategy.CoefficientStrategy import strategyCoefficient
from Data.UpdateDataCenter import updateStockBasics, updatePriceStock, updatePriceIndex
from Plot.PlotFigures import plotCoefficient

import Common.Utilities as u
import Common.Constants as c

# Update Data Center
updateStockBasics()
updatePriceStock(True)
updatePriceIndex(True)

# Strategy Parameters
benchmark_id = '000300'
date_start = '2015-01-01'
date_end = '2017-05-03'
period = 'M'
completeness_threshold = '80.00%'
top_number = 10 

# Run Strategy
strategyCoefficient(benchmark_id, date_start, date_end, period, completeness_threshold, top_number)

# Plot Strategy Results
common_postfix = '_'.join([benchmark_id, date_start, date_end, period])
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

plotCoefficient(positive_correlation['code'], allprice, 'PositiveCorrelation', 'HS300')
plotCoefficient(zero_correlation['code'], allprice, 'ZeroCorrelation', 'HS300')
plotCoefficient(negative_correlation['code'], allprice, 'NegativeCorrelation', 'HS300')

for i in range(len(zero_correlation)):
    stock_id = u.stockID(zero_correlation.ix[i,'code'])
    plotCoefficient([stock_id], allprice, 'Zero_Correlation_'+stock_id, 'HS300')