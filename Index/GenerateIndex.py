# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:25:17 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
import Common.GlobalSettings as gs
from Data.GetTrading import getDailyHFQ, loadDailyQFQ
from Index.Index import load_component, generate_index, load_index_result

def generateIndex(index_name, base_date, base_point, weight_method, benchmark_id):
    # Load Index Component Stocks
    component = load_component(index_name)
    if u.isNoneOrEmpty(component):
        print('Index Component Not Available:', index_name)
        raise SystemExit
    if gs.is_debug:
        print(component.head(10))

    # Update Benchmark Index LSHQ to Latest
    date_start = u.dateFromStr(base_date)
    date_end = u.today()
    getDailyHFQ(stock_id=benchmark_id, is_index=True, date_start=date_start,
                date_end=date_end, time_to_market=None, incremental=True)
    print('Update Price:', benchmark_id)

    # Update Component Stock LSHQ to Latest
    component_number = len(component)
    for i in range(component_number):
        stock_id = u.stockID(component.ix[i,'code'])
        getDailyHFQ(stock_id=stock_id, is_index=False, date_start=date_start,
                    date_end=date_end, time_to_market=None, incremental=True)
        print('Update Price:', stock_id)

    # Generate Index
    generate_index(index_name, base_date, base_point, weight_method, benchmark_id)

def generateIndexSeries(index_names, series_name):
    # Generate Index Series DataFrame
    columns = ['date', 'index_benchmark', 'ratio_benchmark']
    str_columns = ['date']
    float_columns = ['index_benchmark', 'ratio_benchmark']
    index_number = len(index_names)
    for i in range(index_number):
        index_name = index_names[i]
        columns.append('index_'+index_name)
        float_columns.append('index_'+index_name)
        columns.append('ratio_'+index_name)
        float_columns.append('ratio_'+index_name)
    index = load_index_result(index_names[0])
    row_number = len(index)
    series = u.createDataFrame(row_number, columns)
    print(series)

    # Init Series with Common Columns
    for i in range(row_number):
        series.ix[i, 'date'] = index.ix[i, 'date']
        series.ix[i, 'index_benchmark'] = index.ix[i, 'b_index']
        series.ix[i, 'ratio_benchmark'] = 1.0 + index.ix[i, 'b_ratio']

    # Merge Separate Index Data into Index Series
    for index_name in index_names:
        index = load_index_result(index_name)
        for i in range(row_number):
            series.ix[i, 'index_'+index_name] = index.ix[i, 'index']
            series.ix[i, 'ratio_'+index_name] = 1.0 + index.ix[i, 'ratio']

    # Format Columns
    for column in str_columns:
        series[column] = series[column].astype(str)
    for column in float_columns:
        series[column] = series[column].map(lambda x: '%.2f' % x)
        series[column] = series[column].astype(float)
    series.set_index('date', inplace=True)

    # Save to CSV File
    if not u.isNoneOrEmpty(series):
        u.to_csv(series, c.path_dict['index'], c.file_dict['index_r'] % series_name)

def generateComponentStatistics(index_name, latest_date):
    component = load_component(index_name)
    component_number = len(component)
    suspended_number = 0
    # TODO: Improve Performance to Determine Suspended Stocks
#    for i in range(component_number):
#        stock_id = u.stockID(component.ix[i,'code'])
#        stock = loadDailyQFQ(stock_id, False)
#        if u.isNoneOrEmpty(stock):
#            suspended_number = suspended_number + 1
#        else:
#            stock_number = len(stock)
#            if stock.ix[stock_number-1,'date'] < latest_date:
#                suspended_number = suspended_number + 1

    return [component_number, suspended_number]

def generateIndexStatistics(index_names, series_name):
    # Create Statistics DataFrame
    columns = ['name', 'date', 'c_number', 's_number', 'index', 'ratio', 'b_index', 'b_ratio', 'delta_ratio']
    index_number = len(index_names)
    stat = u.createDataFrame(index_number, columns)

    # Calculate Index Statistics
    for i in range(index_number):
        index_name = index_names[i]
        result = load_index_result(index_name)
        if u.isNoneOrEmpty(result):
            continue
        result_number = len(result)
        latest_date = result.ix[result_number-1,'date']
        component_number, suspended_number = generateComponentStatistics(index_name, latest_date)
        stat.ix[i,'name'] = index_name
        stat.ix[i,'date'] = latest_date
        stat.ix[i,'c_number'] = component_number
        stat.ix[i,'s_number'] = suspended_number
        stat.ix[i,'index'] = result.ix[result_number-1,'index']
        ratio = result.ix[result_number-1,'ratio']
        stat.ix[i,'ratio'] = ratio
        stat.ix[i,'b_index'] = result.ix[result_number-1,'b_index']
        b_ratio = result.ix[result_number-1,'b_ratio']
        stat.ix[i,'b_ratio'] = b_ratio
        stat.ix[i,'delta_ratio'] = ratio - b_ratio

    # Format Statistics DataFrame
    for column in ['name', 'date']:
        stat[column] = stat[column].astype(str)
    for column in ['c_number', 's_number']:
        stat[column] = stat[column].astype(int)
    for column in ['index', 'b_index']:
        stat[column] = stat[column].map(lambda x: '%.2f' % x)
        stat[column] = stat[column].astype(float)
    for column in ['ratio', 'b_ratio', 'delta_ratio']:
        stat[column] = stat[column].map(lambda x: '%.2f%%' % (x*100.0))
    stat.set_index('name', inplace=True)

    # Save to CSV File
    if not u.isNoneOrEmpty(stat):
        print(stat)
        u.to_csv(stat, c.path_dict['index'], c.file_dict['index_s'] % series_name)

def generateIndexFeiYan(index_names):
    # Generate Index
    for index_name in index_names:
        generateIndex(index_name, '2016-12-30', 1000, 'EqualWeight', '000300')

    # Generate Index Series
    generateIndexSeries(index_names, 'FeiYan_Series')

    # Generate Index Statistics
    generateIndexStatistics(index_names, 'FeiYan_Series')

###############################################################################
