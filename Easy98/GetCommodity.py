# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:11:13 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Commodity import get_commodity_price
import GlobalSettings as gs
import Constants as c
import Utilities as u

def getCommodityPrice(commodity):
    # Download Commodity Data
    data = get_commodity_price(commodity)
    if gs.is_debug:
        print(data.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(data):
        u.to_csv(data, c.path_dict['commodity'], c.file_dict['commodity'] % commodity)

def loadCommodityPrice(commodity):
    data = u.read_csv(c.fullpath_dict['commodity'] % commodity)
    return data

def validStockBasics(commodity, force_update):
    if force_update == True:
        return False
    else:
        return u.hasFile(c.fullpath_dict['commodity'] % commodity)

def extractCommodityPrice(commodity, column):
    # Load Commodity Data
    data = loadCommodityPrice(commodity)
    data.set_index(u'发布时间', inplace=True)
    print(data.head(10))

    # Extract Price Data based on Given Column
    market = data[column].drop_duplicates()
    market_number = len(market)
    print('Market Number:', market_number)
    print('Markets:', market)

    i = 0
    for m in market:
        print('Market %s: %s' % (i+1, m))
        m_name = 'Market_%s' % (i+1)
        m_data = data[data[column].isin([m])]
        if not u.isNoneOrEmpty(m_data):
            u.to_csv(m_data, c.path_dict['commodity'], c.file_dict['commodity_m'] % (commodity, m_name))
        i = i + 1

    '''
    drop_duplicates()后会保留原来的索引，以下为银报价机构的例子：
        Market Number: 8
        Markets: 发布时间
        2017-03-02    上海易贝
        2017-03-02    生泉金属
        2017-03-02    上海腾银
        2017-03-02    长江有色
        2017-03-02    上海华通
        2017-03-02    上海白银
        2017-02-08    瑜鸿实业
        2016-12-28     京慧诚
    '''