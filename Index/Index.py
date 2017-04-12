# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:25:17 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u
from Data.GetTrading import loadDailyQFQ

import pandas as pd
import numpy as np

def load_component(index_name):
    comp_path = c.path_dict['index']
    comp_file = c.file_dict['index_c'] % index_name
    component = u.read_csv(comp_path+comp_file)
    return component

def find_stock_close(stock, date):
    """
        返回最接近且不迟于date的收盘价，用于丢失数据（停牌）的插值。
    Parameters
    --------
    stock:dataframe         包含收盘价'close'的DataFrame
    date:string             日期 e.g. '2016-12-31'
    """
    stock_number = len(stock)
    if stock_number == 0:
        print('findStockClose: No stock data!')
        return np.nan
    if date <= stock.ix[0,'date']: # Earlier than first date
        return stock.ix[0,'close']
    if date >= stock.ix[stock_number-1,'date']: # Later than last date
        return stock.ix[stock_number-1,'close']
    for i in range(1, stock_number):
        date_prev = stock.ix[i-1,'date']
        date_curr = stock.ix[i,'date']
        if date_prev <= date and date_curr > date:
            return stock.ix[i-1,'close']

    return stock.ix[stock_number-1,'close']

def generate_index(index_name, base_date, base_point, weight_method, benchmark_id):
    """
        根据给定指数成分股，基期，基点，加权方法和基准指数，计算自定义指数并与基准指数做对比。
    Parameters
    --------
    index_name:string       指数名称 e.g. 'FeiYan_NewEnergyVehicle'
    base_date:string        基期日期 e.g. '2016-12-30'
    base_point:float        基点数值 e.g. 1000.0
    weight_method:string    加权方法 e.g. 'EqualWeight'
    benchmark_id:string     基准指数 e.g. '000300'

    Pre-requisites
    --------
    指数成分股列表     DataCenter/Index/IndexComponent_%s.csv % index_name
    基准指数历史行情   DataCenter/Trading/LSHQ/Trading_LSHQ_Index_%s.csv % benchmark_id
    成分股历史行情     DataCenter/Trading/LSHQ/Trading_LSHQ_Stock_%s.csv % stock_id

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

    如果数据文件不存在或者自定义指数计算失败，返回None。
    如果自定义指数计算成功，返回DataFrame，设置date为索引，并根据date进行升序排序。
    """
    # Load Benchmark Index
    benchmark = loadDailyQFQ(benchmark_id, True)
    if u.isNoneOrEmpty(benchmark):
        print('Benchmark LSHQ Not Available:', benchmark_id)
        raise SystemExit

    # Load Index Component Stocks
    component = load_component(index_name)
    if u.isNoneOrEmpty(component):
        print('Index Component Not Available:', index_name)
        raise SystemExit

    # Check Weight Method
    if not weight_method == 'EqualWeight':
        print('Un-supported Weight Method:', weight_method)
        raise SystemExit

    # Create Index Dataframe
    index = benchmark[benchmark.date >= base_date] # Filtered by base_date
    index = index[['date','close']]
    index.set_index('date',inplace=True)
    index.sort_index(ascending=True,inplace=True)
    index_number = len(index)

    # Add New Columns
    for column in ['ratio','index','b_ratio','b_index']:
        index[column] = np.nan

    # Extract Component Stock LSHQ
    component_number = len(component)
    for i in range(component_number):
        stock_id = u.stockID(component.ix[i,'code'])
        df = loadDailyQFQ(stock_id, False)
        # Check Availability
        if u.isNoneOrEmpty(df):
            print('Stock LSHQ Not Available:', stock_id)
            raise SystemExit
        # Slice Data
        stock = df[df.date >= base_date] # Filtered by base_date
        stock = stock[['date','close']]
        stock.set_index('date',inplace=True)
        stock.sort_index(ascending=True,inplace=True)
        # Merge Index with Stock
        index = pd.merge(index, stock, how='left', left_index=True, right_index=True, 
                         sort=True, suffixes=('','_'+stock_id))
        # Fill Missing Data
        column = 'close_' + stock_id
        if np.isnan(index.ix[0,column]): # First Data is NaN
            index.ix[0,column] = find_stock_close(df, base_date)
        for j in range(1, index_number):
            if np.isnan(index.ix[j,column]):
                index.ix[j,column] = index.ix[j-1,column]

    # Calculate Index Value
    for i in range(index_number):
        ratio = 0.0
        for j in range(component_number):
            stock_id = u.stockID(component.ix[j,'code'])
            column = 'close_' + stock_id
            ratio = ratio + (index.ix[i,column] / index.ix[0,column]) - 1.0
        ratio = ratio / float(component_number)
        index.ix[i,'ratio'] = ratio
        index.ix[i,'index'] = float(base_point) * (1.0 + ratio)
        index.ix[i,'b_ratio'] = (index.ix[i,'close'] / index.ix[0,'close']) - 1.0
        index.ix[i,'b_index'] = index.ix[i,'close']

    # Save to CSV File
    if not u.isNoneOrEmpty(index):
        u.to_csv(index, c.path_dict['index'], c.file_dict['index_r'] % index_name)