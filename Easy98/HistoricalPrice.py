# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:29:14 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import pandas as pd
import numpy as np
import datetime as dt
import GlobalSettings as gs
import Utilities as u
import Constants as c

def get_quarterly_qfq(stock_id, is_index, year_start, year_end, time_to_market = None):
    '''
    函数功能：
    --------
    逐季度获取历史前复权数据，用于历史市盈率计算。
    
    输入参数：
    --------
    stock_id : string, 股票代码 e.g. 600036
    is_index : bool, 是否是指数 e.g. True
    year_start : int, 起始年度 e.g. 2005
    year_end : int, 终止年度 e.g. 2016
    time_to_market : datetime.date，上市日期 e.g. datetime.date(2005, 1, 1)
    
    输出参数：
    --------
    DataFrame
        date 季度截止日期 e.g. 2005-03-31
        open 季度开盘价
        high 季度最高价
        close 季度收盘价
        low 季度最低价
        volume 季度成交量
        amount 季度成交额
    
    '''

    # Check Input Parameters
    if not isinstance(stock_id, str) or not isinstance(is_index, bool) \
        or not isinstance(year_start, int) or not isinstance(year_end, int) \
        or not (time_to_market is None or isinstance(time_to_market, dt.date)):
        print('Incorrect type of one or more input parameters!')
        raise SystemExit

    if year_end < year_start:
        print('Start year should be no later than end year!')
        raise SystemExit

    # Prepare Daily Data Frame
    data_columns = ['open','high','close','low','volume','amount']
    data_columns_number = len(data_columns)
    data_index = []
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            quarter_date = u.quarterDate(year, quarter)
            data_index.append(quarter_date)
    if gs.is_debug:
        print(data_index)
    data_index_number = len(data_index)

    # Init all elements to NaN
    data_init = np.random.randn(data_index_number * data_columns_number)
    for i in range(data_index_number * data_columns_number):
        data_init[i] = np.nan
    df = pd.DataFrame(data_init.reshape(data_index_number, data_columns_number),
                      index = data_index, columns = data_columns)
    df.index.names = ['date']

    # Break start date and end date into quarters
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            quarter_start = dt.date(year, u.quarterStartMonth(quarter), u.quarterStartDay(quarter))
            quarter_end = dt.date(year, u.quarterEndMonth(quarter), u.quarterEndDay(quarter))

            # Optimization based on a valid time_to_market
            if not time_to_market is None:
                if quarter_start < time_to_market:
                    quarter_start = time_to_market
    
                if quarter_start > quarter_end:
                    continue

            # Fetch HFQ daily data for each quarter
            # Use HFQ and FQ_Factor to calculate QFQ daily data
            stock_data = ts.get_h_data(stock_id, index=is_index,
                                       start=quarter_start.strftime('%Y-%m-%d'),
                                       end=quarter_end.strftime('%Y-%m-%d'),
                                       autype='hfq', drop_factor=False)

            # Handle stop-trading quarter
            if stock_data is None or len(stock_data) == 0:
                index = u.quarterDate(year, quarter)
                for column in ['open','high','close','low','volume','amount']:
                    df.loc[index,column] = np.nan
            else: # Normal case - at least one trading day in the quarter
                if gs.is_debug:
                    print(stock_data.head(5))

                # Resample to quarterly based data
                period_type = 'Q'
                period_stock_data = stock_data.resample(period_type).first()
                if len(period_stock_data) == 0: # Ignore empty quarterly data
                    continue
                if gs.is_debug:
                    print(len(period_stock_data))

                period_stock_data['open']   = stock_data['open'].resample(period_type).first()
                period_stock_data['high']   = stock_data['high'].resample(period_type).max()
                period_stock_data['close']  = stock_data['close'].resample(period_type).last()
                period_stock_data['low']    = stock_data['low'].resample(period_type).min()
                period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()
                period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()
                period_stock_data['factor'] = stock_data['factor'].resample(period_type).last()

                # Fill data frame
                index = u.quarterDate(year, quarter)
                fq_factor = period_stock_data['factor'][0]
                for column in ['open','high','close','low']:
                    df.loc[index,column] = period_stock_data[column][0] / fq_factor
                df.loc[index, 'volume'] = period_stock_data['volume'][0] # Not touch it
                df.loc[index, 'amount'] = period_stock_data['amount'][0]

    # Return Dataframe
    return df

def calc_qfq(stock_id, period):
    '''
    函数功能：
    --------
    逐周期计算历史前复权数据，用于历史市盈率计算。
    假定：历史行情已经下载并存储成为CSV文件。

    输入参数：
    --------
    stock_id : string, 股票代码 e.g. 600036
    period : string, 重采样周期 e.g. 'W', 'M', 'Q'

    输出参数：
    --------
    DataFrame
        date 周期截止日期 e.g. 2005-03-31
        open 周期开盘价
        high 周期最高价
        close 周期收盘价
        low 周期最低价
        volume 周期成交量
        amount 周期成交额

    '''

    # Check Input Parameters
    if not isinstance(stock_id, str) or not isinstance(period, str):
        print('Incorrect type of one or more input parameters!')
        raise SystemExit

    # Check Period
    period_types = ['W','M','Q']
    if not period in period_types:
        print('Un-supported period type - should be one of:', period_types)
        raise SystemExit

    # Ensure Stock LSHQ Data File is Available
    if not u.hasFile(c.fullpath_dict['lshq'] % stock_id):
        print('Require LSHQ of Stock %s!' % stock_id)
        raise SystemExit

    df = u.read_csv(c.fullpath_dict['lshq'] % stock_id)
    df['date'] = df['date'].astype(np.datetime64)
    df.set_index('date', inplace=True)
    df.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(df.head(10))

    df_resample = df.resample(period).first()

    df_resample['open']   = df['open'].resample(period).first()
    df_resample['high']   = df['high'].resample(period).max()
    df_resample['close']  = df['close'].resample(period).last()
    df_resample['low']    = df['low'].resample(period).min()
    df_resample['volume'] = df['volume'].resample(period).sum()
    df_resample['amount'] = df['amount'].resample(period).sum()
    df_resample['factor'] = df['factor'].resample(period).last()

    df_resample_number = len(df_resample)
    for i in range(df_resample_number):
        fq_factor = df_resample.iloc[i]['factor']
        for column in ['open','high','close','low']:
            df_resample.iloc[i][column] = df_resample.iloc[i][column] / fq_factor
        df_resample.iloc[i]['volume'] = df_resample.iloc[i]['volume'] # Not touch it
        df_resample.iloc[i]['amount'] = df_resample.iloc[i]['amount']

    df_resample.drop('factor', axis=1, inplace=True)

    # Return Resampled Dataframe
    return df_resample

















