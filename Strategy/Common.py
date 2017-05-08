# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:04:42 2017

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

default_benchmark = '000300'

def updateCommonData():
    # Update All Stocks
    if not updateAllStocks():
        print('Update All Stocks Failed!')
        return False

    # Update All Index
    if not updateAllIndex():
        print('Update All Index Failed!')
        return False

    # Update Sample Price for All Stocks
    updateSamplePriceAllStocks(default_benchmark, 'M')

    # Update Sample Price for All Index
    updateSamplePriceAllIndex(default_benchmark, 'M')

    return True

def updateAllStocks():
    '''
    函数功能：
    --------
    更新所有股票列表。

    输入参数：
    --------
    无

    输出参数：
    --------
    True/False : boolean，是否更新成功。

    数据文件
        Strategy_Common_AllStock.csv : 参与策略计算的所有股票列表
    '''
    # Load from Fundamental Stock Basics
    allstock = loadStockBasics()
    if not u.isNoneOrEmpty(allstock):
        # Save to CSV File
        allstock.set_index('code',inplace=True)
        file_postfix = '_'.join(['Common', 'AllStock'])
        u.to_csv(allstock, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)
        return True

    return False

def updateAllIndex():
    '''
    函数功能：
    --------
    更新所有指数列表。

    输入参数：
    --------
    无

    输出参数：
    --------
    True/False : boolean，是否更新成功。

    数据文件
        Strategy_Common_AllIndex.csv : 参与策略计算的所有指数列表
    '''
    # Load from Constants.index_list
    allindex = pd.DataFrame({'code':c.index_list})
    if not u.isNoneOrEmpty(allindex):
        # Save to CSV File
        allindex.set_index('code',inplace=True)
        file_postfix = '_'.join(['Common', 'AllIndex'])
        u.to_csv(allindex, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)
        return True

    return False

def updateSamplePrice(benchmark_id, stock_ids, is_index, period):
    '''
    函数功能：
    --------
    根据基准指数的时间范围和采样周期，对指定股票/指数列表的收盘价格进行全采样。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'，隐含起止时间。
    period : string, 采样周期 e.g. 'M'，支持'D', 'W', and 'M'。

    输出参数：
    --------
    采样成功时，allprice : pandas.Series，采样结果。
    采样失败时，None
    '''
    # Load Benchmark
    benchmark = loadDailyQFQ(benchmark_id, is_index)
    if u.isNoneOrEmpty(benchmark):
        print('Require Benchmark LSHQ File: %s!', benchmark_id)
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
            print('Require Stock LSHQ File: %s!', stock_id)
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

    return allprice

def updateSamplePriceAllStocks(benchmark_id, period):
    '''
    函数功能：
    --------
    根据基准指数的时间范围和采样周期，对所有股票的收盘价格进行全采样。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'，隐含起止时间。
    period : string, 采样周期 e.g. 'M'，支持'D', 'W', and 'M'。

    输出参数：
    --------
    True/False : boolean，是否采样成功。

    数据文件
        Strategy_Common_AllPrice_Benchmark_Period_AllStock.csv : 所有股票收盘价格的采样结果数据文件。
    '''
    # Sample Price for All Stocks
    allstocks = loadAllStocks()
    benchmark_id = '000300'
    period = 'M'
    allprice = updateSamplePrice(benchmark_id, allstocks, False, period)

    # Save to CSV File
    if not u.isNoneOrEmpty(allprice):
        file_postfix = '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllStock'])
        u.to_csv(allprice, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)
        return True

    return False

def updateSamplePriceAllIndex(benchmark_id, period):
    '''
    函数功能：
    --------
    根据基准指数的时间范围和采样周期，对所有指数的收盘价格进行全采样。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'，隐含起止时间。
    period : string, 采样周期 e.g. 'M'，支持'D', 'W', and 'M'。

    输出参数：
    --------
    True/False : boolean，是否采样成功。

    数据文件
        Strategy_Common_AllPrice_Benchmark_Period_AllStock.csv : 所有指数收盘价格的采样结果数据文件。
    '''
    # Sample Price for All Index
    allindex = loadAllIndex()
    benchmark_id = '000300'
    period = 'M'
    allprice = updateSamplePrice(benchmark_id, allindex, True, period)

    # Save to CSV File
    if not u.isNoneOrEmpty(allindex):
        file_postfix = '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllIndex'])
        u.to_csv(allprice, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)
        return True

    return False

###############################################################################

def loadAllStocks():
    '''
    函数功能：
    --------
    加载所有股票列表。

    输入参数：
    --------
    无

    输出参数：
    --------
    加载成功时，stock_ids : pandas.Series, 所有股票列表。
    加载失败时，None
    '''
    # Load Local Cache
    file_postfix = '_'.join(['Common', 'AllStock'])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allstock = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allstock):
        return allstock['code']

    print('Failed to Load File: %s !' % fullpath)
    return None

def loadAllIndex():
    '''
    函数功能：
    --------
    加载所有指数列表。

    输入参数：
    --------
    无

    输出参数：
    --------
    加载成功时，index_ids : pandas.Series, 所有指数列表。
    加载失败时，None
    '''
    # Load Local Cache
    file_postfix = '_'.join(['Common', 'AllIndex'])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allindex = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allindex):
        return allindex['code']

    print('Failed to Load File: %s !' % fullpath)
    return None

