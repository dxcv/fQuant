# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:16:02 2017

@author: freefrom
"""

import pandas as pd
import numpy as np
import datetime as dt

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
from Data.GetTrading import loadDailyQFQ

def strategyPriceFollow(stock_id, is_index, trend_threshold):
    # Load Stock Daily QFQ Data
    lshq = loadDailyQFQ(stock_id, is_index)
    if u.isNoneOrEmpty(lshq):
        raise SystemExit

    # Calculate Trend, Trend High, Trend Low, Trend Ref
    lshq['trend'] = 'Up'
    for column in ['trend_high','trend_low','trend_ref']:
        lshq[column] = 0.0
    for column in ['predict','confirm']:
        lshq[column] = np.nan
    lshq_number = len(lshq)
    trends = []
    trend_turning_points = []
    trend_index_highs = []
    trend_index_lows = []
    index_high = 0
    index_low = 0
    for i in range(lshq_number):
        if i == 0: # Initialization
            lshq.ix[i,'trend'] = 'Up'
            trends.append('Up')
            trend_turning_points.append(i)
            for column in ['trend_high','trend_low','trend_ref']:
                lshq.ix[i,column] = lshq.ix[i,'close']
        else:
            trend = lshq.ix[i-1,'trend']
            trend_high = lshq.ix[i-1,'trend_high']
            trend_low = lshq.ix[i-1,'trend_low']
            trend_ref = lshq.ix[i-1,'trend_ref']
            trend_cur = lshq.ix[i,'close']
            up_to_down = False
            down_to_up = False
            if trend == 'Up':
                if (1.0-trend_cur/trend_high) > trend_threshold:
                    lshq.ix[i,'trend'] = 'Down'
                    up_to_down = True
                    trends.append('Down')
                    trend_turning_points.append(i)
                    trend_index_highs.append(index_high)
                else:
                    lshq.ix[i,'trend'] = 'Up'
                    up_to_down = False
            else:
                if (trend_cur/trend_low-1.0) > trend_threshold:
                    lshq.ix[i,'trend'] = 'Up'
                    down_to_up = True
                    trends.append('Up')
                    trend_turning_points.append(i)
                    trend_index_lows.append(index_low)
                else:
                    lshq.ix[i,'trend'] = 'Down'
                    down_to_up = False
            if trend == 'Up':
                if up_to_down == False: # Up trend continues
                    if trend_cur > trend_high:
                        lshq.ix[i,'predict'] = 1.0
                        for j in range(index_high+1,i+1): # New high confirms all trades since last high to be up-trend
                            lshq.ix[j,'confirm'] = 1.0
                        lshq.ix[i,'trend_high'] = trend_cur
                        index_high = i
                    else:
                        ratio = (1.0-trend_cur/trend_high)/trend_threshold
                        lshq.ix[i,'predict'] = 1.0*(1.0-ratio) + (-1.0)*ratio # Map to [1.0, -1.0]
                        lshq.ix[i,'trend_high'] = trend_high
                    lshq.ix[i,'trend_ref'] = trend_ref
                else: # Up trend reverses
                    lshq.ix[i,'predict'] = -1.0
                    for j in range(index_high+1,i+1): # Turning point confirms all trades since last high to be down-trend
                        lshq.ix[j,'confirm'] = -1.0
                    lshq.ix[i,'trend_ref'] = trend_high
                    lshq.ix[i,'trend_low'] = trend_cur
                    index_low = i
            else:
                if down_to_up == False: # Down trend continues
                    if trend_cur < trend_low:
                        lshq.ix[i,'predict'] = -1.0
                        for j in range(index_low+1,i+1): # New low confirms all trades since last low to be down-trend
                            lshq.ix[j,'confirm'] = -1.0
                        lshq.ix[i,'trend_low'] = trend_cur
                        index_low = i
                    else:
                        ratio = (trend_cur/trend_low-1.0)/trend_threshold
                        lshq.ix[i,'predict'] = (-1.0)*(1.0-ratio) + (1.0)*ratio # Map to [1.0, -1.0]
                        lshq.ix[i,'trend_low'] = trend_low
                    lshq.ix[i,'trend_ref'] = trend_ref
                else: # Down trend reverses
                    lshq.ix[i,'predict'] = 1.0
                    for j in range(index_low+1,i+1): # Turning point confirms all trades since last low to be up-trend
                        lshq.ix[j,'confirm'] = 1.0
                    lshq.ix[i,'trend_ref'] = trend_low
                    lshq.ix[i,'trend_high'] = trend_cur
                    index_high = i
            # Handle Last Trend
            if i == lshq_number-1:
                if lshq.ix[i,'trend'] == 'Up':
                    trend_index_highs.append(i)
                else:
                    trend_index_lows.append(i)

    # Calculate Trend Price
    lshq['trend_price'] = 0.0
    trend_number = len(trends)
    print('Trend # =', trend_number)
    index_ref = 0
    index_tar = 0
    price_ref = 0.0
    price_tar = 0.0
    idx_high = 0
    idx_low = 0
    for i in range(trend_number):
        trend = trends[i]
        index_tar = trend_index_highs[idx_high] if trend == 'Up' else trend_index_lows[idx_low]
        price_ref = lshq.ix[index_ref, 'close']
        price_tar = lshq.ix[index_tar, 'close']
        for index in range(index_ref, index_tar):
            ratio = float(index-index_ref) / float(index_tar-index_ref)
            lshq.ix[index,'trend_price'] = price_ref*(1.0-ratio) + price_tar*ratio
        if trend == 'Up':
            index_ref = trend_index_highs[idx_high]
            idx_high = idx_high + 1
        else:
            index_ref = trend_index_lows[idx_low]
            idx_low = idx_low + 1
        # Handle Last Trend
        if i == trend_number-1:
            lshq.ix[index_tar,'trend_price'] = price_tar

    # Record Timing Data
    trend_number = len(trends)
    timing = u.createDataFrame(trend_number, ['date','trend'])
    for i in range(trend_number):
        trend = trends[i]
        index = trend_turning_points[i]
        timing.ix[i,'date'] = lshq.ix[index,'date']
        timing.ix[i,'trend'] = trend
    timing.set_index('date', inplace=True)
    timing.sort_index(ascending=True, inplace=True)

    # Save to CSV File
    file_postfix = 'Timing_%s_%s' % (u.stockFileName(stock_id, is_index), trend_threshold)
    u.to_csv(timing, c.path_dict['strategy'], file_postfix+'.csv', encoding='gbk')

    # Format Data Frame
    for column in ['trend_high','trend_low','trend_ref','trend_price']:
        lshq[column] = lshq[column].map(lambda x: '%.3f' % x)
        lshq[column] = lshq[column].astype(float)
    lshq.set_index('date', inplace=True)
    lshq.sort_index(ascending=True, inplace=True)

    # Save to CSV File
    file_postfix = 'PriceFollow_%s_%s' % (u.stockFileName(stock_id, is_index), trend_threshold)
    u.to_csv(lshq, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

def mergePriceFollow(stock_list, is_index, threshold_list):
    stock_number = len(stock_list)
    if stock_number < 1:
        print('Stock Number:', stock_number)
        raise SystemExit

    threshold_number = len(threshold_list)
    if threshold_number < 1:
        print('Threshold Number:', threshold_number)
        raise SystemExit

    # Init Price Follow Statistics for All Indexes
    stats_columns = ['date', 'index']
    for i in range(1, threshold_number-1):
        stats_columns.append('wpredict_%s' % threshold_list[i])
        stats_columns.append('wtrend_%s' % threshold_list[i])
    stats = u.createDataFrame(stock_number, stats_columns)

    for s in range(stock_number):
        stock_id = stock_list[s]
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

        # Fill One Row of Statistics
        last_index = len(df)-1
        stats.ix[s, 'date'] = df.ix[last_index, 'date']
        stats.ix[s, 'index'] = stock_id
        for i in range(1,threshold_number-1):
            column_postfix = '_%s' % threshold_list[i]
            stats.ix[s, 'wpredict'+column_postfix] = df.ix[last_index, 'wpredict'+column_postfix]
            stats.ix[s, 'wtrend'+column_postfix] = df.ix[last_index, 'wtrend'+column_postfix]

        # Format Columns
        df.set_index('date',inplace=True)
        # Save to CSV File
        file_postfix = 'PriceFollow_%s_All' % u.stockFileName(stock_id, is_index)
        u.to_csv(df, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Format Columns
    stats.set_index('date',inplace=True)
    # Save to CSV File
    file_postfix = 'PriceFollow_Statistics'
    u.to_csv(stats, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

def optimizePriceFollow(stock_list, is_index, threshold_list, method):
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
                if method == 'Threshold Weighted':
                    predict = 0.0
                    for t in [t_prev, t_curr, t_next]:
                        predict = predict + t * df2.ix[j,'predict'+'_%s'%t]
                    predict = predict / t_total
                    df2.ix[j,'weighted_predict'+column_postfix] = predict
                # Method 2: Equally Weighted Predict
                elif method == 'Equally Weighted':
                    predict = 0.0
                    for t in [t_prev, t_curr, t_next]:
                        predict = predict + 1.0 * df2.ix[j,'predict'+'_%s'%t]
                    predict = predict / 3.0
                    df2.ix[j,'weighted_predict'+column_postfix] = predict
                # Method 3: Single Predict
                else:
                    predict = df2.ix[j,'predict'+column_postfix]
                    df2.ix[j,'weighted_predict'+column_postfix] = predict

            # Optimize for Given Segments within Range [1, -1] to Find Best Cutoff
            print('Optimization Starts for Threshold:', t_curr)
            segments = 10
            delta_mean = []
            delta_stddev = []
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
                describe = df2['delta'+'_%.2f'%cutoff].describe()
                delta_mean.append(np.abs(describe['mean']))
                delta_stddev.append(describe['std'])
            # Find Best Cutoff
            delta_mean_min = min(delta_mean)
            delta_mean_index = delta_mean.index(delta_mean_min)
            print('Delta Mean:', delta_mean)
            print('Delta Stddev:', delta_stddev)
            print('Delta Mean Min:', delta_mean_min)
            print('Delta Mean Index:', delta_mean_index)
            ratio = float(delta_mean_index+1)/float(segments)
            best_cutoff = 1.0*(1.0-ratio) + (-1.0)*ratio
            print('Best Cutoff:', best_cutoff)
            print('Optimization Ends for Threshold:', t_curr)

###############################################################################

# Run Strategy Price Follow for All Indexes, with Given Threshold List
def runStrategyPriceFollow(stock_list=c.index_list, is_index = True, threshold_list=[0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33]):
    # Run Price Follow Strategy for Each Threshold Separately
    for stock_id in stock_list:
        for threshold in threshold_list:
            strategyPriceFollow(stock_id, is_index, threshold)

    # Merge Results
    mergePriceFollow(stock_list, is_index, threshold_list)

# Run Strategy Optimization for Price Follow
def runOptimizationPriceFollow(stock_list=c.index_list, is_index = True, threshold_list=[0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33]):
    # Best Cutoff will be Printed to Output Console, Use it in mergePriceFollow().cutoff
    for method in ['Threshold Weighted', 'Equally Weighted', 'Single Predict']:
        print('Optimization Method:', method)
        optimizePriceFollow(stock_list, is_index, threshold_list, method)

###############################################################################

# Analyze Strategy Price Follow
def analyzeStrategyPriceFollow(target_date, stock_list=c.index_list, is_index = True, threshold_list=[0.02, 0.03, 0.05, 0.08, 0.13, 0.21, 0.33]):
    for stock_id in stock_list:
        for threshold in threshold_list:
            analyzePriceFollow(target_date, stock_id, is_index, threshold)

def analyzePriceFollow(target_date, stock_id, is_index, threshold):
    file_postfix = 'Timing_%s_%s' % (u.stockFileName(stock_id, is_index), threshold)
    timing = u.read_csv(c.path_dict['strategy'] + file_postfix+'.csv', encoding='gbk')
    timing_number = len(timing)

    # Find the matched timing date and trend
    timing_index = -1
    for i in range(timing_number):
        date = dt.datetime.strptime(timing.ix[i,'date'],'%Y-%m-%d').date()
        if date <= target_date:
            timing_index = i
        else:
            break

    # Report results
    if timing_index != -1:
        date = dt.datetime.strptime(timing.ix[timing_index,'date'],'%Y-%m-%d').date()
        trend = timing.ix[timing_index,'trend']
        if date == target_date: # Given target_date is Timing Date
            print ('Date', target_date, ': Trend of', u.stockFileName(stock_id, is_index), 'Goes', trend)
        else:
            print('Date', target_date, ': Trend of', u.stockFileName(stock_id, is_index), 'Does Not Change, Still', trend)
    else:
        print('Date', target_date, ': Trend of', u.stockFileName(stock_id, is_index), 'Not Available, No Timing Data')