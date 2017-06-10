# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:48:59 2017

@author: freefrom
"""

"""
简单择时策略：上涨趋势确认，全仓买入创业板成分股；下跌趋势确认，空仓。

分成四个周期：
全周期测试：2010-06-01 到 2017-04-30。
近周期测试：2015-01-01 到 2017-04-30。
中周期测试：2013-01-01 到 2014-12-31。
远周期测试：2010-06-01 到 2012-12-31。
"""

import numpy as np
import pandas as pd
import datetime as dt

timing_fn = 'Timing/Timing_Index_399006_0.33.csv'

def my_initialize(account):                   # 初始化虚拟账户状态
    account.timing = pd.read_csv(timing_fn, encoding='gbk', dtype=str)
    account.timing_index = 0
    account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y-%m-%d')
    while (account.timing_date < dt.datetime.strptime(start,'%Y-%m-%d')) and (account.timing_index < len(account.timing)-1):
        account.timing_index += 1
        account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y-%m-%d')
    account.timing_trend = account.timing.ix[account.timing_index,'trend']

def my_handle_data(account):                  # 每个交易日的买入卖出指令
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
            weight = 0.0
            for secID in account.security_position:
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
                    order(secID, amount-position)
                    #log.debug(u'%s股票%s' % (u'买入' if (amount-position) > 0 else u'卖出', secID))

        # 更新到下一择时调仓日
        if account.timing_index < len(account.timing)-1:
            account.timing_index += 1
            account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y-%m-%d')
            account.timing_trend = account.timing.ix[account.timing_index,'trend']

###############################################################################

"""
择时策略全周期调试代码

测试择时调仓日、趋势和下一调仓日更新
"""

import numpy as np
import pandas as pd
import datetime as dt

start = '2010-06-01'                       # 回测起始时间
end = '2017-04-30'                         # 回测结束时间
benchmark = '399006.ZICN'                  # 策略参考标准
universe = DynamicUniverse('CYB')          # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    my_initialize(account)

def handle_data(account):                  # 每个交易日的买入卖出指令
    today = account.current_date
    universe = account.universe
    if today == account.timing_date:       # 择时调仓日
        # 输出日志
        log.debug(u'择时调仓日，%s' % account.timing_trend)
        
        # 更新到下一择时调仓日
        if account.timing_index < len(account.timing)-1:
            account.timing_index += 1
            account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y-%m-%d')
            account.timing_trend = account.timing.ix[account.timing_index,'trend']

###############################################################################

"""
择时策略全周期测试：2010-06-01 到 2017-04-30
"""

start = '2010-06-01'                       # 回测起始时间
end = '2017-04-30'                         # 回测结束时间
benchmark = '399006.ZICN'                  # 策略参考标准
universe = DynamicUniverse('CYB')          # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    my_initialize(account)

def handle_data(account):                  # 每个交易日的买入卖出指令
    my_handle_data(account)


###############################################################################

"""
计算月度和季度回报
"""

import pandas as pd
import numpy as np

df = pd.DataFrame({'benchmark_cumulative_values' : perf['benchmark_cumulative_values'], 'cumulative_values' : perf['cumulative_values']})
df.index.name = 'date'
df.rename(columns={'benchmark_cumulative_values':'benchmark', 'cumulative_values':'fund'}, inplace=True)

def generateReturns(period = 'M'):
    df_resample = df.resample(period).last()
    df_resample['benchmark_return'] = np.nan
    df_resample['fund_return'] = np.nan
    df_resample['excess_return'] = np.nan

    for i in range(len(df_resample)):
        if i == 0:
            df_resample.ix[i,'benchmark_return'] = df_resample.ix[i,'benchmark'] - 1.0
            df_resample.ix[i,'fund_return'] = df_resample.ix[i,'fund'] - 1.0
        else:
            df_resample.ix[i,'benchmark_return'] = df_resample.ix[i,'benchmark']/df_resample.ix[i-1,'benchmark'] - 1.0
            df_resample.ix[i,'fund_return'] = df_resample.ix[i,'fund']/df_resample.ix[i-1,'fund'] - 1.0
        df_resample.ix[i,'excess_return'] = df_resample.ix[i,'fund_return'] - df_resample.ix[i,'benchmark_return']

    return df_resample

monthly_return = generateReturns('M')
fn = 'Timing/MonthlyReturn.csv'
monthly_return.to_csv(fn, encoding = 'gbk')

quarterly_return = generateReturns('Q')
fn = 'Timing/QuarterlyReturn.csv'
quarterly_return.to_csv(fn, encoding = 'gbk')

###############################################################################

"""
择时策略近周期测试：2015-01-01 到 2017-04-30
"""

start = '2015-01-01'                       # 回测起始时间
end = '2017-04-30'                         # 回测结束时间
benchmark = '399006.ZICN'                  # 策略参考标准
universe = DynamicUniverse('CYB')          # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    my_initialize(account)

def handle_data(account):                  # 每个交易日的买入卖出指令
    my_handle_data(account)

###############################################################################

"""
择时策略中周期测试：2013-01-01 到 2014-12-31
"""

start = '2013-01-01'                       # 回测起始时间
end = '2014-12-31'                         # 回测结束时间
benchmark = '399006.ZICN'                  # 策略参考标准
universe = DynamicUniverse('CYB')          # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    my_initialize(account)

def handle_data(account):                  # 每个交易日的买入卖出指令
    my_handle_data(account)

###############################################################################

"""
择时策略远周期测试：2010-06-01 到 2012-12-31
"""

start = '2010-06-01'                       # 回测起始时间
end = '2012-12-31'                         # 回测结束时间
benchmark = '399006.ZICN'                  # 策略参考标准
universe = DynamicUniverse('CYB')          # 证券池，支持股票和基金
capital_base = 100000000                   # 起始资金
commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')     # 手续费，印花税
slippage = Slippage(value=0.001, unit='perValue')                           # 买卖滑点
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    my_initialize(account)

def handle_data(account):                  # 每个交易日的买入卖出指令
    my_handle_data(account)

###############################################################################

"""
测试代码
"""

import datetime as dt
import pandas as pd

dt.datetime.strptime('2005/1/4','%Y/%m/%d')

d = {'000001.XSHE': 100, '600000.XSHG': 100}
print d['000001.XSHE']

timing = pd.read_csv('Timing/HS300_Timing_1.csv', encoding='gbk', dtype=str)
print timing
timing_index = 0
timing_date = dt.datetime.strptime(timing.ix[timing_index,'date'],'%Y/%m/%d')
timing_trend = timing.ix[timing_index,'trend']
print timing_date
print timing_trend
pd.read_csv('Timing/HS300_Timing_1_2006.csv', encoding='gbk', dtype=str)