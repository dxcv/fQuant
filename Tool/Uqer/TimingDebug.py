# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:04:37 2017

@author: freefrom
"""

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
        
        # 更新到下一择时调仓日
        if account.timing_index < len(account.timing)-1:
            account.timing_index += 1
            account.timing_date = dt.datetime.strptime(account.timing.ix[account.timing_index,'date'],'%Y/%m/%d')
            account.timing_trend = account.timing.ix[account.timing_index,'trend']