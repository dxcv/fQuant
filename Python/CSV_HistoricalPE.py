# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:28:29 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd
import numpy as np
import DateUtility as du
import ConstantData as cd

def get_historical_pe(stock_id, year_start, year_end):
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
    stock_data = pd.read_csv(cd.path_datacenter + (cd.file_quarterlyqfq % stock_id), encoding='utf-8')
    stock_data_number = len(stock_data)
    if stock_data_number != (year_end - year_start + 1)*4:
        print('The duration of tock data does not match the duration of analysis!')
        raise SystemExit

    stock_data.set_index('date', inplace=True)
    stock_data.sort_index(ascending = True, inplace=True)
    if cd.is_debug:
        print(stock_data.head(10))

    # Handle stop-trading quarter (by filling with previous quarter data)
    # Assume: stock data has been sorted ascendingly by date.
    for i in range(stock_data_number):
        if i > 0 and np.isnan(stock_data.iloc[i]['close']):
            if cd.is_debug:
                print('close = ', stock_data.iloc[i]['close'])
            if np.isnan(stock_data.iloc[i-1]['close']): # Ignore leading stop-trading quarters
                continue
            else: # Regular internal stop-trading quarters
                for column in stock_data.columns:
                    stock_data.iloc[i][column] = stock_data.iloc[i-1][column]

    # Fetch Report Data
    report_data = pd.read_csv(cd.path_datacenter + (cd.file_financesummary % stock_id), encoding='utf-8')
    report_data.set_index('date', inplace=True)
    report_data.sort_index(ascending = True, inplace=True)
    if cd.is_debug:
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
        index_q1 = du.quarterDate(year, 1)
        index_q2 = du.quarterDate(year, 2)
        index_q3 = du.quarterDate(year, 3)
        index_q4 = du.quarterDate(year, 4)
        eps_q1 = hpe.loc[index_q1, 'eps']
        eps_q2 = hpe.loc[index_q2, 'eps']
        eps_q3 = hpe.loc[index_q3, 'eps']
        eps_q4 = hpe.loc[index_q4, 'eps']
        if cd.is_debug:
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
        if cd.is_debug:
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
            index = du.quarterDate(year, quarter)
            eps_filled = hpe.loc[index, 'eps_filled']
            hpe.loc[index, 'eps_rolling'] = eps_filled * rolling_ratio[quarter-1]

    # Calculate Historical P/E Ratio
    price = {'pe_close':'close','pe_high':'high','pe_low':'low'}
    for i in range(hpe_index_number):
        eps_rolling = hpe.iloc[i]['eps_rolling']
        for column in ['pe_close','pe_high','pe_low']:
            hpe.iloc[i][column] = hpe.iloc[i][price[column]] / eps_rolling

    # Format columns
    for column in hpe_columns:
        hpe[column] = hpe[column].map(lambda x: '%.2f' % x)
        hpe[column] = hpe[column].astype(float)

    return hpe

#
# Historical PE Parameters
#
stock_ids  = ['000002'] #['300059','600036','000002','002024']
year_start = 2005
year_end   = 2016

#
# Iteratively Calculate Historical PE
#
stock_number = len(stock_ids)
for i in range(stock_number):
    stock_id = stock_ids[i]
    hpe = get_historical_pe(stock_id = stock_id, year_start = year_start, year_end = year_end)

    # Output Results
    if cd.is_debug:
        print(hpe.head(10))
    hpe.to_excel(cd.path_datacenter + (cd.file_historicalpe % stock_id))
























