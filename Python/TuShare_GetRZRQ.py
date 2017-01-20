# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 21:56:07 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import tushare as ts

#
# Get RZRQ Parameters
#
start_dates = ['2010-03-31','2011-01-01','2012-01-01','2013-01-01','2014-01-01',
              '2015-01-01','2016-01-01','2017-01-01']
end_dates   = ['2010-12-31','2011-12-31','2012-12-31','2013-12-31','2014-12-31',
              '2015-12-31','2016-12-31','2017-01-16']
path_datacenter = '../DataCenter/'

#
# Iteratively Get RZRQ Data Year-by-Year
#
date_number = len(start_dates)
if date_number == 0:
    raise SystemExit
if date_number != len(end_dates):
    print('start date number does not match end date number!')
    raise SystemExit

for i in range(date_number):
    #
    # Get RZRQ Data
    #
    start_date = start_dates[i]
    end_date = end_dates[i]
    sh_rzrq = ts.sh_margins(start=start_date, end=end_date)
    sz_rzrq = ts.sz_margins(start=start_date, end=end_date)
    
    #
    # Output RZRQ Data
    #
    sh_rzrq.to_csv(path_datacenter+'sh_rzrq'+str(i)+'.csv')
    sz_rzrq.to_csv(path_datacenter+'sz_rzrq'+str(i)+'.csv')