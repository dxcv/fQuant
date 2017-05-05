# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:59:58 2017

@author: freefrom
"""

import pandas as pd
import numpy as np

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
import Common.GlobalSettings as gs

from Data.GetTrading import loadDailyQFQ
from Data.GetFundamental import loadStockBasics

def strategyCoefficient(benchmark_id = '000300', date_start = '2015-01-01', date_end = '2016-12-31', period = 'M', 
                        completeness_threshold = '80.00%', top_number = 20):
    '''
    函数功能：
    --------
    按照给定起止时间和给定频率，计算全市场所有股票和业绩基准之间的Alpha/Beta/Correlation。
    假定：全市场股票列表，个股历史前复权数据，业绩基准历史前复权数据已经提前获取并存储为CSV文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. 000300
    date_start : string, 起始日期 e.g. '2015-01-01'
    date_end : string, 终止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'

    输出参数：
    --------
    DataFrame
        code : 股票代码
        alpha : alpha系数
        beta : beta系数
        correlation : 相关系数

    数据文件
        Strategy_Coefficient_AllPrice_Benchmark_DateStart_Date_End_Period.csv : 与业绩基准时间对其的所有股票价格
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_Date_End_Period.csv  : 与业绩基准相参照的所有股票系数
    '''
    # Check Period
    period_types = ['W','M','Q']
    if not period in period_types:
        print('Un-supported period type - should be one of:', period_types)
        return None

    # Common Postfix
    common_postfix = '_'.join([benchmark_id, date_start, date_end, period])

    # Load All Stocks
    allstock = loadAllStocks(common_postfix)
    if u.isNoneOrEmpty(allstock):
        return None

    # Sample Prices
    allprice = samplePrice(benchmark_id, allstock, date_start, date_end, period)
    if u.isNoneOrEmpty(allprice):
        return None

    # Calculate Coefficients: Alpha, Beta, Correlation
    allcoef = calculateCoefficient(common_postfix)
    if u.isNoneOrEmpty(allcoef):
        return None

    # Analyze Filtered Coefficients
    analyzeCoefficient(common_postfix, completeness_threshold, top_number)

def loadAllStocks(postfix):
    # Load Local Cache of Stock Basics
    file_postfix = '_'.join(['Coefficient', 'AllStock', postfix])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allstock = u.read_csv(fullpath)    
    if not u.isNoneOrEmpty(allstock):
        return allstock['code']

    # Load from Fundamental Stock Basics
    allstock = loadStockBasics()
    if u.isNoneOrEmpty(allstock):
        return None
    stock_ids = allstock['code']
    # Save to CSV File
    allstock.set_index('code',inplace=True)
    u.to_csv(allstock, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return stock_ids

def samplePrice(benchmark_id, stock_ids, date_start, date_end, period):
    # Check if AllPrice File Already Exists
    file_postfix = '_'.join(['Coefficient', 'AllPrice', benchmark_id, date_start, date_end, period])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allprice = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allprice):
        return allprice

    # Load Benchmark
    benchmark = loadDailyQFQ(benchmark_id, True)
    if u.isNoneOrEmpty(benchmark):
        return None

    # Resample Benchmark
    benchmark['date'] = benchmark['date'].astype(np.datetime64)
    benchmark.set_index('date', inplace=True)
    benchmark.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(benchmark.head(10))

    drop_columns = ['open','high','low','volume','amount']
    benchmark.drop(drop_columns,axis=1,inplace=True)
    allprice = benchmark.resample(period).first()
    allprice['close'] = benchmark['close'].resample(period).last()
    allprice['close'] = allprice['close'].map(lambda x: '%.3f' % x)
    allprice['close'] = allprice['close'].astype(float)

    # Iterate over all stocks
    stocks_number = len(stock_ids)
    for i in range(stocks_number):
        # Load Stock LSHQ
        stock_id = u.stockID(stock_ids[i])
        stock = loadDailyQFQ(stock_id, False)
        if u.isNoneOrEmpty(stock):
            continue
        stock['date'] = stock['date'].astype(np.datetime64)
        stock.set_index('date', inplace=True)
        stock.sort_index(ascending = True, inplace=True)
        if gs.is_debug:
            print(stock.head(10))

        # Resample Stock LSHQ
        stock.drop(drop_columns,axis=1,inplace=True)
        stock_resample = stock.resample(period).first()
        stock_resample['close'] = stock['close'].resample(period).last()
        stock_resample['close'] = stock_resample['close'].map(lambda x: '%.3f' % x)
        stock_resample['close'] = stock_resample['close'].astype(float)

        # Merge Benchmark with Stock
        allprice = pd.merge(allprice, stock_resample, how='left', left_index=True, right_index=True, 
                             sort=True, suffixes=('','_'+stock_id))

    # Save to CSV File
    u.to_csv(allprice, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return allprice

def calculateCoefficient(postfix):
    # Check if AllPrice File Already Exists
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allcoef = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allcoef):
        return allcoef

    # Load Coefficient_AllPrice
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllPrice', postfix])
    allprice = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allprice):
        print('Require Coefficient AllPrice File: %s!' % fullpath)
        return None

    # Calculate Coefficient for Each Stock
    stocks_number = len(allprice.columns) - 2
    if stocks_number <= 0:
        print('No Stock Data in Coefficient AllPrice File!')
        return None

    allcoef = u.createDataFrame(stocks_number, columns=['code','completeness','alpha','beta','correlation'])
    for i in range(stocks_number):
        column = allprice.columns[i+2]
        # Compute correlation with other Series, excluding missing values.
        # Set min_periods to 12 (Months) to avoid CXG whose IPO date is less than one year earlier.
        correlation = allprice['close'].corr(allprice[column], min_periods=12)
        allcoef.ix[i,'code'] = column.replace('close_', '')
        allcoef.ix[i,'correlation'] = correlation
        null_count = allprice[column].isnull().sum()
        allcoef.ix[i,'completeness'] = 1.0 - float(null_count) / len(allprice[column])

    # Format Columns
    allcoef.set_index('code',inplace=True)
    for column in ['alpha','beta','correlation']:
        allcoef[column] = allcoef[column].map(lambda x: '%.3f' % x)
        allcoef[column] = allcoef[column].astype(float)
    allcoef['completeness'] = allcoef['completeness'].map(lambda x: ('%.2f' % (x*100)) + '%')

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix])
    u.to_csv(allcoef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return allcoef

def analyzeCoefficient(postfix, completeness_threshold, top_number):
    # Load Coefficient_AllCoef
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', postfix])
    allcoef = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allcoef):
        print('Require Coefficient AllCoef File: %s!' % fullpath)
        return None

    # Filter Out Stocks without Sufficient Data
    threshold = float(completeness_threshold.replace('%',''))
    allcoef['completeness'] = allcoef['completeness'].map(lambda x: x.replace('%',''))
    allcoef['completeness'] = allcoef['completeness'].astype(float)
    allcoef = allcoef[allcoef.completeness >= threshold]
    allcoef['completeness'] = allcoef['completeness'].map(lambda x: ('%.2f' % (x)) + '%')
    allcoef.set_index('code',inplace=True)

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold])
    u.to_csv(allcoef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Calculate Coefficient Statistics
    allcoef['correlation_abs'] = allcoef['correlation'].map(lambda x: abs(x))
    allcoef['correlation_abs'] = allcoef['correlation_abs'].astype(float)
    negative_correlation = allcoef[allcoef.correlation < 0.0]
    positive_correlation = allcoef[allcoef.correlation > 0.0]
    zero_correlation = allcoef[allcoef.correlation_abs < 0.25]

    # Filter Out Top Number of Positive Correlation
    positive_correlation = positive_correlation.sort_values('correlation', axis=0, ascending=False)
    positive_correlation = positive_correlation[0:(top_number if len(positive_correlation) >= top_number else len(positive_correlation))]

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold, 'Positive_Correlation'])
    u.to_csv(positive_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Zero Correlation
    zero_correlation = zero_correlation.sort_values('correlation_abs', axis=0, ascending=True)
    zero_correlation = zero_correlation[0:(top_number if len(zero_correlation) >= top_number else len(zero_correlation))]

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold, 'Zero_Correlation'])
    u.to_csv(zero_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Negative Correlation
    negative_correlation = negative_correlation.sort_values('correlation', axis=0, ascending=True)
    negative_correlation = negative_correlation[0:(top_number if len(negative_correlation) >= top_number else len(negative_correlation))]

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold, 'Negative_Correlation'])
    u.to_csv(negative_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return [positive_correlation, zero_correlation, negative_correlation]