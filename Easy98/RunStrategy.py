# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:36:03 2017

@author: freefrom
"""

from Strategy import strategyAncleXu, strategyPriceFollow
import Constants as c
import Utilities as u

def runStrategySingle(stock_id, is_index, strategy):
    if strategy == 'AncleXu':
        strategyAncleXu(stock_id, is_index)
    elif strategy == 'PriceFollow':
        strategyPriceFollow(stock_id, is_index, 0.1)

def runStrategy(stock_list, is_index, strategy):
    for stock_id in stock_list:
        runStrategySingle(stock_id, is_index, strategy)

def mergePriceFollow(stock_list, is_index, threshold_list):
    stock_number = len(stock_list)
    if stock_number < 1:
        print('Stock Number:', stock_number)
        raise SystemExit

    for stock_id in stock_list:
        threshold_number = len(threshold_list)
        if threshold_number == 0:
            continue
        else:
            # Load First Threshold
            threshold = threshold_list[0]
            file_postfix = 'PriceFollow_%s_%s' % (u.stockFileName(stock_id, is_index), threshold)
            fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
            df = u.read_csv(fullpath)
            # Drop Un-used Columns
            for column in ['trend','trend_high','trend_low','trend_ref']:
                df.drop(column, axis=1, inplace=True)
            df.rename(columns={'trend_price': 'trend_price+%s'%threshold}, inplace=True)
            # Merge Other Thresholds
            for i in range(1, threshold_number):
                threshold = threshold_list[i]
                file_postfix = 'PriceFollow_%s_%s' % (u.stockFileName(stock_id, is_index), threshold)
                fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
                df2 = u.read_csv(fullpath)
                # Append Useful Columns
                column = 'trend_price_%s' % threshold
                df[column] = df2['trend_price']
            # Save to CSV File
            file_postfix = 'PriceFollow_%s_All' % u.stockFileName(stock_id, is_index)
            u.to_csv(df, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

###############################################################################

# Run Strategy
threshold_list = [0.01, 0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33]
#for stock_id in c.index_list:
#    for threshold in threshold_list:
#        strategyPriceFollow(stock_id, True, threshold)

# Merge Results
mergePriceFollow(c.index_list, True, threshold_list)