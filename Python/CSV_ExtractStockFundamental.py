# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:43:31 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd
import numpy as np

#
# Extract Stock Fundamental Parameters
#
stock_id = '600036'
is_index = False
year_begin = 2005
year_end = 2016
is_debug = False
path_datacenter = '../DataCenter/'

#
# Load Stock Basics, Extract Stock Time-to-Market
#
basics = pd.read_csv(path_datacenter+'StockBasics'+'.csv',encoding='utf-8')
basics.set_index('code', inplace=True)
print(basics.head(10))

timeToMarket = basics.loc[int(stock_id), 'timeToMarket'] #上市日期YYYYMMDD
print(timeToMarket)

date = pd.to_datetime(timeToMarket, format='%Y%m%d')
print(date.year, date.month, date.day)

#
# Load Report Data and Extract Reports for the Given Stock
#
if year_begin < date.year:
    year_begin = date.year

report_columns = ['eps','eps_yoy','bvps','roe','epcf','net_profits',
                  'profits_yoy','distrib','report_date']
report_columns_number = len(report_columns)
report_index = []
for year in range(year_begin, year_end+1):
    for quarter in range(1, 5):
        report_index.append(str(year)+'Q'+str(quarter))
print(report_index)
report_index_number = len(report_index)

# Init all elements to NaN
data_init = np.random.randn(report_index_number * report_columns_number)
for i in range(report_index_number * report_columns_number):
    data_init[i] = np.nan
df = pd.DataFrame(data_init.reshape(report_index_number, report_columns_number), 
                  index = report_index, columns = report_columns)

for year in range(year_begin, year_end+1):
    for quarter in range(1, 5):
        index = str(year)+'Q'+str(quarter)
        postfix = '_'+str(year)+'Q'+str(quarter)
        report = pd.read_csv(path_datacenter+'ReportData'+postfix+'.csv',encoding='utf-8')
        if is_debug:
            print(report.head(10))
        r = report[report.code == int(stock_id)] # type(r) is a data frame
        if is_debug:
            print(r)
        if not r.empty:
            df.loc[index] = r.irow(0)
            if is_debug:
                print(r.irow(0)['eps'])

#
# Fill the Missing Data
#
df['eps_filled'] = pd.Series(np.random.randn(report_index_number), index=df.index)
for year in range(year_begin, year_end+1):
    index_q1 = str(year)+'Q'+str(1)
    index_q2 = str(year)+'Q'+str(2)
    index_q3 = str(year)+'Q'+str(3)
    index_q4 = str(year)+'Q'+str(4)
    eps_q1 = df.loc[index_q1, 'eps']
    eps_q2 = df.loc[index_q2, 'eps']
    eps_q3 = df.loc[index_q3, 'eps']
    eps_q4 = df.loc[index_q4, 'eps']
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
    print('eps_q1_filled =', eps_q1_filled, 'eps_q2_filled =', eps_q2_filled, 
          'eps_q3_filled =', eps_q3_filled, 'eps_q4_filled =', eps_q4_filled)
    
    df.loc[index_q1, 'eps_filled'] = eps_q1_filled
    df.loc[index_q2, 'eps_filled'] = eps_q2_filled
    df.loc[index_q3, 'eps_filled'] = eps_q3_filled
    df.loc[index_q4, 'eps_filled'] = eps_q4_filled

#
# Calculate Rolling EPS
#
df['eps_rolling'] = pd.Series(np.random.randn(report_index_number), index=df.index)
for year in range(year_begin, year_end+1):
    index_q1 = str(year)+'Q'+str(1)
    index_q2 = str(year)+'Q'+str(2)
    index_q3 = str(year)+'Q'+str(3)
    index_q4 = str(year)+'Q'+str(4)
    eps_q1 = df.loc[index_q1, 'eps_filled']
    eps_q2 = df.loc[index_q2, 'eps_filled']
    eps_q3 = df.loc[index_q3, 'eps_filled']
    eps_q4 = df.loc[index_q4, 'eps_filled']
    df.loc[index_q1, 'eps_rolling'] = eps_q1 * 4.0
    df.loc[index_q2, 'eps_rolling'] = eps_q2 * 2.0
    df.loc[index_q3, 'eps_rolling'] = eps_q3 * 1.333333333333333
    df.loc[index_q4, 'eps_rolling'] = eps_q4 * 1.0

#
# Output Extracted Reports for the Given Stock
# 
print(df)
df.to_csv(path_datacenter+'ReportData_'+stock_id+'.csv',encoding='utf-8')



























