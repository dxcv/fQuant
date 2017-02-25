# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:36:03 2017

@author: freefrom
"""

from Strategy import strategyAncleXu

def runStrategy(stock_id, strategy):
    if strategy == 'AncleXu':
        strategyAncleXu(stock_id)

###############################################################################

runStrategy('000300', 'AncleXu')