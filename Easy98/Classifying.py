# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:22:37 2017

@author: freefrom
"""

import tushare as ts

def get_industry_sina():
    '''
    函数功能：
    --------
    获取沪深上市公司所属的行业信息，基于sina财经对沪深股票进行的行业分类。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        industry,所属行业
    '''
    # Download data
    industry = ts.get_industry_classified()
    industry.rename(columns={'c_name':'industry'}, inplace=True)

    # Return Dataframe
    return industry

def get_concept_sina():
    '''
    函数功能：
    --------
    获取沪深上市公司所属的概念信息，基于sina财经对沪深股票进行的概念分类。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        concept,所属概念
    '''
    # Download data
    concept = ts.get_concept_classified()
    concept.rename(columns={'c_name':'concept'}, inplace=True)

    # Return Dataframe
    return concept

def get_area():
    '''
    函数功能：
    --------
    获取沪深上市公司所属的地域信息。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        area,所属地域
    '''
    # Download data
    area = ts.get_area_classified()

    # Return Dataframe
    return area

def get_sme():
    '''
    函数功能：
    --------
    获取所有中小板上市的公司。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
    '''
    # Download data
    sme = ts.get_sme_classified()

    # Return Dataframe
    return sme

def get_gem():
    '''
    函数功能：
    --------
    获取所有创业板上市的公司。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
    '''
    # Download data
    gem = ts.get_gem_classified()

    # Return Dataframe
    return gem

def get_st():
    '''
    函数功能：
    --------
    获取所有风险警示板的公司，即所有st的股票。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
    '''
    # Download data
    st = ts.get_st_classified()

    # Return Dataframe
    return st

def get_hs300():
    '''
    函数功能：
    --------
    获取所有沪深300指数的当前成分股及所占权重。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        date,日期
        weight,权重
    '''
    # Download data
    hs300 = ts.get_hs300s()

    # Return Dataframe
    return hs300

def get_sz50():
    '''
    函数功能：
    --------
    获取所有上证50指数的当前成分股。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
    '''
    # Download data
    sz50 = ts.get_sz50s()

    # Return Dataframe
    return sz50

def get_zz500():
    '''
    函数功能：
    --------
    获取所有中证500指数的当前成分股。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        date,日期
        weight,权重
    '''
    # Download data
    zz500 = ts.get_zz500s()

    # Return Dataframe
    return zz500

def get_terminated():
    '''
    函数功能：
    --------
    获取所有已经被终止上市的股票列表，数据从上交所获取，目前只在上交所有被终止上市的股票。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        oDate,上市日期
        tDate,终止上市日期
    '''
    # Download data
    terminated = ts.get_terminated()

    # Return Dataframe
    return terminated

def get_suspended():
    '''
    函数功能：
    --------
    获取所有被暂停上市的股票列表，数据从上交所获取，目前只在上交所有被暂停上市的股票。

    输入参数：
    --------
    无

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        oDate,上市日期
        tDate,暂停上市日期
    '''
    # Download data
    suspended = ts.get_suspended()

    # Return Dataframe
    return suspended
