# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:55:29 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Trading import get_daily_hfq
import GlobalSettings as gs
import Constants as c
import Utilities as u

def getDailyHFQ(stock_id, is_index, date_start, date_end, time_to_market = None):
    # Download
    df = get_daily_hfq(stock_id=stock_id, is_index=is_index, date_start=date_start, 
                       date_end=date_end, time_to_market=time_to_market)
    df.sort_index(ascending=True,inplace=True) # date is set to index
    if gs.is_debug:
        print(df.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(df):
        u.to_csv(df, c.path_dict['lshq'], c.file_dict['lshq'] % u.stockFileName(stock_id, is_index))

def loadDailyHFQ(stock_id, is_index):
    fullpath = c.fullpath_dict['lshq'] % u.stockFileName(stock_id, is_index)

    # Ensure data file is available
    if not u.hasFile(fullpath):
        print('Require LSHQ of %s!' % u.stockFileName(stock_id, is_index))
        return None

    # Read data file
    df = u.read_csv(fullpath)
    return df

def validDailyHFQ(stock_id, is_index, force_update):
    if force_update == True:
        return False

    else:
        return u.hasFile(c.fullpath_dict['lshq'] % u.stockFileName(stock_id, is_index))

def loadDailyQFQ(stock_id, is_index):
    """
        加载股票日线数据，并进行前复权
    Parameters
    --------
    stock_id:string    股票代码 e.g. 600036
    is_index:bool      是否指数 e.g. True/False

    Return
    --------
    DataFrame
        date 日期 e.g. 2005-03-31
        open 开盘价
        high 最高价
        close 收盘价
        low 最低价
        volume 成交量
        amount 成交额

    如果数据文件不存在或者没有数据，返回None。
    如果数据存在，根据复权因子进行前复权，同时根据date进行升序排序。
    """
    # Load HFQ(LSHQ) Data
    lshq = loadDailyHFQ(stock_id, is_index)
    if u.isNoneOrEmpty(lshq):
        print('No LSHQ Data Available!')
        return None

    # Convert to QFQ Data
    lshq_number = len(lshq)
    fq_factor = lshq['factor'][lshq_number-1]
    for i in range(lshq_number):
        for column in ['open','high','close','low']:
            lshq.ix[i, column] = lshq.ix[i, column] / fq_factor

    # Drop Factor
    lshq.drop('factor', axis=1, inplace=True)

    # Sort Index
    lshq.sort_values('date', inplace=True)
    if gs.is_debug:
        print(lshq.head(10))

    return lshq