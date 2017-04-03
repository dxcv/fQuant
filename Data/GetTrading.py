# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:55:29 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

import sys
sys.path.append('..')

from Data.Trading import get_daily_hfq
import Common.GlobalSettings as gs
import Common.Constants as c
import Common.Utilities as u

def getDailyHFQ(stock_id, is_index, date_start, date_end, time_to_market, incremental):
    hfq = None
    # For incremental update, use the next day of last update as the date start.
    if incremental:
        hfq = loadDailyHFQ(stock_id, is_index)
        if not u.isNoneOrEmpty(hfq):
            hfq.set_index('date',inplace=True)
            hfq.sort_index(ascending=True,inplace=True)
            last_day = hfq.index[len(hfq)-1]
            date_start = u.nextDayFromStr(last_day)

    # Download
    if gs.is_debug:
        print('Download Daily HFQ: %s, start=%s, end=%s' % (stock_id, u.dateToStr(date_start), u.dateToStr(date_end)))
    df = get_daily_hfq(stock_id=stock_id, is_index=is_index, date_start=date_start, 
                       date_end=date_end, time_to_market=time_to_market)
    if not u.isNoneOrEmpty(df):
        # Default df has 'date' set as index with type pandas.tslib.Timestamp,
        # so merged results will contain 00:00:00 along with date.
        # With below series of operation, index of df will be converted to type
        # str, thus avoid above issue.
        df.reset_index(inplace=True)
        df['date'] = df['date'].map(lambda x:str(x.date()))
        df.set_index('date',inplace=True)
        df.sort_index(ascending=True,inplace=True)

    # For incremental update, merge data
    if incremental:
        if (not u.isNoneOrEmpty(df)) and (not u.isNoneOrEmpty(hfq)):
            df = hfq.append(df)

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
    lshq.sort_values('date', ascending=True, inplace=True)
    if gs.is_debug:
        print(lshq.head(10))

    return lshq