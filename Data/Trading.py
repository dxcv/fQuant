# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:22:35 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import datetime as dt

def get_daily_hfq(stock_id, is_index, date_start, date_end, time_to_market = None):
    '''
    函数功能：
    --------
    逐日获取历史后复权数据。

    输入参数：
    --------
    stock_id : string, 股票代码 e.g. 600036
    is_index : bool, 是否是指数 e.g. True
    date_start : datetime.date, 起始日期 e.g. datetime.date(2005, 1, 1)
    date_end : datetime.date, 终止日期 e.g. datetime.date(2016, 12, 31)
    time_to_market : datetime.date，上市日期 e.g. datetime.date(2005, 1, 1)

    输出参数：
    --------
    DataFrame
        date 日期 e.g. 2005-03-31
        open 开盘价
        high 最高价
        close 收盘价
        low 最低价
        volume 成交量
        amount 成交额
        factor 复权因子

    如果没有数据，返回None
    如果输入为指数，factor（复权因子）一列统一为1.00
    '''

    # Check Input Parameters
    if not isinstance(stock_id, str) or not isinstance(is_index, bool) \
        or not isinstance(date_start, dt.date) or not isinstance(date_end, dt.date) \
        or not (time_to_market is None or isinstance(time_to_market, dt.date)):
        print('Incorrect type of one or more input parameters!')
        raise SystemExit

    if date_end < date_start:
        print('Start date should be no later than end date!')
        raise SystemExit

    # Optimization based on a valid time_to_market
    if (not time_to_market is None) and (date_start < time_to_market):
        date_start = time_to_market # Shift date_start to time_to_market
        if date_end < date_start: # Empty date range
            return None

    # Fetch HFQ daily data
    stock_data = ts.get_h_data(stock_id, index=is_index,
                               start=date_start.strftime('%Y-%m-%d'),
                               end=date_end.strftime('%Y-%m-%d'),
                               autype='hfq', drop_factor=False)

    # Handle no data availabe cases (e.g. stop trading)
    if stock_data is None or len(stock_data) == 0:
        return None

    # Add FQ_Factor for index
    if is_index:
        stock_data['factor'] = '1.00'

    # Return Dataframe
    return stock_data


























