# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:34:26 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts
import ConstantData as cd

#
# Get and Save Stock Basics
#
basics = ts.get_stock_basics()
if cd.is_debug:
    print(basics.head(10))
#basics.index = basics.index.map(lambda x:str(x).zfill(6)) # 'code'

basics.to_csv(cd.path_datacenter + cd.file_stockbasics, encoding='utf-8')
