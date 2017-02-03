# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:34:06 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import pandas as pd
import numpy as np
import datetime as dt
import DateUtility as du
import ConstantData as cd
import StockUtility as su

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
        path/StockData_QuarterlyQFQ_stock_id.csv
    
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
            quarter_date = du.quarterDate(year, quarter)
            data_index.append(quarter_date)
    if cd.is_debug:
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
            quarter_start = dt.date(year, du.quarterStartMonth(quarter), du.quarterStartDay(quarter))
            quarter_end = dt.date(year, du.quarterEndMonth(quarter), du.quarterEndDay(quarter))

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
                index = du.quarterDate(year, quarter)
                for column in ['open','high','close','low','volume','amount']:
                    df.loc[index,column] = np.nan
            else: # Normal case - at least one trading day in the quarter
                if cd.is_debug:
                    print(stock_data.head(5))

                # Resample to quarterly based data
                period_type = 'Q'
                period_stock_data = stock_data.resample(period_type).first()
                if len(period_stock_data) == 0: # Ignore empty quarterly data
                    continue
                if cd.is_debug:
                    print(len(period_stock_data))

                period_stock_data['open']   = stock_data['open'].resample(period_type).first()
                period_stock_data['high']   = stock_data['high'].resample(period_type).max()
                period_stock_data['close']  = stock_data['close'].resample(period_type).last()
                period_stock_data['low']    = stock_data['low'].resample(period_type).min()
                period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()
                period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()
                period_stock_data['factor'] = stock_data['factor'].resample(period_type).last()

                # Fill data frame
                index = du.quarterDate(year, quarter)
                fq_factor = period_stock_data['factor'][0]
                for column in ['open','high','close','low']:
                    df.loc[index,column] = period_stock_data[column][0] / fq_factor
                df.loc[index, 'volume'] = period_stock_data['volume'][0] # Not touch it
                df.loc[index, 'amount'] = period_stock_data['amount'][0]

    # Return Dataframe
    return df

#
# Get Quarterly QFQ Parameters
#
stock_ids  = ['300059','600036','000002','002024']
is_indexs  = [False,False,False,False]
year_start = 2005
year_end   = 2016

#
# Load Stock Basics
#
basics = su.loadStockBasics()

#
# Iterate Over All Stocks
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    is_index = is_indexs[i]

    # Extract Stock Time-to-Market
    date_timeToMarket = su.timeToMarket(stock_basics = basics, stock_id = stock_id)
    df = get_quarterly_qfq(stock_id = stock_id, is_index = is_index, year_start = year_start,
                           year_end = year_end, time_to_market = date_timeToMarket)

    # Save to CSV File
    df.to_csv(cd.path_datacenter + (cd.file_quarterlyqfq % stock_id), encoding='utf-8')

























