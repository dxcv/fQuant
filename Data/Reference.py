# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:21:46 2017

@author: freefrom
"""

import tushare as ts
import numpy as np

def get_rzrq_sh(date_start, date_end):
    """
        获取沪市融资融券汇总数据
    Parameters
    --------
    date_start          开始日期，e.g. '2010-03-31'
    date_end            截止日期，e.g. '2017-03-28'

    Return
    --------
    DataFrame
        date            日期
        rzye_sh         融资余额上海(元)
        rzmre_sh        融资买入额上海(元)
        rqyl_sh         融券余量上海
        rqylje_sh       融券余量金额上海(元)
        rqmcl_sh        融券卖出量上海
        rzrqye_sh       融资融券余额上海(元)
    """
    rzrq = ts.sh_margins(start=date_start, end=date_end)
    # Rename Columns
    columns_map = {'opDate':'date', 'rzye':'rzye_sh', 'rzmre':'rzmre_sh',
                   'rqyl':'rqyl_sh', 'rqylje':'rqylje_sh', 'rqmcl':'rqmcl_sh',
                   'rzrqjyzl':'rzrqye_sh'}
    rzrq.rename(columns=columns_map, inplace = True)
    return rzrq

def get_rzrq_sz(date_start, date_end):
    """
        获取深市融资融券汇总数据
    Parameters
    --------
    date_start          开始日期，e.g. '2010-03-31'
    date_end            截止日期，e.g. '2017-03-28'

    Return
    --------
    DataFrame
        date            日期
        rzye_sz         融资余额深圳(元)
        rzmre_sz        融资买入额深圳(元)
        rqyl_sz         融券余量深圳
        rqylje_sz       融券余量金额深圳(元)
        rqmcl_sz        融券卖出量深圳
        rzrqye_sz       融资融券余额深圳(元)
    """
    rzrq = ts.sz_margins(start=date_start, end=date_end)
    # Rename Columns
    columns_map = {'opDate':'date', 'rzmre':'rzmre_sz', 'rzye':'rzye_sz',
                   'rqmcl':'rqmcl_sz', 'rqyl':'rqyl_sz', 'rqye':'rqylje_sz',
                   'rzrqye':'rzrqye_sz'}
    rzrq.rename(columns=columns_map, inplace = True)
    print(rzrq.head(10))
    # Swith Columns
    rzye_sz = rzrq.pop('rzye_sz')
    rzrq.insert(1, 'rzye_sz', rzye_sz)
    rqmcl_sz = rzrq.pop('rqmcl_sz')
    rzrq.insert(5, 'rqmcl_sz', rqmcl_sz)
    return rzrq

def get_rzrq_sh_details(date_start, date_end):
    """
        获取沪市融资融券明细数据
    Parameters
    --------
    date_start          开始日期，e.g. '2010-03-31'
    date_end            截止日期，e.g. '2017-03-28'

    Return
    --------
    DataFrame
        date            日期
        code            股票代码
        name            股票名称
        rzye            融资余额(元)
        rzmre           融资买入额(元)
        rzche           融资偿还额(元)
        rqyl            融券余量
        rqmcl           融券卖出量
        rqchl           融券偿还量
        rqylje          融券余量金额(元)
        rzrqye          融资融券余额(元)
    """
    rzrq = ts.sh_margin_details(start=date_start, end=date_end)
    # Rename Columns
    columns_map = {'opDate':'date', 'stockCode':'code', 'securityAbbr':'name'}
    rzrq.rename(columns=columns_map, inplace = True)
    # Add Missing Columns
    rzrq['rqylje'] = np.nan
    rzrq['rzrqye'] = np.nan
    return rzrq

def get_rzrq_sz_details(date):
    """
        获取深市融资融券明细数据
    Parameters
    --------
    date                日期，e.g. '2010-03-31'

    Return
    --------
    DataFrame
        date            日期
        code            股票代码
        name            股票名称
        rzye            融资余额(元)
        rzmre           融资买入额(元)
        rzche           融资偿还额(元)
        rqyl            融券余量
        rqmcl           融券卖出量
        rqchl           融券偿还量
        rqylje          融券余量金额(元)
        rzrqye          融资融券余额(元)
    """
    rzrq = ts.sz_margin_details(date)
    # Rename Columns
    columns_map = {'stockCode':'code', 'securityAbbr':'name', 'rqye':'rqylje', 'opDate':'date'}
    rzrq.rename(columns=columns_map, inplace = True)
    # Add Missing Columns
    rzrq['rzche'] = np.nan
    rzrq['rqchl'] = np.nan
    # Swith Columns
    date = rzrq.pop('date')
    rzrq.insert(0, 'date', date)
    rzye = rzrq.pop('rzye')
    rzrq.insert(3, 'rzye', rzye)
    rzche = rzrq.pop('rzche')
    rzrq.insert(5, 'rzche', rzche)
    rqyl = rzrq.pop('rqyl')
    rzrq.insert(6, 'rqyl', rqyl)
    rqchl = rzrq.pop('rqchl')
    rzrq.insert(8, 'rqchl', rqchl)
    return rzrq