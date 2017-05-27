# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:56:25 2017

@author: freefrom
"""

import numpy as np
import pandas as pd
import datetime as dt
from CAL.PyCAL import *
cal = Calendar('China.SSE')

def moveDate(tradeDate = None, day = -1):
    """
    给定某个日期，前后移动若干个交易日
    Args:
        tradeDate (string '%Y-%m-%d'): 进行移动的日期,默认为调用当天
        day (int): 前后漂移的交易日的个数，正数向后移，负数向前移
    Returns:
        datetime: 移动后的日期

    Examples:
        >> tradeDate = dt.datetime(year=2017,month=5,day=27)
        >> nextDate = moveDate(tradeDate, 1)
        >> prevDate = moveDate(tradeDate, -1)
    """
    tradeDate = dt.datetime.strptime(tradeDate,'%Y-%m-%d') if tradeDate is not None else dt.datetime.now()
    period = str(day) + 'B'
    return cal.advanceDate(tradeDate, period).strftime("%Y-%m-%d")

def dataToRatio(price, method):
    '''
    函数功能：
    --------
    对输入的价格序列，转换成涨跌幅。

    输入参数：
    --------
    price : pandas.Series, 价格序列。
    method : string, 比例计算方法。

    输出参数：
    --------
    ratio : pandas.Series, 处理后的价格序列。

    '''
    # Ignore Leading NaNs
    date_number = len(price)
    row = -1
    for i in range(date_number):
        if not np.isnan(price.ix[i]):
            row = i
            break
    # Calculate Ratio.
    ratio = price.copy()
    if row != -1:
        if method == 'P':
            for i in range(row, date_number):
                prev_price = price.ix[i] if i==row else price.ix[i-1]
                curr_price = price.ix[i]
                if not np.isnan(prev_price) and not np.isnan(curr_price): # Both are valid prices
                    ratio.ix[i] = (curr_price-prev_price)/prev_price # Turn price to ratio
                else: # One of them is invalid
                    ratio.ix[i] = np.nan
        elif method == 'B':
            base_price = price.ix[row]
            for i in range(row, date_number):
                curr_price = price.ix[i]
                if not np.isnan(curr_price): # Both are valid prices
                    ratio.ix[i] = (curr_price-base_price)/base_price # Turn price to ratio

    return ratio

def universeCorrelation(universe, benchmark, date, window, excess_return, corr_coef, corr_abs):
    """
    计算给定股票池universe，相对于业绩基准benchmark的相关性。
    计算周期为截止于date的window个交易日。
    """
    endDate = date
    beginDate = moveDate(endDate, -window)

    indexField=['indexID','tradeDate','closeIndex']
    stockField=['secID','tradeDate','closePrice','accumAdjFactor','isOpen']

    # Get Index History
    index_dict = {'HS300':'000300.ZICN'}
    indexID = index_dict[benchmark]
    index = DataAPI.MktIdxdGet(indexID=indexID,beginDate=beginDate,endDate=endDate,field=indexField,pandas="1")
    index_ratio = dataToRatio(index['closeIndex'],'B')

    # Calculate Stock Return and Excess Return
    stock_id = []
    stock_return = []
    stock_excess_return = []
    for stockID in universe:
        stock = DataAPI.MktEqudGet(secID=[stockID],beginDate=beginDate,endDate=endDate,field=stockField,pandas='1')
        stock_ratio = dataToRatio(stock['closePrice']*stock['accumAdjFactor'],'B')
        stock_id.append(stockID)
        stock_return.append(stock_ratio.ix[len(stock_ratio)-1] if len(stock_ratio) > 0 else np.nan)
        excess_return = stock_ratio.ix[len(stock_ratio)-1] - index_ratio.ix[len(index_ratio)-1] if len(stock_ratio) > 0 else np.nan
        stock_excess_return.append(excess_return)

    # Select Stocks with Positive (Excess) Return
    column_return = 'excess_return' if excess_return else 'return'
    df = pd.DataFrame({'code':stock_id, 'return':stock_return, 'excess_return':stock_excess_return})
    df = df[df[column_return] > 0.0]
    df = df.sort_values(column_return, axis=0, ascending=False).reset_index(drop=True)

    # Calculate Stock Correlation w.r.t. Benchmark
    df['correlation'] = np.nan
    df['corr_abs'] = np.nan
    for i in range(len(df)):
        stock_id = df.ix[i,'code']
        stock = DataAPI.MktEqudGet(secID=[stockID],beginDate=beginDate,endDate=endDate,field=stockField,pandas='1')
        stock_ratio = dataToRatio(stock['closePrice']*stock['accumAdjFactor'],'B')
        correlation = index_ratio.corr(stock_ratio)
        df.ix[i,'correlation'] = correlation
        df.ix[i,'corr_abs'] = np.abs(correlation)

    # Extract low correlation stocks
    column_corr = 'corr_abs' if corr_abs else 'correlation'
    low_corr_with_return = df[df[column_corr] < corr_coef].reset_index(drop=True)

    # Add Stock Name
    df['name'] = ''
    for i in range(len(low_corr_with_return)):
        stockID = low_corr_with_return.ix[i,'code']
        name = DataAPI.EquGet(secID=[stockID],field=['secShortName'],pandas='1').ix[0,'secShortName']
        low_corr_with_return.ix[i,'name'] = name
    print 'Universe Correlation Calculation Done! Select %d Stocks' % len(low_corr_with_return)
    return low_corr_with_return

###############################################################################

# Test Code

d = '2017-5-22'
w = 20
print (moveDate(d, -w))

###############################################################################

# Generate Stock Universe based on Correlation Strategy

universe = set_universe('HS300')
benchmark = 'HS300'
#date = '2017-05-19'
date = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')
window = 20
excess_return = False
corr_coef = 0.3
corr_abs = True

stocks = universeCorrelation(universe, benchmark, date, window, excess_return, corr_coef, corr_abs)
stocks = stocks.set_index('name')

csv_fn = '/'.join(['Correlation', '.'.join(['_'.join([benchmark,'Correlation',date]), 'csv'])])
excel_fn = '/'.join(['Correlation', '.'.join(['_'.join([benchmark,'Correlation',date]), 'xlsx'])])
stocks.to_csv(csv_fn,encoding='gbk')
stocks.to_excel(excel_fn,encoding='gbk')