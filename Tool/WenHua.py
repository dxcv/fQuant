# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:01:48 2017

@author: freefrom
"""

import os, fnmatch, sys, chardet
import pandas as pd
import GlobalSettings as gs
import Utilities as u

def filterFiles(dirname, patterns='*', single_level=False, yield_folders=False):
    patterns = patterns.split(';')
    allfiles = []
    for rootdir, subdirs, files in os.walk(dirname):
        print(subdirs)
        allfiles.extend(files)
        if yield_folders:
            allfiles.extend(subdirs)
        if single_level:
            break
    allfiles.sort()
    for eachpattern in patterns:
        for eachfile in fnmatch.filter(allfiles, eachpattern):
            print(os.path.normpath(eachfile))

    return allfiles

def detectCodec(fullpath):
    f = open(fullpath, 'rb')
    data = f.read()
    print (chardet.detect(data))

def handleResults(root, paras):
    # Get List of Results Files
    files = filterFiles(root, patterns='*.xls', single_level=True)
    df_all = pd.DataFrame()
    for file in files:
        # Load Each Results File
        fullpath = root + file
        df = pd.read_excel(fullpath,encoding='ascii')
        df.columns = ['编号','时间','交易所','合约','信号','信号行','买卖','平开','价格','手数(平,开)','成交额','手续费','投保','平仓盈亏','可用资金','权益','滑点损耗','信号消失成本']
        df_number = len(df)
        if df_number == 0:
            continue;
        df = df.drop(df_number-1)
        df_number = df_number-1
        # Accumulate indices for string columns
        column_indexes = []
        df_columns_number = len(df.columns)
        for i in range(df_columns_number):
            if isinstance(df.iloc[0,i], str):
                column_indexes.append(i)
        for i in range(df_number):
            for c in column_indexes: # Remove last character for string entries.
                df.iloc[i,c] = df.iloc[i,c][:-1]
            df.iloc[i,1] = u.formatDateYYYYmmddStr(df.iloc[i,1][:8]) # '时间'取前八位YYYYmmdd
        df.set_index('编号',inplace=True)
        if gs.is_debug:
            print(df.head(10))
        # Process Results Data Frame
        df = handleResultsSingle(df, paras)
        if gs.is_debug:
            print(df.head(10))
        # Merge Data Frame
        if file == files[0]:
            df_all = df
        else:
            df_all = pd.concat([df_all,df])
        if gs.is_debug:
            print(df_all.tail(10))
        # Save to CSV File
        if not u.isNoneOrEmpty(df):
            u.to_csv(df,root,file[:-4]+'.csv')

    # Save Merged Results to CSV File
    u.to_csv(df_all, root, 'all.csv')

    # Process Merged Results
    df_all.sort_values('时间',ascending=True,inplace=True)
    df_all = df_all.reset_index(drop=True)
    df_all_number = len(df_all)
    date = df_all.ix[0,'时间']
    profit = df_all.ix[0,'模拟盈亏']
    df_merged = pd.DataFrame(columns=['date','profit'])
    for i in range(1, df_all_number):
        if df_all.ix[i,'时间'] == date:
            profit = profit + df_all.ix[i,'模拟盈亏']
            if i == df_all_number-1: # Last one
                df_merged = df_merged.append({'date':date,'profit':profit},ignore_index=True)
        else:
            df_merged = df_merged.append({'date':date,'profit':profit},ignore_index=True)
            date = df_all.ix[i,'时间']
            profit = df_all.ix[i,'模拟盈亏']
    # Calculate '累计盈亏'
    df_merged['accu_profit'] = 0.0
    df_merged.ix[0,'accu_profit'] = df_merged.ix[0,'profit']
    df_merged_number = len(df_merged)
    for i in range(1,df_merged_number):
        df_merged.ix[i,'accu_profit'] = df_merged.ix[i-1,'accu_profit'] + df_merged.ix[i,'profit']
    # Calculate '净值'
    df_merged['net_value'] = 0.0
    base = paras[2]
    for i in range(df_merged_number):
        df_merged.ix[i,'net_value'] = 1.0+df_merged.ix[i,'accu_profit']/base

    # Saved Final Results to CSV File
    u.to_csv(df_merged, root, 'final.csv')

def handleResultsSingle(df, paras):
    # Remove '平仓盈亏'为无效项的数据行
    df_number = len(df)
    df = df[df.平仓盈亏 != '---']
    df = df.reset_index(drop=True)
    # Remove '信号'为CLOSEOUT的数据行
    df_number = len(df)
    df = df[df.信号 != 'CLOSEOUT']
    df = df.reset_index(drop=True)
    # Calculate '模拟盈亏'
    df['模拟盈亏'] = 0.0
    df_number = len(df)
    loss = paras[0]
    profit = paras[1]
    for i in range(df_number):
        df.ix[i,'模拟盈亏'] = loss if df.ix[i,'平仓盈亏'][:1] == '-' else profit
    # Calculate '累计盈亏'
    df['累计盈亏'] = 0.0
    df.ix[0,'累计盈亏'] = df.ix[0,'模拟盈亏']
    for i in range(1,df_number):
        df.ix[i,'累计盈亏'] = df.ix[i-1,'累计盈亏'] + df.ix[i,'模拟盈亏']
    # Calculate '净值'
    df['净值'] = 0.0
    base = paras[2]
    for i in range(df_number):
        df.ix[i,'净值'] = 1.0+df.ix[i,'累计盈亏']/base

    return df

###############################################################################
root = 'D:\\Documents\\策略\\测试\\'
paras = [-10000,10000,10000000] # loss, profit, base

print(sys.getdefaultencoding())
handleResults(root, paras)