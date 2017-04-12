# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:25:17 2017

@author: freefrom
"""

import sys
sys.path.append('..')

import Common.Utilities as u
import Common.GlobalSettings as gs
from Data.GetTrading import getDailyHFQ
from Index import load_component, generate_index

def generateIndex(index_name, base_date, base_point, weight_method, benchmark_id):
    # Load Index Component Stocks
    component = load_component(index_name)
    if u.isNoneOrEmpty(component):
        print('Index Component Not Available:', index_name)
        raise SystemExit
    if gs.is_debug:
        print(component.head(10))

    # Update Benchmark Index LSHQ to Latest
    date_start = u.dateFromStr(base_date)
    date_end = u.today()
    getDailyHFQ(stock_id=benchmark_id, is_index=True, date_start=date_start,
                date_end=date_end, time_to_market=None, incremental=True)
    print('Update Price:', benchmark_id)

    # Update Component Stock LSHQ to Latest
    component_number = len(component)
    for i in range(component_number):
        stock_id = u.stockID(component.ix[i,'code'])
        getDailyHFQ(stock_id=stock_id, is_index=False, date_start=date_start,
                    date_end=date_end, time_to_market=None, incremental=True)
        print('Update Price:', stock_id)

    # Generate Index
    generate_index(index_name, base_date, base_point, weight_method, benchmark_id)

###############################################################################

generateIndex('FeiYan_NewEnergyVehicle', '2016-12-30', 1000, 'EqualWeight', '000300')