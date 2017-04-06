# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:36:03 2017

@author: freefrom
"""

import pandas as pd
import numpy as np

import sys
sys.path.append('..')
import Common.Constants as c
import Common.Utilities as u
from Strategy import strategyAncleXu, strategyPriceFollow, strategyCXG

def runStrategySingle(stock_id, is_index, strategy):
    if strategy == 'AncleXu':
        strategyAncleXu(stock_id, is_index)
    elif strategy == 'PriceFollow':
        strategyPriceFollow(stock_id, is_index, 0.1)

def runStrategy(stock_list, is_index, strategy):
    for stock_id in stock_list:
        runStrategySingle(stock_id, is_index, strategy)

###############################################################################

# Run Strategy Price Follow for All Indexes, with Given Threshold List
def runStrategyPriceFollow(stock_list=c.index_list, is_index = True, threshold_list=[0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33]):
    for stock_id in stock_list:
        for threshold in threshold_list:
            strategyPriceFollow(stock_id, is_index, threshold)

    # Merge Results
    mergePriceFollow(stock_list, is_index, threshold_list)

    # Optimization
    # Best Cutoff will be Printed to Output Console, Use it in mergePriceFollow().cutoff
    optimizePriceFollow(stock_list, is_index, threshold_list)

# Run Strategy CXG
def runStrategyCXG(hc_segments = 5, yk_segments = 10):
    strategyCXG(hc_segments, yk_segments)

###############################################################################

runStrategyPriceFollow(stock_list=['000300'])
#runStrategyCXG(hc_segments=5, yk_segments=100)




