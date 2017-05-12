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

from Strategy.Common import samplePrice, ignoreData, checkPeriod, checkRatioMethod, dataToRatio

def strategyCoefficient(benchmark_id, date_start, date_end, period, ratio_method, stock_ids, is_index, stock_name):
    '''
    函数功能：
    --------
    按照给定起止时间和给定频率，计算全市场所有股票和业绩基准之间的Alpha/Beta/Correlation。
    假定：全市场股票列表，个股历史前复权数据，业绩基准历史前复权数据已经提前获取并存储为CSV文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'
    date_start : string, 起始日期 e.g. '2005-01-01'
    date_end : string, 终止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'
    ratio_method : string, 比例计算方法 e.g. 'B'
    stock_ids : pandas.Series or list, 股票/指数列表
    is_index : boolean, 股票/指数标识
    stock_name : string, 股票/指数名称

    输出参数：
    --------
    True/False : boolean, 策略运行是否完成

    数据文件
        Strategy_Coefficient_DateStart_DateEnd_Period_RatioMethod_StockName_vs_Benchmark.csv : 参与计算的所有所有股票/指数系数
    '''
    # Check Period and Ratio Method
    if not checkPeriod(period) or not checkRatioMethod(ratio_method):
        return False

    # Sample Prices
    price = samplePrice(benchmark_id, stock_ids, is_index, date_start, date_end, period)
    if u.isNoneOrEmpty(price):
        return False

    # Calculate Coefficients: Alpha, Beta, Correlation
    # For newly-IPO stocks, we need to ignore first 3-month trading.
    # And if the time-to-market date is less than one year, we will skip it when calculating coefficient.
    # For index, we need to ignore first data.
    ignore_dict = {'M':1,'W':1,'D':1} if is_index else {'M':3,'W':3*4,'D':3*4*5}
    min_period_dict = {'M':12,'W':12*4,'D':12*4*5}
    coef = calculateCoefficient(price, ignore_dict[period], min_period_dict[period]-ignore_dict[period], ratio_method)
    if u.isNoneOrEmpty(coef):
        return False

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', date_start, date_end, period, ratio_method, stock_name, 'vs', benchmark_id])
    u.to_csv(coef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def calculateCoefficient(price, ignore_number, min_period_number, ratio_method):
    # Create Coefficient Data Frame
    stocks_number = len(price.columns) - 2 # Remove 'date', 'close_benchmark'
    if stocks_number <= 0:
        print('No Stock Data to Calculate Coefficient!')
        return None
    coef = u.createDataFrame(stocks_number, columns=['code','completeness','alpha','beta','correlation'])

    # Calculate Coefficients
    # 1. Calculate Correlation - No need to interpolate price for stop trading
    benchmark = price[price.columns[1]]
    bench_ratio = dataToRatio(benchmark, ratio_method)
    for i in range(stocks_number):
        column = price.columns[i+2]
        stock = price[column].copy()
        # Turn price to ratio
        stock_ratio = dataToRatio(stock, ratio_method)
        # Manually ignore a given number of valid data (since IPO)
        stock_ratio = ignoreData(stock_ratio, ignore_number)
        # Compose data frame and drop NaN
        df = pd.DataFrame({'bench_ratio':bench_ratio,'stock_ratio':stock_ratio})
        df = df.dropna(axis=0,how='any')
        df = df.reset_index(drop=True)
        df_number = len(df)
        # Compute correlation with other Series, excluding missing values.
        if df_number >= min_period_number: # Has sufficient data, exclude those IPO recently.
            b_ratio = df['bench_ratio']
            s_ratio = df['stock_ratio']
            correlation = b_ratio.corr(s_ratio)
            coef.ix[i,'correlation'] = correlation
        # Calculate completeness
        coef.ix[i,'code'] = column.replace('close_', '')
        null_count = price[column].isnull().sum()
        coef.ix[i,'completeness'] = 1.0 - float(null_count) / len(price[column])

    # 2. Calculate Alpha and Beta - Need to interpolate price for stop trading
    benchmark = price[price.columns[1]]
    bench_ratio = dataToRatio(benchmark, ratio_method)
    for i in range(stocks_number):
        column = price.columns[i+2]
        stock = price[column].copy()
        # Turn price to ratio
        stock_ratio = dataToRatio(stock, ratio_method)
        # Manually ignore a given number of valid data (since IPO)
        stock_ratio = ignoreData(stock_ratio, ignore_number)
        # Compose data frame and drop NaN
        df = pd.DataFrame({'bench_ratio':bench_ratio,'stock_ratio':stock_ratio})
        df = df.dropna(axis=0,how='any')
        df = df.reset_index(drop=True)
        df_number = len(df)
        if df_number >= min_period_number: # Has sufficient data
            # Compute Beta w.r.t. Benchmark
            b_ratio = df['bench_ratio']
            s_ratio = df['stock_ratio']
            b_mean = b_ratio.mean()
            s_mean = s_ratio.mean()
            a = 0.0
            b = 0.0
            for j in range(df_number):
                a += (b_ratio[j]-b_mean) * (s_ratio[j]-s_mean)
                b += (b_ratio[j]-b_mean) * (b_ratio[j]-b_mean)
            beta = a/b
            # Same as below method
            # beta = b_ratio.cov(s_ratio) / b_ratio.var()
            coef.ix[i,'beta'] = beta
            # Calculate Alpha
            alpha = s_mean - beta*b_mean
            coef.ix[i,'alpha'] = alpha

    # Format Columns
    coef.set_index('code',inplace=True)
    for column in ['alpha','beta','correlation']:
        coef[column] = coef[column].map(lambda x: '%.3f' % x)
        coef[column] = coef[column].astype(float)
    coef['completeness'] = coef['completeness'].map(lambda x: ('%.2f' % (x*100)) + '%')

    return coef

###############################################################################

def strategyCoefficientRolling(benchmark_id, date_start, date_end, period, ratio_method, stock_ids, is_index, stock_name):
    '''
    函数功能：
    --------
    按照给定起止时间和给定频率，按照滚动的方式，计算全市场所有股票和业绩基准之间的Alpha/Beta/Correlation。
    假定：全市场股票列表，个股历史前复权数据，业绩基准历史前复权数据已经提前获取并存储为CSV文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'
    date_start : string, 起始日期 e.g. '2005-01-01'
    date_end : string, 终止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'
    ratio_method : string, 比例计算方法 e.g. 'B'
    stock_ids : pandas.Series or list, 股票/指数列表
    is_index : boolean, 股票/指数标识
    stock_name : string, 股票/指数名称

    输出参数：
    --------
    True/False : boolean, 策略运行是否完成

    数据文件
        Strategy_Coefficient_DateStart_DateEnd_Period_RatioMethod_StockName_vs_Benchmark.csv : 参与计算的所有所有股票/指数系数
    '''
    # Check Period and Ratio Method
    if not checkPeriod(period) or not checkRatioMethod(ratio_method):
        return False

    # Sample Prices
    price = samplePrice(benchmark_id, stock_ids, is_index, date_start, date_end, period)
    if u.isNoneOrEmpty(price):
        return False

    # Calculate Coefficients: Alpha, Beta, Correlation
    rolling_number_dict = {'M':3,'W':3*4,'D':3*4*5}
    min_period_dict = {'M':2,'W':2*4,'D':2*4*5}
    coef = calculateCoefficientRolling(price, rolling_number_dict[period], min_period_dict[period], ratio_method)
    if u.isNoneOrEmpty(coef):
        return False

    # Save to CSV File
    file_postfix = '_'.join(['Coefficient', date_start, date_end, period, ratio_method, stock_name, 'vs', benchmark_id, 'Rolling', str(rolling_number_dict[period])])
    u.to_csv(coef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def calculateCoefficientRolling(price, rolling_number, min_period_number, ratio_method):
    # Create Coefficient Data Frame
    stocks_number = len(price.columns) - 2 # Remove 'date', 'close_benchmark'
    if stocks_number <= 0:
        print('No Stock Data to Calculate Coefficient!')
        return None
    date_number = len(price)
    coef_columns = ['date', 'close']
    for i in range(stocks_number):
        column = price.columns[i+2]
        stock_id = column.replace('close_', '')
        for item in ['close','completeness','alpha','beta','correlation']:
            coef_columns.append('_'.join([item,stock_id]))
    coef = u.createDataFrame(date_number, columns=coef_columns)
    coef['date'] = price['date']
    coef['close'] = price['close']
    for i in range(stocks_number):
        column = price.columns[i+2]
        coef[column] = price[column]

    # Calculate Coefficients
    # 1. Calculate Correlation - No need to interpolate price_rolling for stop trading
    for i in range(date_number):
        if i+1 < rolling_number:
            continue
        price_rolling = price.iloc[i+1-rolling_number:i+1,:]
        price_rolling = price_rolling.reset_index(drop=True)
        benchmark = price_rolling[price_rolling.columns[1]]
        bench_ratio = dataToRatio(benchmark, ratio_method)
        for j in range(stocks_number):
            column = price_rolling.columns[j+2]
            stock_id = column.replace('close_', '')
            stock = price_rolling[column].copy()
            # Turn price to ratio
            stock_ratio = dataToRatio(stock, ratio_method)
            # Compose data frame and drop NaN
            df = pd.DataFrame({'bench_ratio':bench_ratio,'stock_ratio':stock_ratio})
            df = df.dropna(axis=0,how='any')
            df = df.reset_index(drop=True)
            df_number = len(df)
            if df_number >= min_period_number: # Has sufficient data
                b_ratio = df['bench_ratio']
                s_ratio = df['stock_ratio']
                correlation = b_ratio.corr(s_ratio)
                coef.ix[i,'_'.join(['correlation',stock_id])] = correlation
            # Calculate completeness
            null_count = price_rolling[column].isnull().sum()
            coef.ix[i,'_'.join(['completeness',stock_id])] = 1.0 - float(null_count) / len(price[column])

    # 2. Calculate Alpha and Beta - No need to interpolate price_rolling for stop trading
    for i in range(date_number):
        if i+1 < rolling_number:
            continue
        price_rolling = price.iloc[i+1-rolling_number:i+1,:]
        price_rolling = price_rolling.reset_index(drop=True)
        benchmark = price_rolling[price_rolling.columns[1]]
        bench_ratio = dataToRatio(benchmark, ratio_method)
        for j in range(stocks_number):
            column = price_rolling.columns[j+2]
            stock_id = column.replace('close_', '')
            stock = price_rolling[column].copy()
            # Turn price to ratio
            stock_ratio = dataToRatio(stock, ratio_method)
            # Compose data frame and drop NaN
            df = pd.DataFrame({'bench_ratio':bench_ratio,'stock_ratio':stock_ratio})
            df = df.dropna(axis=0,how='any')
            df = df.reset_index(drop=True)
            df_number = len(df)
            if df_number >= min_period_number: # Has sufficient data
                # Compute Beta w.r.t. Benchmark
                b_ratio = df['bench_ratio']
                s_ratio = df['stock_ratio']
                b_mean = b_ratio.mean()
                s_mean = s_ratio.mean()
                a = 0.0
                b = 0.0
                for k in range(df_number):
                    a += (b_ratio[k]-b_mean) * (s_ratio[k]-s_mean)
                    b += (b_ratio[k]-b_mean) * (b_ratio[k]-b_mean)
                beta = a/b
                # Same as below method
                # beta = b_ratio.cov(s_ratio) / b_ratio.var()
                coef.ix[i,'_'.join(['beta',stock_id])] = beta
                # Calculate Alpha
                alpha = s_mean - beta*b_mean
                coef.ix[i,'_'.join(['alpha',stock_id])] = alpha

    # Format Columns
    coef.set_index('date',inplace=True)
    for i in range(stocks_number):
        stock_id = price.columns[i+2].replace('close_', '')
        for item in ['alpha','beta','correlation']:
            column = '_'.join([item,stock_id])
            coef[column] = coef[column].map(lambda x: '%.3f' % x)
            coef[column] = coef[column].astype(float)
        for item in ['completeness']:
            column = '_'.join([item,stock_id])
            coef[column] = coef[column].map(lambda x: ('%.2f' % (x*100)) + '%' if not np.isnan(x) else np.nan)

    return coef

###############################################################################

def analyzeCoefficient(postfix, completeness_threshold, top_number):
    '''
    函数功能：
    --------
    根据计算的系数文件，做进一步统计分析。
    假定：全市场股票相对于业绩基准的系数已经计算完成并存储为CSV文件。

    输入参数：
    --------
    postfix : string, 系数文件后缀 e.g. Coefficient_2005-01-01_2017-04-30_M_AllStock_vs_000300。
    completeness_threshold : string, 起始日期 e.g. '80.00%', 即选取不少于80.00%的历史数据的个股做后续分析。
    top_number : int, 各类排行榜的入选个股数量 e.g. 20, 选取不多于20只个股。

    输出参数：
    --------
    True/False : boolean, 策略分析是否完成

    数据文件
        Common_Prefix = Strategy_Coefficient_DateStart_DateEnd_Period_RatioMethod_StockName_vs_Benchmark_
        Common_Prefix_CompletenessThreshold.csv  : 经过数据完备性筛选的个股系数列表
        Common_Prefix_CompletenessThreshold_PositiveCorrelation.csv  : 经过数据完备性筛选后正相关性最强的个股列表
        Common_Prefix_CompletenessThreshold_ZeroCorrelation.csv      : 经过数据完备性筛选后相关性最弱的个股列表
        Common_Prefix_CompletenessThreshold_NegativeCorrelation.csv  : 经过数据完备性筛选后负相关性最强的个股列表
        Common_Prefix_CompletenessThreshold_HistogramCorelation.csv  : 经过数据完备性筛选后相关性统计直方图

        Common_Prefix_CompletenessThreshold_PositiveBeta.csv   : 经过数据完备性筛选后正贝塔值最强的个股列表
        Common_Prefix_CompletenessThreshold_ZeroBeta.csv       : 经过数据完备性筛选后贝塔值最弱的个股列表
        Common_Prefix_CompletenessThreshold_NegativeBeta.csv   : 经过数据完备性筛选后负贝塔值最强的个股列表
        Common_Prefix_CompletenessThreshold_HistogramBeta.csv  : 经过数据完备性筛选后贝塔值统计直方图

        Common_Prefix_CompletenessThreshold_PositiveAlpha.csv  : 经过数据完备性筛选后正阿尔法值最强的个股列表
        Common_Prefix_CompletenessThreshold_ZeroAlpha.csv      : 经过数据完备性筛选后阿尔法值最弱的个股列表
        Common_Prefix_CompletenessThreshold_NegativeAlpha.csv  : 经过数据完备性筛选后负阿尔法值最强的个股列表
        Common_Prefix_CompletenessThreshold_HistogramAlpha.csv : 经过数据完备性筛选后阿尔法值统计直方图
    '''
    # Filter Stocks Based on Completeness Threshold
    if not filterCoefficient(postfix, completeness_threshold):
        return False

    # Calculate Top Number on Stock Correlation
    if not topCorrelation(postfix, completeness_threshold, top_number):
        return False

    # Calculate Histogram on Stock Correlation
    if not histogramCorrelation(postfix, completeness_threshold):
        return False

    # Calculate Top Number on Stock Beta
    if not topBeta(postfix, completeness_threshold, top_number):
        return False

    # Calculate Histogram on Stock Beta
    if not histogramBeta(postfix, completeness_threshold):
        return False

    # Calculate Top Number on Stock Alpha
    if not topAlpha(postfix, completeness_threshold, top_number):
        return False

    # Calculate Histogram on Stock Alpha
    if not histogramAlpha(postfix, completeness_threshold):
        return False

    return True

def filterCoefficient(postfix, completeness_threshold):
    # Load Coefficient File
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % postfix
    allcoef = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allcoef):
        print('Require Coefficient AllCoef File: %s!' % fullpath)
        return False

    # Filter Out Stocks without Sufficient Data
    threshold = float(completeness_threshold.replace('%',''))
    allcoef['completeness'] = allcoef['completeness'].map(lambda x: x.replace('%',''))
    allcoef['completeness'] = allcoef['completeness'].astype(float)
    allcoef = allcoef[allcoef.completeness >= threshold]
    allcoef['completeness'] = allcoef['completeness'].map(lambda x: ('%.2f' % (x)) + '%')
    allcoef.set_index('code',inplace=True)

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold])
    u.to_csv(allcoef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def loadCoefficient(postfix, completeness_threshold):
    # Load Coefficient File
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join([postfix, completeness_threshold])
    allcoef = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allcoef):
        print('Require Coefficient File: %s!' % fullpath)
        return None 

    return allcoef

