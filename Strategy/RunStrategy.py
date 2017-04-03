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

def mergePriceFollow(stock_list, is_index, threshold_list):
    stock_number = len(stock_list)
    if stock_number < 1:
        print('Stock Number:', stock_number)
        raise SystemExit

    threshold_number = len(threshold_list)
    if threshold_number < 1:
        print('Threshold Number:', threshold_number)
        raise SystemExit

    for stock_id in stock_list:
        # Load Results from Different Threshold
        dfs = []
        for i in range(threshold_number):
            threshold = threshold_list[i]
            file_postfix = 'PriceFollow_%s_%s' % (u.stockFileName(stock_id, is_index), threshold)
            fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
            df = u.read_csv(fullpath)
            dfs.append(df)
        # Compose Final Results
        drop_columns = ['trend','trend_high','trend_low','trend_ref','trend_price','predict','confirm']
        df = dfs[0].drop(drop_columns,axis=1)
        for i in range(threshold_number):
            threshold = threshold_list[i]
            column = 'trend'
            df[column+'_%s'%threshold] = dfs[i][column]
        for i in range(threshold_number):
            threshold = threshold_list[i]
            column = 'trend_price'
            df[column+'_%s'%threshold] = dfs[i][column]
        for i in range(threshold_number):
            threshold = threshold_list[i]
            column = 'predict'
            df[column+'_%s'%threshold] = dfs[i][column]
        for i in range(threshold_number):
            threshold = threshold_list[i]
            column = 'confirm'
            df[column+'_%s'%threshold] = dfs[i][column]
        # Weighted Predict Columns
        cutoff = 0.0 # Optimized cutoff for weighted predict
        for i in range(1,threshold_number-1):
            t_prev = threshold_list[i-1]
            t_curr = threshold_list[i]
            t_next = threshold_list[i+1]
            t_total = t_prev + t_curr + t_next
            column_postfix = '_%s' % t_curr
            df['wpredict'+column_postfix] = np.nan
            df['wtrend'+column_postfix] = np.nan
            row_number = len(df)
            for j in range(1, row_number):
                wpredict = 0.0
                for t in [t_prev, t_curr, t_next]:
                    wpredict = wpredict + t * df.ix[j,'predict'+'_%s'%t]
                wpredict = wpredict / t_total
                df.ix[j,'wpredict'+column_postfix] = wpredict
                df.ix[j,'wtrend'+column_postfix] = 'Up' if wpredict >= cutoff else 'Down'

        # Format Columns
        df.set_index('date',inplace=True)
        # Save to CSV File
        file_postfix = 'PriceFollow_%s_All' % u.stockFileName(stock_id, is_index)
        u.to_csv(df, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

def optimizePriceFollow(stock_list, is_index, threshold_list):
    stock_number = len(stock_list)
    if stock_number < 1:
        print('Stock Number:', stock_number)
        raise SystemExit

    threshold_number = len(threshold_list)
    if threshold_number < 1:
        print('Threshold Number:', threshold_number)
        raise SystemExit

    for stock_id in stock_list:
        # Load Results from Different Threshold
        file_postfix = 'PriceFollow_%s_All' % u.stockFileName(stock_id, is_index)
        df = u.read_csv(c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix)
        row_number = len(df)
        for i in range(1,threshold_number-1):
            t_prev = threshold_list[i-1]
            t_curr = threshold_list[i]
            t_next = threshold_list[i+1]
            t_total = t_prev + t_curr + t_next
            column_postfix = '_%s' % t_curr
            # Slice Interested Columns
            select_columns = []
            for t in [t_prev, t_curr, t_next]:
                select_columns.append('predict'+'_%s'%t)
            select_columns.append('confirm'+column_postfix)
            df2 = pd.DataFrame.copy(df.loc[:,select_columns])
            # Calculate Weighted Predict
            df2['weighted_predict'+column_postfix] = np.nan
            for j in range(1, row_number):
                # Method 1: Threshold Weighted Predict
                predict = 0.0
                for t in [t_prev, t_curr, t_next]:
                    predict = predict + t * df2.ix[j,'predict'+'_%s'%t]
                predict = predict / t_total
                df2.ix[j,'weighted_predict'+column_postfix] = predict
                # Method 2: Equally Weighted Predict
#                predict = 0.0
#                for t in [t_prev, t_curr, t_next]:
#                    predict = predict + 1.0 * df2.ix[j,'predict'+'_%s'%t]
#                predict = predict / 3.0
#                df2.ix[j,'weighted_predict'+column_postfix] = predict
                # Method 3: Single Predict
#                predict = df2.ix[j,'predict'+column_postfix]
#                df2.ix[j,'weighted_predict'+column_postfix] = predict

            # Optimize for Given Segments within Range [1, -1] to Find Best Cutoff
            print('Optimization Starts for Threshold:', t_curr)
            segments = 10
            delta_descriptions = []
            for j in range(1, row_number):
                weighted_predict = df2.ix[j,'weighted_predict'+column_postfix]
                confirm = df2.ix[j,'confirm'+column_postfix]
                for k in range(1, segments):
                    ratio = float(k)/float(segments)
                    cutoff = 1.0*(1.0-ratio) + (-1.0)*ratio
                    predict_cutoff = 1 if weighted_predict > cutoff else -1
                    delta_cutoff = predict_cutoff - confirm if not np.isnan(confirm) else np.nan
                    df2.ix[j,'delta'+'_%.2f'%cutoff] = delta_cutoff
            # Save to CSV File
            file_postfix = 'PriceFollow_%s_Cutoff_%s' % (u.stockFileName(stock_id, is_index), t_curr)
            u.to_csv(df2, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)
            # Gather Mean of Delta_Cutoffs
            for k in range(1, segments):
                ratio = float(k)/float(segments)
                cutoff = 1.0*(1.0-ratio) + (-1.0)*ratio
                delta_descriptions.append(np.abs(df2['delta'+'_%.2f'%cutoff].describe()['mean']))
            # Find Best Cutoff
            delta_min = min(delta_descriptions)
            delta_index = delta_descriptions.index(delta_min)
            print('Delta Descriptions:', delta_descriptions)
            print('Delta Min:', delta_min)
            print('Delta Index:', delta_index)
            ratio = float(delta_index+1)/float(segments)
            best_cutoff = 1.0*(1.0-ratio) + (-1.0)*ratio
            print('Best Cutoff:', best_cutoff)
            print('Optimization Ends for Threshold:', t_curr)

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




