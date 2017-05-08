# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:59:58 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
import Common.GlobalSettings as gs

from Strategy.Common import loadAllStocks, samplePrice, ignoreData, checkPeriod

def strategyCoefficient(benchmark_id = '000300', date_start = '2015-01-01', date_end = '2016-12-31', period = 'M'):
    '''
    函数功能：
    --------
    按照给定起止时间和给定频率，计算全市场所有股票和业绩基准之间的Alpha/Beta/Correlation。
    假定：全市场股票列表，个股历史前复权数据，业绩基准历史前复权数据已经提前获取并存储为CSV文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'
    date_start : string, 起始日期 e.g. '2015-01-01'
    date_end : string, 终止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'

    输出参数：
    --------
    True/False : boolean, 策略运行是否完成

    数据文件
        Strategy_Coefficient_AllStock_Benchmark_DateStart_DateEnd_Period.csv : 参与系数计算的所有股票列表
        Strategy_Coefficient_AllPrice_Benchmark_DateStart_DateEnd_Period.csv : 与业绩基准时间对齐的所有股票价格
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_DateEnd_Period.csv  : 与业绩基准相参照的所有股票系数
    '''
    # Check Period
    period_types = ['W','M','Q']
    if not period in period_types:
        print('Un-supported period type - should be one of:', period_types)
        return False

    # Common Postfix
    common_postfix = '_'.join([benchmark_id, date_start, date_end, period])

    # Load All Stocks
    allstock = loadAllStocks()
    if u.isNoneOrEmpty(allstock):
        return False

    # Sample Prices
    allprice = samplePrice(benchmark_id, allstock, False, period)
    if u.isNoneOrEmpty(allprice):
        return False

    # Calculate Coefficients: Alpha, Beta, Correlation
    # For newly-IPO stocks, we need to ignore first 3-month trading.
    # And if the time-to-market date is less than one year, we will skip it when calculating coefficient.
    ignore_dict = {'M':3,'W':3*4,'D':3*4*5}
    min_period_dict = {'M':12,'W':12*4,'D':12*4*5}
    allcoef = calculateCoefficient(common_postfix, ignore_dict[period], min_period_dict[period]-ignore_dict[period])
    if u.isNoneOrEmpty(allcoef):
        return False

    return True

def calculateCoefficient(postfix, ignore_number, min_period_number):
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
        stock = allprice[column].copy()
        # Manually ignore a given number of valid data since IPO
        stock = ignoreData(stock, ignore_number)
        # Compute correlation with other Series, excluding missing values.
        # Set min_periods to avoid CXG whose IPO date is less than one year earlier.
        correlation = allprice['close'].corr(stock, min_periods=min_period_number)
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

###############################################################################

def analyzeCoefficient(postfix, completeness_threshold, top_number):
    '''
    函数功能：
    --------
    根据计算的系数文件，做进一步统计分析。
    假定：全市场股票相对于业绩基准的系数已经计算完成并存储为CSV文件。

    输入参数：
    --------
    postfix : string, 数据文件公共后缀 e.g. 000300_2015-01-01_2017-05-03_M, 即相对于沪深300自2015-01-01至2017-05-03月度数据。
    completeness_threshold : string, 起始日期 e.g. '80.00%', 即选取不少于80.00%的历史数据的个股做后续分析。
    top_number : int, 各类排行榜的入选个股数量 e.g. 20, 选取不多于20只个股。

    输出参数：
    --------
    True/False : boolean, 策略分析是否完成

    数据文件
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_DateEnd_Period_CompletenessThreshold.csv  : 经过数据完备性筛选的个股系数列表
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_DateEnd_Period_CompletenessThreshold_Positive_Correlation.csv  : 经过数据完备性筛选后正相关性最强的个股列表
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_DateEnd_Period_CompletenessThreshold_Zero_Correlation.csv      : 经过数据完备性筛选后相关性最弱的个股列表
        Strategy_Coefficient_AllCoef_Benchmark_DateStart_DateEnd_Period_CompletenessThreshold_Negative_Correlation.csv  : 经过数据完备性筛选后负相关性最强的个股列表
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

    return True

def filterCoefficient(postfix, completeness_threshold):
    # Load Coefficient File
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', postfix])
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
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold])
    u.to_csv(allcoef, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True

def topCorrelation(postfix, completeness_threshold, top_number):
    # Load Coefficient File
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold])
    allcoef = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allcoef):
        print('Require Coefficient AllCoef File: %s!' % fullpath)
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

    return True

def histogramCorrelation(postfix, completeness_threshold):
    # Load Coefficient File
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold])
    allcoef = u.read_csv(fullpath)
    if u.isNoneOrEmpty(allcoef):
        print('Require Coefficient AllCoef File: %s!' % fullpath)
        return False

    # Calculate Coefficient Histogram
    columns = ['Total', 'Very Strong', 'Strong', 'Medium', 'Weak', 'Very Weak', 'Negative Very Weak', 'Negative Weak', 'Negative Medium', 'Negative Strong', 'Negative Very Strong']
    histogram = u.createDataFrame(1, columns, 0)
    stock_number = len(allcoef)
    histogram.ix[0, 'Total'] = stock_number
    for i in range(stock_number):
        correlation = allcoef.ix[i,'correlation']
        if correlation > 0.8:   # (0.8, 1.0]
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
    file_postfix = '_'.join(['Coefficient', 'AllCoef', postfix, completeness_threshold, 'Correlation_Histogram'])
    u.to_csv(histogram, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    return True