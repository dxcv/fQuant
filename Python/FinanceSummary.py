# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:38:12 2017

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
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

#
# Constants and Parameters
#
stock_ids  = ['300059','600036','000002','002024']

DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'
FINANCE_SUMMARY_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%s.phtml'
FINANCE_SUMMARY_COLS = ['date', 'bvps', 'eps', 'cfps', 'zbgj', 'gdzchj',
                        'ldzchj', 'zczj', 'cqfzhj', 'zrywsr', 'cwfy', 'jlr']
FINANCE_SUMMARY_STRIP = len(FINANCE_SUMMARY_COLS) + 1 # 1 for a separator line
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

def get_finance_summary(stock_id, retry_count=3, pause=0.001):
    """
        获取财务摘要表数据
    Parameters
    --------
    stock_id:string    股票代码 e.g. 600848

    Return
    --------
    DataFrame
        date,截止日期
        bvps,每股净资产
        eps,每股收益
        cfps,每股现金含量
        zbgj,每股资本公积金
        gdzchj,固定资产合计
        ldzchj,流动资产合计
        zczj,资产总计
        cqfzhj,长期负债合计
        zrywsr,主营业务收入
        cwfy,财务费用
        jlr,净利润
    """
    _write_head()
    _write_console()

    for _ in range(retry_count):
        print('\n')
        time.sleep(pause)
        df = pd.DataFrame()
        try:
            request = Request(FINANCE_SUMMARY_URL%(stock_id))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            tables = html.xpath('//table[@id=\"FundHoldSharesTable\"]')
            tables_number = len(tables)            
            print('Number of tables = %s' % tables_number)
            
            if (tables_number != 1):
                print('Unknown format: more than one table exist.\n')
                raise SystemExit

            items = tables[0].xpath('tr')
            items_number = len(items)
            print('Number of items = %s' % len(items))
            print('Type of items = %s' % type(items))

            if (items_number % FINANCE_SUMMARY_STRIP) != 0:
                print('Unknown format: incorrect record strip.\n')
                raise SystemExit

            # Init all elements to NaN
            records_number = int(items_number / FINANCE_SUMMARY_STRIP)
            columns_number = len(FINANCE_SUMMARY_COLS)
            print('Records number = ' + str(records_number))
            print('Columns number = ' + str(columns_number))
            data_init = np.random.randn(records_number * columns_number)
            for i in range(records_number * columns_number):
                data_init[i] = np.nan
            df = pd.DataFrame(data_init.reshape(records_number, columns_number), 
                              columns = FINANCE_SUMMARY_COLS)

            # Extract records one by one
            for r in range(records_number):
                print('\n\nRecord %s' % r)
                for i in range(columns_number):
                    item_index = r * FINANCE_SUMMARY_STRIP + i
                    item = items[item_index]
                    #print('Type of item = %s' % type(item))
                    
                    if r == 0: # First record contains hyperlink
                        if i == 0:
                            item = item.xpath('td[2]/strong')
                        else:
                            item = item.xpath('td[2]/a')
                    else:
                        if i == 0:
                            item = item.xpath('td[2]/strong')
                        else:
                            item = item.xpath('td[2]')
                    #print('Type of item = %s' % type(item))
                    #print('Item number = %s' % len(item))

                    if len(item) == 1:                        
                        item = str(item[0].xpath('string(.)')).replace('元', '')
                        item = item.strip() # Remove white space on both sides
                        #print('Type of item = %s' % type(item))
                        print(item)
                            
                        if len(item) != 0: # has data
                            df.iloc[r, i] = item

            # Format df
            df.set_index('date', inplace=True)
            
        except ValueError as e:
            # 读不到数据
            return None
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(NETWORK_URL_ERROR_MSG)

