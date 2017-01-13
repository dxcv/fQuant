# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:28:23 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import numpy as np
import pandas as pd

#
# Merge By Date Parameters
#
stock_id   = '000300'
start_date = '2005-04-08'
end_date   = '2016-12-30'
is_debug   = True
path_datacenter = '../DataCenter/'
periods = [1, 3, 5, 10, 20, 60, 120, 240]

#
# Fetch Stock Data
#
stock_data = pd.read_csv(path_datacenter+stock_id+'.csv')
stock_data_number = len(stock_data)
if stock_data_number == 0:
    raise SystemExit

stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y-%m-%d')
stock_data.set_index('date', inplace=True)
stock_data = stock_data.sort_index(0)
if is_debug:
    print(stock_data.head(10))
    print(stock_data.tail(10))

#
# Calculate Rate of Change
#
period_number = len(periods)
# Check the sanity of periods
if period_number < 1:
    print('At least needs one period!')
    raise SystemExit
for i in range(period_number):
    if periods[i] < 0:
        print('Period needs to be positive number!')
        raise SystemExit

# Create a new data frame
df_columns = ['close']
for i in range(period_number):
    df_columns.append(str(periods[i]))
    
df = pd.DataFrame(np.random.randn(stock_data_number, period_number + 1), 
                  index = stock_data.index, columns = df_columns)
for i in range(stock_data_number):
    df['close'][i] = stock_data['close'][i]

reference = 0.0
for period in periods:
    column = str(period)
    for i in range(stock_data_number):
        if (i < period):
            reference = df['close'][0]
        else:
            reference = df['close'][i - period]
        df[column][i] = (df['close'][i] / reference) - 1.0

#
# Output ROC Statistics
#
if is_debug:
    print(df.head(10))

df.to_excel(path_datacenter+stock_id+'_RateOfChange'+'.xlsx')

#
# Calculate Statistics for ROC
#
stat_columns = ['count', 'mean', 'median', 'std', 'min', '10%', '20%', '30%', 
                '40%', '50%', '60%', '70%', '80%', '90%', 'max']
stat_column_number = len(stat_columns)
quantile_percentile = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

stat = pd.DataFrame(np.random.randn(period_number, stat_column_number),
                    index = periods, columns = stat_columns)
for period in periods:
    column = str(period)
    q = df[column].quantile(quantile_percentile)
    
    stat.loc[period,'count'] = len(df[column])
    stat.loc[period,'mean'] = df[column].mean()
    stat.loc[period,'median'] = df[column].median()
    stat.loc[period,'std'] = df[column].std()
    stat.loc[period,'min'] = df[column].min()
    stat.loc[period,'10%'] = q.loc[.1]
    stat.loc[period,'20%'] = q.loc[.2]
    stat.loc[period,'30%'] = q.loc[.3]
    stat.loc[period,'40%'] = q.loc[.4]
    stat.loc[period,'50%'] = q.loc[.5]
    stat.loc[period,'60%'] = q.loc[.6]
    stat.loc[period,'70%'] = q.loc[.7]
    stat.loc[period,'80%'] = q.loc[.8]
    stat.loc[period,'90%'] = q.loc[.9]
    stat.loc[period,'max'] = df[column].max()

#
# Output Statistics for ROC
#    
if is_debug:
    print(stat)
    
stat.to_excel(path_datacenter+stock_id+'_RateOfChange_Statistics'+'.xlsx')

#
# Calculate Histogram for ROC
#
hist_columns = ['count', 'mean', 'median', 'std', '< -3std', '-3std : -2std', 
                '-2std : -std', '-std : mean', 'mean : std', 'std : 2std',
                '2std : 3std', '> 3std']
hist_column_number = len(hist_columns)

hist = pd.DataFrame(np.random.randn(period_number, hist_column_number),
                    index = periods, columns = hist_columns)
for period in periods:
    column = str(period)
    
    hist.loc[period,'count'] = len(df[column])
    hist.loc[period,'mean'] = df[column].mean()
    hist.loc[period,'median'] = df[column].median()
    hist.loc[period,'std'] = df[column].std()
    
    mean = hist.loc[period,'mean'] # Use mean
    std = hist.loc[period,'std']
    hist_count = [0 for i in range(8)]
    for i in range(stock_data_number):
        price = df[column][i]
        if (price > mean + 3.0 * std):
            hist_count[0] += 1
        elif (price > mean + 2.0 * std):
            hist_count[1] += 1
        elif (price > mean + std):
            hist_count[2] += 1
        elif (price > mean):
            hist_count[3] += 1
        elif (price > mean - std):
            hist_count[4] += 1
        elif (price > mean - 2.0 * std):
            hist_count[5] += 1
        elif (price > mean - 3.0 * std):
            hist_count[6] += 1
        else:
            hist_count[7] += 1

    hist.loc[period,'< -3std']       = hist_count[7]
    hist.loc[period,'-3std : -2std'] = hist_count[6]
    hist.loc[period,'-2std : -std']  = hist_count[5]
    hist.loc[period,'-std : mean']   = hist_count[4]
    hist.loc[period,'mean : std']    = hist_count[3]
    hist.loc[period,'std : 2std']    = hist_count[2]
    hist.loc[period,'2std : 3std']   = hist_count[1]
    hist.loc[period,'> 3std']        = hist_count[0]

#
# Output Statistics for ROC
#    
if is_debug:
    print(hist)
    
hist.to_excel(path_datacenter+stock_id+'_RateOfChange_Histogram'+'.xlsx')

