def topCorrelation(postfix, completeness_threshold, top_number):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Statistics
    allcoef.set_index('code',inplace=True)
    allcoef['correlation_abs'] = allcoef['correlation'].map(lambda x: abs(x))
    allcoef['correlation_abs'] = allcoef['correlation_abs'].astype(float)
    negative_correlation = allcoef[allcoef.correlation < 0.0]
    positive_correlation = allcoef[allcoef.correlation > 0.0]
    zero_correlation = allcoef[allcoef.correlation_abs < 0.25]

    # Filter Out Top Number of Positive Correlation
    positive_correlation = positive_correlation.sort_values('correlation', axis=0, ascending=False)
    positive_correlation = positive_correlation[0:(top_number if len(positive_correlation) >= top_number else len(positive_correlation))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'PositiveCorrelation'])
    u.to_csv(positive_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Zero Correlation
    zero_correlation = zero_correlation.sort_values('correlation_abs', axis=0, ascending=True)
    zero_correlation = zero_correlation[0:(top_number if len(zero_correlation) >= top_number else len(zero_correlation))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'ZeroCorrelation'])
    u.to_csv(zero_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Negative Correlation
    negative_correlation = negative_correlation.sort_values('correlation', axis=0, ascending=True)
    negative_correlation = negative_correlation[0:(top_number if len(negative_correlation) >= top_number else len(negative_correlation))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'NegativeCorrelation'])
    u.to_csv(negative_correlation, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def histogramCorrelation(postfix, completeness_threshold):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Histogram
    columns = ['Total', 'Very Strong', 'Strong', 'Medium', 'Weak', 'Very Weak', 'Negative Very Weak', 'Negative Weak', 'Negative Medium', 'Negative Strong', 'Negative Very Strong']
    histogram = u.createDataFrame(1, columns, 0)
    stock_number = len(allcoef)
    histogram.ix[0, 'Total'] = stock_number
    for i in range(stock_number):
        correlation = allcoef.ix[i,'correlation']
        if correlation   > 0.8: # (0.8, 1.0]
            histogram.ix[0, 'Very Strong'] = histogram.ix[0, 'Very Strong'] + 1
        elif correlation > 0.6: # (0.6, 0.8]
            histogram.ix[0, 'Strong'] = histogram.ix[0, 'Strong'] + 1
        elif correlation > 0.4: # (0.4, 0.6]
            histogram.ix[0, 'Medium'] = histogram.ix[0, 'Medium'] + 1
        elif correlation > 0.2: # (0.2, 0.4]
            histogram.ix[0, 'Weak'] = histogram.ix[0, 'Weak'] + 1
        elif correlation >= 0.0:# [0.0, 0.2]
            histogram.ix[0, 'Very Weak'] = histogram.ix[0, 'Very Weak'] + 1
        elif correlation > -0.2:# (-0.2, 0.0)
            histogram.ix[0, 'Negative Very Weak'] = histogram.ix[0, 'Negative Very Weak'] + 1
        elif correlation > -0.4:# (-0.4, -0.2]
            histogram.ix[0, 'Negative Weak'] = histogram.ix[0, 'Negative Weak'] + 1
        elif correlation > -0.6:# (-0.6, -0.4]
            histogram.ix[0, 'Negative Medium'] = histogram.ix[0, 'Negative Medium'] + 1
        elif correlation > -0.8:# (-0.8, -0.6]
            histogram.ix[0, 'Negative Strong'] = histogram.ix[0, 'Negative Strong'] + 1
        else:                   # [-1.0, -0.8]
            histogram.ix[0, 'Negative Very Strong'] = histogram.ix[0, 'Negative Very Strong'] + 1

    # Save to CSV File
    histogram.set_index('Total', inplace=True)
    file_postfix = '_'.join([postfix, completeness_threshold, 'HistogramCorrelation'])
    u.to_csv(histogram, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def topBeta(postfix, completeness_threshold, top_number):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Statistics
    allcoef.set_index('code',inplace=True)
    allcoef['beta_abs'] = allcoef['beta'].map(lambda x: abs(x))
    allcoef['beta_abs'] = allcoef['beta_abs'].astype(float)
    negative_beta = allcoef[allcoef.beta < 0.0]
    positive_beta = allcoef[allcoef.beta > 0.0]
    zero_beta = allcoef[allcoef.beta_abs < 0.25]

    # Filter Out Top Number of Positive Beta
    positive_beta = positive_beta.sort_values('beta', axis=0, ascending=False)
    positive_beta = positive_beta[0:(top_number if len(positive_beta) >= top_number else len(positive_beta))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'PositiveBeta'])
    u.to_csv(positive_beta, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Zero Beta
    zero_beta = zero_beta.sort_values('beta_abs', axis=0, ascending=True)
    zero_beta = zero_beta[0:(top_number if len(zero_beta) >= top_number else len(zero_beta))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'ZeroBeta'])
    u.to_csv(zero_beta, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Negative Beta
    negative_beta = negative_beta.sort_values('beta', axis=0, ascending=True)
    negative_beta = negative_beta[0:(top_number if len(negative_beta) >= top_number else len(negative_beta))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'NegativeBeta'])
    u.to_csv(negative_beta, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def histogramBeta(postfix, completeness_threshold):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Histogram
    columns = ['Total', 'Very High', 'High', 'Medium', 'Low', 'Very Low', 'Negative Very Low', 'Negative Low', 'Negative Medium', 'Negative High', 'Negative Very High']
    histogram = u.createDataFrame(1, columns, 0)
    stock_number = len(allcoef)
    histogram.ix[0, 'Total'] = stock_number
    for i in range(stock_number):
        beta = allcoef.ix[i,'beta']
        if beta   >= 2.0: # [2.0, +Infinity)
            histogram.ix[0, 'Very High'] = histogram.ix[0, 'Very High'] + 1
        elif beta >= 1.5: # [1.5, 2.0)
            histogram.ix[0, 'High'] = histogram.ix[0, 'High'] + 1
        elif beta >= 1.0: # [1.0, 1.5)
            histogram.ix[0, 'Medium'] = histogram.ix[0, 'Medium'] + 1
        elif beta >= 0.5: # [0.5, 1.0)
            histogram.ix[0, 'Low'] = histogram.ix[0, 'Low'] + 1
        elif beta >= 0.0: # [0.0, 0.5)
            histogram.ix[0, 'Very Low'] = histogram.ix[0, 'Very Low'] + 1
        elif beta >= -0.5:# [-0.5, 0.0)
            histogram.ix[0, 'Negative Very Low'] = histogram.ix[0, 'Negative Very Low'] + 1
        elif beta >= -1.0:# [-1.0, -0.5)
            histogram.ix[0, 'Negative Low'] = histogram.ix[0, 'Negative Low'] + 1
        elif beta >= -1.5:# [-1.5, -1.0)
            histogram.ix[0, 'Negative Medium'] = histogram.ix[0, 'Negative Medium'] + 1
        elif beta >= -2.0:# [-2.0, -1.5)
            histogram.ix[0, 'Negative High'] = histogram.ix[0, 'Negative High'] + 1
        else:             # (-Infinity, -2.0)
            histogram.ix[0, 'Negative Very High'] = histogram.ix[0, 'Negative Very High'] + 1

    # Save to CSV File
    histogram.set_index('Total', inplace=True)
    file_postfix = '_'.join([postfix, completeness_threshold, 'HistogramBeta'])
    u.to_csv(histogram, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def topAlpha(postfix, completeness_threshold, top_number):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Statistics
    allcoef.set_index('code',inplace=True)
    allcoef['alpha_abs'] = allcoef['alpha'].map(lambda x: abs(x))
    allcoef['alpha_abs'] = allcoef['alpha_abs'].astype(float)
    negative_alpha = allcoef[allcoef.alpha < 0.0]
    positive_alpha = allcoef[allcoef.alpha > 0.0]
    zero_alpha = allcoef[allcoef.alpha_abs < 0.25]

    # Filter Out Top Number of Positive Alpha
    positive_alpha = positive_alpha.sort_values('alpha', axis=0, ascending=False)
    positive_alpha = positive_alpha[0:(top_number if len(positive_alpha) >= top_number else len(positive_alpha))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'PositiveAlpha'])
    u.to_csv(positive_alpha, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Zero Alpha
    zero_alpha = zero_alpha.sort_values('alpha_abs', axis=0, ascending=True)
    zero_alpha = zero_alpha[0:(top_number if len(zero_alpha) >= top_number else len(zero_alpha))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'ZeroAlpha'])
    u.to_csv(zero_alpha, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Filter Out Top Number of Negative Alpha
    negative_alpha = negative_alpha.sort_values('alpha', axis=0, ascending=True)
    negative_alpha = negative_alpha[0:(top_number if len(negative_alpha) >= top_number else len(negative_alpha))]

    # Save to CSV File
    file_postfix = '_'.join([postfix, completeness_threshold, 'NegativeAlpha'])
    u.to_csv(negative_alpha, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def histogramAlpha(postfix, completeness_threshold):
    # Load Coefficient File
    allcoef = loadCoefficient(postfix, completeness_threshold)
    if u.isNoneOrEmpty(allcoef):
        return False

    # Calculate Coefficient Histogram
    columns = ['Total', 'Very High', 'High', 'Medium', 'Low', 'Very Low', 'Negative Very Low', 'Negative Low', 'Negative Medium', 'Negative High', 'Negative Very High']
    histogram = u.createDataFrame(1, columns, 0)
    stock_number = len(allcoef)
    histogram.ix[0, 'Total'] = stock_number
    for i in range(stock_number):
        alpha = allcoef.ix[i,'alpha']
        if alpha   >= 0.4: # [0.4, +Infinity)
            histogram.ix[0, 'Very High'] = histogram.ix[0, 'Very High'] + 1
        elif alpha >= 0.3: # [0.3, 0.4)
            histogram.ix[0, 'High'] = histogram.ix[0, 'High'] + 1
        elif alpha >= 0.2: # [0.2, 0.3)
            histogram.ix[0, 'Medium'] = histogram.ix[0, 'Medium'] + 1
        elif alpha >= 0.1: # [0.1, 0.2)
            histogram.ix[0, 'Low'] = histogram.ix[0, 'Low'] + 1
        elif alpha >= 0.0: # [0.0, 0.1)
            histogram.ix[0, 'Very Low'] = histogram.ix[0, 'Very Low'] + 1
        elif alpha >= -0.1:# [-0.1, 0.0)
            histogram.ix[0, 'Negative Very Low'] = histogram.ix[0, 'Negative Very Low'] + 1
        elif alpha >= -0.2:# [-0.2, -0.1)
            histogram.ix[0, 'Negative Low'] = histogram.ix[0, 'Negative Low'] + 1
        elif alpha >= -0.3:# [-0.3, -0.2)
            histogram.ix[0, 'Negative Medium'] = histogram.ix[0, 'Negative Medium'] + 1
        elif alpha >= -0.4:# [-0.4, -0.3)
            histogram.ix[0, 'Negative High'] = histogram.ix[0, 'Negative High'] + 1
        else:              # (-Infinity, -0.4)
            histogram.ix[0, 'Negative Very High'] = histogram.ix[0, 'Negative Very High'] + 1

    # Save to CSV File
    histogram.set_index('Total', inplace=True)
    file_postfix = '_'.join([postfix, completeness_threshold, 'HistogramAlpha'])
    u.to_csv(histogram, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True