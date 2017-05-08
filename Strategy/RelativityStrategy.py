# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:52:00 2017

@author: freefrom
"""

import pandas as pd
import numpy as np

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
import Common.GlobalSettings as gs

from Strategy.Common import checkPeriod, samplePrice

def strategyRelativity(benchmark_id, stock_ids, is_index, date_start, date_end, period):
    '''
    函数功能：
    --------
    按照给定起止时间和采样频率，计算全市场所有指数和业绩基准之间的相对强弱。
    假定：全市场指数列表，指数历史前复权数据，业绩基准历史前复权数据已经提前获取并存储为CSV文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'
    stock_ids : pandas.Series or list, 股票/指数列表
    is_index : boolean, 股票/指数标识
    date_start : string, 起始日期 e.g. '2005-01-01'
    date_end : string, 终止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'

    输出参数：
    --------
    True/False : boolean, 策略运行是否完成

    数据文件
        Strategy_Relativity_DateStart_DateEnd_Period_Stock_vs_Benchmark.csv : 参与计算的所有指数相对强弱

    '''
    # Check Period
    if not checkPeriod(period):
        return False

    # Sample Prices
    price = samplePrice(benchmark_id, stock_ids, is_index, date_start, date_end, period)
    if u.isNoneOrEmpty(price):
        return False

    # Output Data
    df = price.copy()

    # Calculate Relativity
    # 1. Turn Prices to Ratios
    date_number = len(price)
    column_number = len(price.columns)
    relativity = u.createDataFrame(date_number, price.columns, np.nan)
    relativity['date'] = price['date']
    for col in range(1, column_number): # Skip 'date'
        column = relativity.columns[col]
        for i in range(1, date_number):
            prev_price = price.ix[i-1,column]
            curr_price = price.ix[i,column]
            if not np.isnan(prev_price) and not np.isnan(curr_price): # Both are valid prices
                relativity.ix[i,column] = (curr_price-prev_price)/prev_price # Turn price to ratio

    for col in range(1, column_number): # Skip 'date'
        column = relativity.columns[col]
        df['ratio_'+column[-6:]] = relativity[column]

    # 2. Turn Ratios to Deltas
    for col in range(2, column_number): # Skip 'date' and 'close_benchmark'
        column = relativity.columns[col]
        for i in range(1, date_number):
            ratio_stock = relativity.ix[i,column]
            ratio_bench = relativity.ix[i,'close_'+benchmark_id]
            if not np.isnan(ratio_stock) and not np.isnan(ratio_bench): # Both are valid ratios
                relativity.ix[i,column] = ratio_stock - ratio_bench # Turn ratio to delta

    for col in range(2, column_number): # Skip 'date' and 'close_benchmark'
        column = relativity.columns[col]
        df['delta_'+column[-6:]] = relativity[column]

    # 3. Turn Deltas to Accumulated Deltas
    for col in range(2, column_number): # Skip 'date' and 'close_benchmark'
        column = relativity.columns[col]
        for i in range(1, date_number):
            prev_delta = relativity.ix[i-1,column]
            curr_delta = relativity.ix[i,column]
            if not np.isnan(prev_delta) and not np.isnan(curr_delta): # Both are valid deltas
                relativity.ix[i,column] = prev_delta + curr_delta # Turn delta to accumulated delta

    for col in range(2, column_number): # Skip 'date' and 'close_benchmark'
        column = relativity.columns[col]
        df['accumu_'+column[-6:]] = relativity[column]

    # Save to CSV File
    df.set_index('date',inplace=True)
    file_postfix = '_'.join(['Relativity', 'Data', date_start, date_end, period, 'AllIndex', 'vs', benchmark_id])
    u.to_csv(df, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def analyzeRelativity():
    pass
