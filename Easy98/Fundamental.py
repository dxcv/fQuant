# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:23:11 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import GlobalSettings as gs
import Utilities as u

#
# Get Stock Basics
#

def get_stock_basics():
    '''
    函数功能：
    --------
    获取沪深上市公司基本情况。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数
    '''
    # Download data
    basics = ts.get_stock_basics()
    if gs.is_debug:
        print(basics.head(10))

    # Return Dataframe
    return basics



















