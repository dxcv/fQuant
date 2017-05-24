# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:38:28 2017

@author: freefrom
"""

import numpy as np
import pandas as pd

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

###############################################################################

import numpy as np
import pandas as pd
import datetime as dt

def universeCorrelation(universe, benchmark, date, window = 30):
    endDate = dt.datetime.strptime(date,'%Y-%m-%d')
    beginDate = endDate + dt.timedelta(days=-30)

    beginDate=dt.datetime.strftime(beginDate,'%Y-%m-%d')
    endDate=dt.datetime.strftime(endDate,'%Y-%m-%d')

    indexField=['indexID','tradeDate','closeIndex','CHGPct']
    stockField=['secID','tradeDate','closePrice','chgPct','accumAdjFactor','PE','PE1','isOpen']

    # Get Index History
    index = DataAPI.MktIdxdGet(indexID=indexList,beginDate=beginDate,endDate=endDate,field=indexField,pandas="1")
    index_ratio = dataToRatio(index['closeIndex'],'B')

    # Calculate Stock Correlation w.r.t. Index
    stock_id = []
    stock_name = []
    stock_correlation = []
    stock_corr_abs = []
    stock_return = []
    stock_excess_return = []
    for stockID in universe:
        stock = DataAPI.MktEqudGet(secID=[stockID],beginDate=start,endDate=end,field=stockField,pandas='1')
        name = DataAPI.EquGet(secID=[stockID],field=['secShortName'],pandas='1').ix[0,'secShortName']
        stock_ratio = dataToRatio(stock['closePrice'],'B')
        correlation = index_ratio.corr(stock_ratio)
        stock_id.append(stockID)
        stock_name.append(name)
        stock_correlation.append(correlation)
        stock_corr_abs.append(np.abs(correlation))
        stock_return.append(stock_ratio.ix[len(stock_ratio)-1] if len(stock_ratio) > 0 else np.nan)
        excess_return = stock_ratio.ix[len(stock_ratio)-1] - index_ratio.ix[len(index_ratio)-1] if len(stock_ratio) > 0 else np.nan
        stock_excess_return.append(excess_return)
        #print 'Correlation (%s vs. %s/%s) = %f' % (indexList[0], stockID, name, correlation)

    df = pd.DataFrame({'code':stock_id, 'name':stock_name, 'correlation':stock_correlation, 'corr_abs':stock_corr_abs, 'return':stock_return, 'excess_return':stock_excess_return})
    df = df.sort_values('corr_abs', axis=0, ascending=True).reset_index(drop=True)

    # Extrace low correlation stocks and sort by excess return
    low_corr = df[df['corr_abs'] < 0.3]
    low_corr = low_corr.sort_values('excess_return', axis=0, ascending=False).reset_index(drop=True)
    low_corr_with_return = low_corr[low_corr['excess_return'] > 0.0]

    print 'Universe Correlation Calculation Done!'
    return low_corr_with_return

universe = set_universe('HS300')
date = '2017-05-19'
#date = dt.datetime.strftime(dt.date.today(),'%Y-%m-%d')

stocks = universeCorrelation(universe, 'HS300', date)
stocks = stocks.set_index('code')

csv_fn = '.'.join(['_'.join(['HS300','Correlation',date]), 'csv'])
excel_fn = '.'.join(['_'.join(['HS300','Correlation',date]), 'xlsx'])
stocks.to_csv(csv_fn,encoding='gbk')
stocks.to_excel(excel_fn,encoding='gbk')

###############################################################################

import numpy as np
import pandas as pd
import datetime as dt

start = '2006-01-01'                       # 回测起始时间
end = '2017-04-30'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
universe = DynamicUniverse('HS300')        # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    account.timing = pd.read_csv('Timing/HS300_Timing_1_2006.csv', encoding='gbk', dtype=str)
    account.timing_index = 0
    account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y/%m/%d')
    while (account.timing_date < dt.datetime.strptime(start,'%Y-%m-%d')) and (account.timing_index < len(account.timing)-1):
        account.timing_index += 1
        account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y/%m/%d')
    account.timing_trend = account.timing.ix[account.timing_index,'trend']

def handle_data(account):                  # 每个交易日的买入卖出指令
    today = account.current_date
    universe = account.universe
    if today == account.timing_date:       # 择时调仓日
        # 输出日志
        log.debug(u'择时调仓日，%s' % account.timing_trend)

        # 根据趋势来调仓
        wts = {}
        if account.timing_trend == 'Up':
            secNumber = len(account.universe)
            weight = 1.0 / float(secNumber) if secNumber > 0 else 0.0
            for secID in account.universe:
                wts[secID] = weight
        else:
            yesterday = dt.datetime.strftime(account.previous_date,'%Y-%m-%d')
            stocks = universeCorrelation(account.current_universe, benchmark, yesterday, window = 30)
            stocks = stocks['code'].tolist()
            secNumber = len(stocks)
            weight = 1.0 / float(secNumber) if secNumber > 0 else 0.0
            for secID in stocks:
                wts[secID] = weight

        # 交易
        for secID in wts:
            weight = wts[secID]
            price = account.reference_price[secID] if (secID in account.reference_price) else 0.0
            if price > 0.0:
                amount = weight * account.reference_portfolio_value
                amount = np.round(amount / price, decimals=-2)
                position = account.security_position[secID] if (secID in account.security_position) else 0.0
                if np.abs(amount-position) > 0.0:
                    order(secID,amount-position)
                    #log.debug(u'%s股票%s' % (u'买入' if (amount-position) > 0 else u'卖出', secID))

        # 更新到下一择时调仓日
        if account.timing_index < len(account.timing)-1:
            account.timing_index += 1
            account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y/%m/%d')
            account.timing_trend = account.timing.ix[account.timing_index,'trend']