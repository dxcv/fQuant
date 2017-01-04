# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 10:26:41 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import numpy as np
import pandas as pd
import datetime as dt

#
# Monthly Return Statistics Parameters
#
stock_id   = '000300'
is_index   = True
start_date = '2005-04-08'
end_date   = '2016-12-30'
is_debug   = True
path_datacenter = '../DataCenter/'

#
# Fetch Stock Data
#
stock_data = pd.read_csv(path_datacenter+stock_id+'.csv')
number_sd = len(stock_data)
if number_sd == 0:
    raise SystemExit
    
stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y-%m-%d')
#stock_data.sort('date', inplace=True)
stock_data.set_index('date', inplace=True)
stock_data = stock_data.sort_index(0)
if is_debug:
    print(stock_data.head(10))
    print(stock_data.tail(10))

#
# Convert Daily Data to Monthly Data
#

# Weekly='W', Monthly='M', Quarterly='Q', 5 Minutes='5min', 12 Days='12D'
period_type = 'M'
period_stock_data = stock_data.resample(period_type).first()
if is_debug:
    print(period_stock_data.head(10))
    print(period_stock_data.tail(10))

#period_stock_data['date']   = stock_data['date'].resample(period_type).first()
period_stock_data['open']   = stock_data['open'].resample(period_type).first()
period_stock_data['high']   = stock_data['high'].resample(period_type).max()
period_stock_data['close']  = stock_data['close'].resample(period_type).last()
period_stock_data['low']    = stock_data['low'].resample(period_type).min()
period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()
period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()
if is_debug:
    print(period_stock_data.head(10))
    print(period_stock_data.tail(10))

#
# Calculate Monthly Return Statistics
#
s_date = dt.datetime.strptime(start_date,'%Y-%m-%d')
e_date = dt.datetime.strptime(end_date,'%Y-%m-%d')
if is_debug:
    print(s_date.year, s_date.month, s_date.day)
    print(e_date.year, e_date.month, e_date.day)

period_return = [[0 for col in range(12)] for row in range(e_date.year - s_date.year + 1)]
if is_debug:
    print(period_return)

number_stock_data = len(period_stock_data)
number_per_month = [0 for row in range(12)]

for index in range(0, number_stock_data):
    current_year = period_stock_data.index[index].year
    current_month = period_stock_data.index[index].month
    if is_debug:
        print(current_year, current_month)
    
    current_open = period_stock_data['open'][index]
    current_close = period_stock_data['close'][index]
    ratio = 0
    if (index < 1):
        ratio = current_close / current_open - 1
    else:
        ratio = current_close / period_stock_data['close'][index-1] - 1
    period_return[current_year-s_date.year][current_month-1] = ratio
    number_per_month[current_month-1] += 1
if is_debug:
    print(period_return)

avg_month_return = [0 for row in range(12)]
for year in range(e_date.year - s_date.year + 1):
    for month in range(12):
        avg_month_return[month] += period_return[year][month]
for month in range(12):
    avg_month_return[month] /= number_per_month[month]

if is_debug:
    print(avg_month_return)

#
# Output Statistics
#
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = []
num_years = e_date.year - s_date.year + 1
for year in range(num_years):
    years.append(s_date.year + year)
    
df = pd.DataFrame(np.random.randn(12, num_years), index = months, columns = years)
    
for year in range(num_years):
    for month in range(12):
        df.loc[months[month], years[year]] = period_return[year][month]

if is_debug:
    print(df)

df.to_excel(path_datacenter+stock_id+'_MonthlyReturn'+'.xlsx')











