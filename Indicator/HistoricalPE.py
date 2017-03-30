# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 23:00:24 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd
import numpy as np
import Utilities as u
import Constants as c
import GlobalSettings as gs

def calc_hpe_quarterly(stock_id, year_start, year_end):
    '''
    函数功能：
    --------
    逐季度计算历史市盈率。
    假定：逐季度历史前复权数据，以及逐季度每股收益已经提前获取并存储为CSV文件。

    输入参数：
    --------
    stock_id : string, 股票代码 e.g. 600036
    year_start : int, 起始年度 e.g. 2005
    year_end : int, 终止年度 e.g. 2016

    输出参数：
    --------
    DataFrame
        date 季度截止日期 e.g. 2005-03-31
        close 季度收盘价
        high 季度最高价
        low 季度最低价
        eps 季度末每股收益（可能有数据缺失）
        eps_filled 根据临近季度推算出的，缺失的季度末每股收益
        eps_rolling 根据季度末每股收益（含推算），折算的年度预期每股收益
        pe_close 根据季度收盘价，计算出的市盈率
        pe_high 根据季度最高价，计算出的市盈率
        pe_low 根据季度最低价，计算出的市盈率

    '''

    # Check Input Parameters
    if not isinstance(stock_id, str) \
        or not isinstance(year_start, int) or not isinstance(year_end, int):
        print('Incorrect type of one or more input parameters!')
        raise SystemExit

    if not (year_start <= year_end):
        print('Start year should be no later than end year!')
        raise SystemExit

    # Fetch Stock Data
    stock_data = u.read_csv(c.fullpath_dict['qfq_q'] % stock_id)
    stock_data_number = len(stock_data)
    if stock_data_number != (year_end - year_start + 1)*4:
        print('The duration of tock data does not match the duration of analysis!')
        raise SystemExit

    stock_data.set_index('date', inplace=True)
    stock_data.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(stock_data.head(10))

    # Handle stop-trading quarter (by filling with previous quarter data)
    # Assume: stock data has been sorted ascendingly by date.
    for i in range(stock_data_number):
        if i > 0 and np.isnan(stock_data.iloc[i]['close']):
            if gs.is_debug:
                print('close = ', stock_data.iloc[i]['close'])
            if np.isnan(stock_data.iloc[i-1]['close']): # Ignore leading stop-trading quarters
                continue
            else: # Regular internal stop-trading quarters
                for column in stock_data.columns:
                    stock_data.iloc[i][column] = stock_data.iloc[i-1][column]

    # Fetch Report Data
    report_data = u.read_csv(c.fullpath_dict['finsum'] % stock_id)
    report_data.set_index('date', inplace=True)
    report_data.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(report_data.head(10))

    # Join Stock Data and Report Data (Assume Stock Data is the reference)
    hpe_columns = ['close','high','low','eps','eps_filled','eps_rolling',
                   'pe_close','pe_high','pe_low']
    hpe_columns_number = len(hpe_columns)
    hpe_index_number = stock_data_number

    # Init all elements to NaN
    data_init = np.random.randn(hpe_index_number * hpe_columns_number)
    for i in range(hpe_index_number * hpe_columns_number):
        data_init[i] = np.nan
    hpe = pd.DataFrame(data_init.reshape(hpe_index_number, hpe_columns_number),
                       index = stock_data.index, columns = hpe_columns)

    # Inherite close/high/low from stock data, and eps from report data
    for i in range(hpe_index_number):
        for column in ['close','high','low']:
            hpe.iloc[i][column] = stock_data.iloc[i][column]
        index = hpe.index[i]
        if index in report_data.index: # Has EPS data
            hpe.iloc[i]['eps']   = report_data.loc[index, 'eps']
        else: # Missing EPS data
            hpe.iloc[i]['eps']   = np.nan

    # Fill the Missing EPS Data
    for year in range(year_start, year_end+1):
        index_q1 = u.quarterDateStr(year, 1)
        index_q2 = u.quarterDateStr(year, 2)
        index_q3 = u.quarterDateStr(year, 3)
        index_q4 = u.quarterDateStr(year, 4)
        eps_q1 = hpe.loc[index_q1, 'eps']
        eps_q2 = hpe.loc[index_q2, 'eps']
        eps_q3 = hpe.loc[index_q3, 'eps']
        eps_q4 = hpe.loc[index_q4, 'eps']
        if gs.is_debug:
            print('eps_q1 =', eps_q1, 'eps_q2 =', eps_q2, 'eps_q3 =', eps_q3, 'eps_q4 =', eps_q4)

        eps_q1_filled = eps_q1
        eps_q2_filled = eps_q2
        eps_q3_filled = eps_q3
        eps_q4_filled = eps_q4

        if (np.isnan(eps_q1)):
            if   (not np.isnan(eps_q2)):
                eps_q1_filled = eps_q2 * 0.5
            elif (not np.isnan(eps_q3)):
                eps_q1_filled = eps_q3 * 0.3333333333333333
            elif (not np.isnan(eps_q4)):
                eps_q1_filled = eps_q4 * 0.25
        if (np.isnan(eps_q2)):
            if   (not np.isnan(eps_q1)):
                eps_q2_filled = eps_q1 * 2.0
            elif (not np.isnan(eps_q3)):
                eps_q2_filled = eps_q3 * 0.6666666666666667
            elif (not np.isnan(eps_q4)):
                eps_q2_filled = eps_q4 * 0.5
        if (np.isnan(eps_q3)):
            if (not np.isnan(eps_q2)):
                eps_q3_filled = eps_q2 * 1.5
            elif (not np.isnan(eps_q1)):
                eps_q3_filled = eps_q1 * 3.0
            elif (not np.isnan(eps_q4)):
                eps_q3_filled = eps_q4 * 0.75
        if (np.isnan(eps_q4)):
            if (not np.isnan(eps_q3)):
                eps_q4_filled = eps_q3 * 1.333333333333333
            elif (not np.isnan(eps_q2)):
                eps_q4_filled = eps_q2 * 2.0
            elif (not np.isnan(eps_q1)):
                eps_q4_filled = eps_q1 * 4.0
        if gs.is_debug:
            print('eps_q1_filled =', eps_q1_filled, 'eps_q2_filled =', eps_q2_filled,
                  'eps_q3_filled =', eps_q3_filled, 'eps_q4_filled =', eps_q4_filled)

        hpe.loc[index_q1, 'eps_filled'] = eps_q1_filled
        hpe.loc[index_q2, 'eps_filled'] = eps_q2_filled
        hpe.loc[index_q3, 'eps_filled'] = eps_q3_filled
        hpe.loc[index_q4, 'eps_filled'] = eps_q4_filled

    # Calculate Rolling EPS
    rolling_ratio = [4.0, 2.0, 1.333333333333333, 1.0]
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            index = u.quarterDateStr(year, quarter)
            eps_filled = hpe.loc[index, 'eps_filled']
            hpe.loc[index, 'eps_rolling'] = eps_filled * rolling_ratio[quarter-1]

    # Calculate Historical P/E Ratio
    price = {'pe_close':'close','pe_high':'high','pe_low':'low'}
    for i in range(hpe_index_number):
        index = hpe.index[i] # 'YYYY-mm-dd'
        eps_rolling = hpe.iloc[i]['eps_rolling']
        for column in ['pe_close','pe_high','pe_low']:
            hpe.loc[index, column] = hpe.loc[index, price[column]] / eps_rolling

    # Format columns
    for column in hpe_columns:
        hpe[column] = hpe[column].map(lambda x: '%.2f' % x)
        hpe[column] = hpe[column].astype(float)

    return hpe


