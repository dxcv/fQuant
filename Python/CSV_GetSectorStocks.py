# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 21:11:38 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import ConstantData as cd
import pandas as pd
import datetime as dt

def get_sector_stocks(stock_basics, sector_name, cutoff_date):
    '''
    函数功能：
    --------
    获取给定产业，指定日之前上市的所有股票列表。
    
    输入参数：
    --------
    stock_basics : dataframe, 股票基本信息DF
    sector_name : string, 行业名称 e.g. 银行
    cutoff_date : datetime.date, 截至上市日期 e.g. datetime.date(2005, 1, 1)
    
    输出参数：
    --------
    DataFrame
        code 股票代码 e.g. 2005-03-31
        name 股票名称 e.g. 招商银行
        timeToMarket 上市日期 e.g. 2005-01-01
    
    '''
    # Get stocks for the given sector
    sector_stocks = stock_basics[['code','name','timeToMarket']][stock_basics['industry'] == sector_name]
    for column in ['code','name','timeToMarket']:
        sector_stocks[column] = sector_stocks[column].astype(str)
    sector_stocks['code'] = sector_stocks['code'].map(lambda x:str(x).zfill(6))
    if cd.is_debug:
        print(sector_stocks.head(10))

    date = dt.date.strftime(cutoff_date, '%Y%m%d')
    sector_stocks = sector_stocks[sector_stocks['timeToMarket'] < date]
    sector_stocks.set_index('code', inplace=True)
    sector_stocks.sort_values(['timeToMarket'], ascending = True, inplace = True)
    if cd.is_debug:
        print(sector_stocks.head(10))

    return sector_stocks

#
# Get Sector Stocks Parameters
#
sector = '银行'
date = dt.date(2016, 1, 1)

#
# Load Stock Basics, Extract Stocks for Given Sector
#
basics = pd.read_csv(cd.path_datacenter + cd.file_stockbasics, encoding='utf-8')
if cd.is_debug:
    print(basics.head(10))

stocks = get_sector_stocks(stock_basics = basics, sector_name = sector, cutoff_date = date)
stocks.to_csv(cd.path_datacenter + cd.file_sectorstocks % sector, encoding='utf-8')























