# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 18:56:19 2017

@author: freefrom
"""

import sys
sys.path.append('..')

from Index import find_stock_close
from Data.GetTrading import loadDailyQFQ

import numpy as np

def unitTest1():
    df = loadDailyQFQ('300617', False)
    if find_stock_close(df, '2017-01-01') != 35.11:
        print('#1 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '2017-02-28') != 35.11:
        print('#2 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '2017-03-01') != 38.62:
        print('#3 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '2017-03-16') != 110.19:
        print('#4 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '2017-04-06') != 93.00:
        print('#5 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '2017-04-07') != 89.00:
        print('#6 Unit Test for Index::find_stock_close Failed!')
    if find_stock_close(df, '3000-01-01') != 89.00:
        print('#7 Unit Test for Index::find_stock_close Failed!')

def unitTest2():
    epsilon = 0.0001
    df = loadDailyQFQ('002664', False)
    print(df.tail(10))
    if np.abs(find_stock_close(df, '2017-01-01') - 25.38988581) > epsilon:
        print('#1 Unit Test for Index::find_stock_close Failed!')
###############################################################################

unitTest1()
unitTest2()