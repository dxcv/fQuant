# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:45:52 2017

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
        tradeDate (datetime): 进行移动的日期,默认为调用当天
        day (int): 前后漂移的交易日的个数，正数向后移，负数向前移
    Returns:
        datetime: 移动后的日期

    Examples:
        >> tradeDate = dt.datetime(year=2017,month=5,day=27)
        >> nextDate = moveDate(tradeDate, 1)
        >> prevDate = moveDate(tradeDate, -1)
    """
    tradeDate = tradeDate if tradeDate is not None else dt.datetime.now()
    period = str(day) + 'B'
    return cal.advanceDate(tradeDate, period)

def removeST(stocks, st_date):
    """
    stocks: list, [secID]
    st_date: string, '%Y%m%d'
    """
    df_st = DataAPI.SecSTGet(secID=stocks, beginDate=st_date, endDate=st_date, field=['secID','STflg'], pandas='1')
    return [s for s in stocks if s not in list(df_st['secID'])]

def removeStopTrading(stocks, open_date):
    """
    stocks: list, [secID]
    open_date: string, '%Y%m%d'
    """
    df_open = DataAPI.MktEqudGet(secID=stocks, tradeDate=open_date, field=['secID','isOpen'],pandas='1')
    df_open = df_open[df_open['isOpen'] == 1]
    return [s for s in stocks if s in list(df_open['secID'])]

def filterTrades(wts, date, remove_st, remove_stop_trading):
    str_date = date.strftime('%Y%m%d')
    stocks = [s for s in wts]
    stocks = removeST(stocks, str_date) if remove_st else stocks
    stocks = removeStopTrading(stocks, str_date) if remove_stop_trading else stocks

    filtered_wts = {}
    for secID in wts:
        if secID in stocks:
            filtered_wts[secID] = wts[secID]

    return filtered_wts

def trade(account, wts):
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