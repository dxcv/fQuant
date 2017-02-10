# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 18:10:01 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from GetFundamental import getStockBasics, loadStockBasics
import Utilities as u
import Constants as c

#
# Iteratively Update Databases
#
#getStockBasics()

#
# Iteratively Clean Database
#
basics = loadStockBasics()
print(basics.head(10))

# Format columns
#for i in range(10):
#    print(i, type(basics.loc[i,'timeToMarket']), basics.loc[i,'timeToMarket'])
basics['timeToMarket'] = basics['timeToMarket'].map(u.formatDateYYYYmmddInt64)
basics_number = len(basics)
for i in range(basics_number):
    if basics.loc[i,'timeToMarket'] == c.magic_date_YYYYmmdd_str:
        print(i, type(basics.loc[i,'timeToMarket']), basics.loc[i,'timeToMarket'])

# Save to CSV File
u.to_csv(basics, c.path_dict['basics'], c.file_dict['basics'])