def loadSamplePriceAllStocks(benchmark_id, period):
    '''
    函数功能：
    --------
    根据基准指数的时间范围和采样周期，加载所有股票的收盘价格采样文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'，隐含起止时间。
    period : string, 采样周期 e.g. 'M'，支持'D', 'W', and 'M'。

    输出参数：
    --------
    加载成功时，allprice : pandas.DataFrame, 所有股票的收盘价格采样结果。
    加载失败时，None
    '''
    # Check if AllPrice File Already Exists
    file_postfix = '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllStock'])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allprice = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allprice):
        return allprice

    print('Failed to Load File: %s !' % fullpath)
    return None

def loadSamplePriceAllIndex(benchmark_id, period):
    '''
    函数功能：
    --------
    根据基准指数的时间范围和采样周期，加载所有指数的收盘价格采样文件。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'，隐含起止时间。
    period : string, 采样周期 e.g. 'M'，支持'D', 'W', and 'M'。

    输出参数：
    --------
    加载成功时，allprice : pandas.DataFrame, 所有指数的收盘价格采样结果。
    加载失败时，None
    '''
    # Check if AllPrice File Already Exists
    file_postfix = '_'.join(['Common', 'AllPrice', benchmark_id, period, 'AllIndex'])
    fullpath = c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix
    allprice = u.read_csv(fullpath)
    if not u.isNoneOrEmpty(allprice):
        return allprice

    print('Failed to Load File: %s !' % fullpath)
    return None

###############################################################################

def samplePrice(benchmark_id, stock_ids, is_index, date_begin, date_end, period):
    '''
    函数功能：
    --------
    根据基准指数，起止时间和采样周期，对指定股票/指数列表进行收盘价格采样。

    输入参数：
    --------
    benchmark_id : string, 指数代码 e.g. '000300'。
    stock_ids : pandas.Series or list, 股票/指数列表 e.g. ['600016']
    is_index : boolean, 股票/指数标示 e.g. True
    date_begin : string, 起始日期 e.g. '2005-01-01'
    date_end : string, 截止日期 e.g. '2016-12-31'
    period : string, 采样周期 e.g. 'M'

    输出参数：
    --------
    采样成功时，sampleprice : pandas.DataFrame, 指定股票/指数列表的收盘价格采样结果。
    采样失败时，None
    '''
    # Load All Security and Filter Input stock_ids with Existed Ones.
    filtered_security_ids = []
    all_security = list(loadAllIndex() if is_index else loadAllStocks())
    security_number = len(stock_ids)
    for i in range(security_number):
        security_id = stock_ids[i]
        if security_id in all_security:
            filtered_security_ids.append(security_id)

    # Extract Price for Filtered Security
    all_price = loadSamplePriceAllIndex(default_benchmark, period) if is_index else loadSamplePriceAllStocks(default_benchmark, period)
    column_dict = {}
    filtered_stock_number = len(filtered_security_ids)
    for i in range(filtered_stock_number):
        security_id = u.stockID(filtered_security_ids[i])
        column_dict[security_id] = all_price['close_'+security_id]
    sample_price = pd.DataFrame(column_dict)

    # Filter by date_begin and date_end
    sample_price = sample_price[sample_price.date >= date_begin and sample_price.date <= date_end]

    return sample_price

###############################################################################

def ignoreData(price, ignore_number):
    '''
    函数功能：
    --------
    对输入的价格序列，忽略给定数目的价格采样数据。
    假定价格序列已经按照时间升序排好序。

    输入参数：
    --------
    price : pandas.Series, 价格序列。
    ignore_number : int, 忽略的价格采样数据的数目。

    输出参数：
    --------
    price : pandas.Series, 处理后的价格序列。

    '''
    # Find first valid data, assuming it has been sorted by date ascendingly.
    date_number = len(price)
    row = -1
    for j in range(date_number):
        if not np.isnan(price.ix[j]):
            row = j
            break
    if row != -1:
        for j in range(row, row+ignore_number if row+ignore_number <= date_number else date_number):
            price.ix[j] = np.nan

    return price

def fillMissingData(price):
    '''
    函数功能：
    --------
    对输入的价格序列，填充缺失的价格采样数据。
    假定价格序列已经按照时间升序排好序。

    输入参数：
    --------
    price : pandas.Series, 价格序列。

    输出参数：
    --------
    price : pandas.Series, 处理后的价格序列。

    '''
    # Ignore Leading NaNs
    date_number = len(price)
    row = -1
    for i in range(date_number):
        if not np.isnan(price.ix[i]):
            row = i
            break
    # Fill missed data by previous valid data.
    if row != -1:
        for i in range(row+1, date_number):
            if np.isnan(price.ix[i]):
                price.ix[i] = price.ix[i-1]

    return price

def checkPeriod(period):
    '''
    函数功能：
    --------
    检查是否是支持的时间周期：'W','M','Q'。

    输入参数：
    --------
    period : string, e.g. 'W', 时间周期。

    输出参数：
    --------
    True/False : boolean，是否支持。

    '''
    period_types = ['W','M','Q']
    if not period in period_types:
        print('Un-supported period type - should be one of:', period_types)
        return False

    return True