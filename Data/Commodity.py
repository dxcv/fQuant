# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:48:21 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import sys
import lxml.html
import time
from pandas.compat import StringIO
import pandas as pd
import numpy as np
try:
    from urllib.request import urlopen, Request, quote
except ImportError:
    from urllib2 import urlopen, Request, quote
import Common.GlobalSettings as gs
import Common.Utilities as u

#
# Constants and Parameters
#
DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'
COMMODITY_URL = 'http://www.100ppi.com/price/plist-%s-%s.html'

#
# Functions and Utilities
#
PY3 = (sys.version_info[0] >= 3)
def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()

def check_network(url):
    import httplib2
    try:
        http = httplib2.Http()
        resp, content = http.request(url)
    except:
        return 0
    return 1

def get_commodity_price(code, retry_count=3, pause=0.01):
    """
        获取生意社（100PPI）商品价格
    Parameters
    --------
    code:string    商品代码 e.g. 67(钴的代码)

    Return
    --------
    DataFrame
        发布时间
        报价机构
        报价类型
        报价
        规格
        产地
    """

    # Download Commodity Data
    pageNo = 1
    df_all = _get_commodity_price(code, pageNo, pd.DataFrame(), retry_count, pause)
    if not u.isNoneOrEmpty(df_all):
        df_all.drop_duplicates(inplace=True)
        df_all.set_index(u'发布时间', inplace=True)
    return df_all

def _get_commodity_price(code, pageNo, df_all, retry_count, pause):
    # Compose URL based on Given Commodity
    url = COMMODITY_URL%(code, pageNo)
    print('Getting URL:', url)

    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(url)
            text = urlopen(request, timeout=10).read()
            text = text.decode('utf8')
            html = lxml.html.parse(StringIO(text))
            tables = html.xpath('//table[@class=\"lp-table mb15\"]')
            tables_number = len(tables)
            print('Number of tables = %s' % tables_number)

            if (tables_number != 1):
                print('Unknown format: more than one table exist.\n')
                raise SystemExit

            records = tables[0].xpath('tr')
            records_number = len(records)
            print('Number of records = %s' % len(records))
            if records_number < 1:
                continue

            # Extract Columns
            head = records[0]
            columns = head.xpath('th')
            columns_number = len(columns)
            commodity_columns = []
            for i in range(columns_number):
                column_name = columns[i].xpath('string(.)')
                commodity_columns.append(column_name)
                print('Table Head %d' % i, column_name)

            # Init all elements to NaN
            records_number = int(records_number - 1)
            print('Records number = ' + str(records_number))
            print('Columns number = ' + str(columns_number))
            data_init = np.random.randn(records_number * columns_number)
            for i in range(records_number * columns_number):
                data_init[i] = np.nan
            df = pd.DataFrame(data_init.reshape(records_number, columns_number),
                              columns = commodity_columns)

            # Extract records one by one
            for r in range(records_number): # Skip record 0, which is table header
                record = records[r+1]
                for i in range(columns_number):
                    xpath_key = 'td[%d]' % (i+1)
                    if i == 0:
                        item = record.xpath(xpath_key + '/div/a')
                    elif i == 4:
                        item = record.xpath(xpath_key + '/div')
                    else:
                        item = record.xpath(xpath_key)

                    if len(item) == 1:
                        item = str(item[0].xpath('string(.)'))
                        item = item.strip() # Remove white space on both sides

                    if len(item) != 0: # has data
                        df.iloc[r, i] = item
            print('Getting URL Complete:', url)
            if gs.is_debug:
                print(df.head(10))

            # Merge with Previous Pages
            if pageNo == 1:
                df_all = df
            else:
                df_all = df_all.append(df, ignore_index=True)
            if gs.is_debug:
                print(df_all.tail(10))
            nextPage = html.xpath('//div[@class=\"page-inc\"]/a[last()]')
            if len(nextPage)>0:
                nextPage = nextPage[0].xpath('string(.)')
                print(nextPage)
                if not nextPage.isdigit(): # 有“下一页”
                    pageNo = pageNo + 1
                    return _get_commodity_price(code, pageNo, df_all, retry_count, pause)
                else: # 没有“下一页”
                    return df_all
            else:
                return df_all
        except Exception as e:
            print('Exception:', e)
            pass
#    raise IOError(NETWORK_URL_ERROR_MSG)
    print('Getting URL Imcomplete:', url)
    return _get_commodity_price(code, pageNo, df_all, retry_count, pause)


