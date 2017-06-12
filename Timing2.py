# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:16:07 2017

@author: freefrom
"""

import datetime as dt

from Strategy.TimingStrategy import analyzeStrategyPriceFollow

#
# All-in-one entry for daily report of timing2
#
today = dt.date.today()
stock_list = ['000300', '000905', '399006']
is_index = True
threshold_list=[0.03, 0.05]

analyzeStrategyPriceFollow(target_date=today, stock_list=stock_list,
                           is_index=is_index, threshold_list=threshold_list)