def calc_hpe(stock_id, period, ratio):
    '''
    函数功能：
    --------
    逐周期计算历史市盈率。
    假定：逐周期前复权数据，Finance Summary数据已经下载或计算完成，并存储成为CSV文件。

    输入参数：
    --------
    stock_id : string, 股票代码 e.g. 600036
    period : string, 采样周期 e.g. 'W', 'M', 'Q'

    输出参数：
    --------
    DataFrame
        date 周期截止日期（为周期最后一天） e.g. 2005-03-31
        high 周期最高价
        close 周期收盘价
        low 周期最低价
        eps 周期末每股收益（可能有数据缺失）
        eps_filled 根据邻近周期推算出的周期末每股收益
        eps_rolling 根据周期末每股收益（含推算），折算的年度预期每股收益
        pe_high 根据周期最高价，计算出的市盈率
        pe_close 根据周期收盘价，计算出的市盈率
        pe_low 根据周期最低价，计算出的市盈率

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

    # Check Ratio
    ratio_types = ['PE','EP']
    if not ratio in ratio_types:
        print('Un-supported ratio type - should be one of:', ratio_types)
        raise SystemExit

    # Ensure Stock QFQ Data File is Available
    qfq_path = c.path_dict['qfq'] % period
    qfq_file = c.file_dict['qfq'] % (period, stock_id)
    qfq_fullpath = qfq_path + qfq_file
    if not u.hasFile(qfq_fullpath):
        print('Require stock QFQ file:', (qfq_fullpath))
        raise SystemExit

    # Ensure Stock Finance Summary Data File is Available
    fs_fullpath = c.fullpath_dict['finsum'] % stock_id
    if not u.hasFile(fs_fullpath):
        print('Require stock finance summary file:', (fs_fullpath))
        raise SystemExit

    #
    # Load QFQ Data
    #

    qfq = u.read_csv(qfq_fullpath)
    qfq.set_index('date', inplace=True)
    qfq.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(qfq.head(10))

    # Check empty QFQ data
    qfq_number = len(qfq)
    if qfq_number == 0:
        print('Stock QFQ data length is 0!')
        raise SystemExit

    # Handle stop-trading period (by filling with previous period data)
    # Assume: qfq data has been sorted ascendingly by date.
    for i in range(qfq_number):
        if i > 0 and np.isnan(qfq.iloc[i]['close']):
            if gs.is_debug:
                print('close = ', qfq.iloc[i]['close'])
            if np.isnan(qfq.iloc[i-1]['close']): # Ignore leading stop-trading periods
                continue
            else: # Regular internal stop-trading periods
                for column in qfq.columns:
                    qfq.iloc[i][column] = qfq.iloc[i-1][column]

    #
    # Load Finance Summary Data
    #

    fs = u.read_csv(fs_fullpath)
    fs.set_index('date', inplace=True)
    fs.sort_index(ascending = True, inplace=True)
    if gs.is_debug:
        print(fs.head(10))

    # Check empty Finance Summary data
    fs_number = len(fs)
    if fs_number == 0:
        print('Stock finance summary data length is 0!')
        raise SystemExit

    #
    # Generate Rolling EPS for Each Quarter
    #

    eps_index = []
    date_start = u.dateFromStr(qfq.index[0]) # First element
    date_end = u.dateFromStr(qfq.index[-1])  # Last element
    year_start = date_start.year
    year_end = date_end.year
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            date = u.quarterDateStr(year, quarter)
            eps_index.append(date)
    if gs.is_debug:
        print(eps_index)

    eps_columns = ['eps','eps_filled','eps_rolling']
    eps_columns_number = len(eps_columns)
    eps_index_number = len(eps_index)

    # Init all elements to NaN
    data_init = np.random.randn(eps_index_number * eps_columns_number)
    for i in range(eps_index_number * eps_columns_number):
        data_init[i] = np.nan
    eps = pd.DataFrame(data_init.reshape(eps_index_number, eps_columns_number),
                       index = eps_index, columns = eps_columns)

    # Inherite EPS from finance summary
    for i in range(eps_index_number):
        index = eps.index[i]
        if index in fs.index: # Has EPS data
            eps.iloc[i]['eps'] = fs.loc[index, 'eps']
        else: # Missing EPS data
            eps.iloc[i]['eps'] = np.nan

    # Fill the Missing EPS Data
    for year in range(year_start, year_end+1):
        index_q1 = u.quarterDateStr(year, 1)
        index_q2 = u.quarterDateStr(year, 2)
        index_q3 = u.quarterDateStr(year, 3)
        index_q4 = u.quarterDateStr(year, 4)
        eps_q1 = eps.loc[index_q1, 'eps']
        eps_q2 = eps.loc[index_q2, 'eps']
        eps_q3 = eps.loc[index_q3, 'eps']
        eps_q4 = eps.loc[index_q4, 'eps']
        if gs.is_debug:
            print('eps_q1 =', eps_q1, 'eps_q2 =', eps_q2, 'eps_q3 =', eps_q3, 'eps_q4 =', eps_q4)

        eps_q1_filled = eps_q1
        eps_q2_filled = eps_q2
        eps_q3_filled = eps_q3
        eps_q4_filled = eps_q4

        if (np.isnan(eps_q1)):
            if   (not np.isnan(eps_q2)):
                eps_q1_filled = eps_q2 * 0.5
            elif (not np.isnan(eps_q3)):
                eps_q1_filled = eps_q3 * 0.3333333333333333
            elif (not np.isnan(eps_q4)):
                eps_q1_filled = eps_q4 * 0.25
        if (np.isnan(eps_q2)):
            if   (not np.isnan(eps_q1)):
                eps_q2_filled = eps_q1 * 2.0
            elif (not np.isnan(eps_q3)):
                eps_q2_filled = eps_q3 * 0.6666666666666667
            elif (not np.isnan(eps_q4)):
                eps_q2_filled = eps_q4 * 0.5
        if (np.isnan(eps_q3)):
            if (not np.isnan(eps_q2)):
                eps_q3_filled = eps_q2 * 1.5
            elif (not np.isnan(eps_q1)):
                eps_q3_filled = eps_q1 * 3.0
            elif (not np.isnan(eps_q4)):
                eps_q3_filled = eps_q4 * 0.75
        if (np.isnan(eps_q4)):
            if (not np.isnan(eps_q3)):
                eps_q4_filled = eps_q3 * 1.333333333333333
            elif (not np.isnan(eps_q2)):
                eps_q4_filled = eps_q2 * 2.0
            elif (not np.isnan(eps_q1)):
                eps_q4_filled = eps_q1 * 4.0
        if gs.is_debug:
            print('eps_q1_filled =', eps_q1_filled, 'eps_q2_filled =', eps_q2_filled,
                  'eps_q3_filled =', eps_q3_filled, 'eps_q4_filled =', eps_q4_filled)

        eps.loc[index_q1, 'eps_filled'] = eps_q1_filled
        eps.loc[index_q2, 'eps_filled'] = eps_q2_filled
        eps.loc[index_q3, 'eps_filled'] = eps_q3_filled
        eps.loc[index_q4, 'eps_filled'] = eps_q4_filled

    # Calculate Rolling EPS
    rolling_ratio = [4.0, 2.0, 1.333333333333333, 1.0]
    for year in range(year_start, year_end+1):
        for quarter in range(1, 5):
            index = u.quarterDateStr(year, quarter)
            eps_filled = eps.loc[index, 'eps_filled']
            eps.loc[index, 'eps_rolling'] = eps_filled * rolling_ratio[quarter-1]

    if gs.is_debug:
        print(eps.head(10))

    #
    # Calculate HPE based on given period
    #

    # Drop un-used columns
    hpe = qfq.drop(['open', 'volume', 'amount'], axis=1)

    # Add columns to hpe
    if ratio == 'PE':
        for column in ['eps','eps_filled','eps_rolling','pe_high','pe_close','pe_low']:
            hpe[column] = np.nan
    else:
        for column in ['eps','eps_filled','eps_rolling','ep_high','ep_close','ep_low']:
            hpe[column] = np.nan

    # Calculate Historical P/E or E/P Ratio
    hpe_number = len(hpe)
    for i in range(hpe_number):
        index = hpe.index[i] # 'YYYY-mm-dd'
        index_date = u.dateFromStr(index) # datetime.date(YYYY-mm-dd)
        index_quarter = u.quarterDateStr(index_date.year, u.quarterOfDate(index_date)) # 'YYYY-mm-dd'
        for column in ['eps', 'eps_filled', 'eps_rolling']:
            hpe.loc[index, column] = eps.loc[index_quarter, column]

    if ratio == 'PE':
        # Calculate Historical P/E Ratio
        price = {'pe_close':'close','pe_high':'high','pe_low':'low'}
        for i in range(hpe_number):
            index = hpe.index[i] # 'YYYY-mm-dd'
            eps_rolling = hpe.iloc[i]['eps_rolling']
            for column in ['pe_close','pe_high','pe_low']:
                hpe.loc[index, column] = hpe.loc[index, price[column]] / eps_rolling
    else:
        # Calculate Historical E/P Ratio
        price = {'ep_close':'close','ep_high':'high','ep_low':'low'}
        for i in range(hpe_number):
            index = hpe.index[i] # 'YYYY-mm-dd'
            eps_rolling = hpe.iloc[i]['eps_rolling']
            for column in ['ep_close','ep_high','ep_low']:
                hpe.loc[index, column] = eps_rolling / hpe.loc[index, price[column]]

    # Format columns
    for column in hpe.columns:
        hpe[column] = hpe[column].map(lambda x: '%.2f' % x)
        hpe[column] = hpe[column].astype(float)

    return hpe
