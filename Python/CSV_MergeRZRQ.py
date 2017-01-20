# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 23:24:50 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#
import pandas as pd

#
# Merge RZRQ Parameters
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

sh_rzrq_all = pd.DataFrame()
sz_rzrq_all = pd.DataFrame()

for i in range(date_number):
    #
    # Get RZRQ Data
    #
    start_date = start_dates[i]
    end_date = end_dates[i]
    sh_rzrq = pd.read_csv(path_datacenter+'sh_rzrq'+str(i)+'.csv')
    sz_rzrq = pd.read_csv(path_datacenter+'sz_rzrq'+str(i)+'.csv')
    
    #
    # Process RZRQ Data
    #
    sh_rzrq['opDate'] = pd.to_datetime(sh_rzrq['opDate'], format='%Y-%m-%d')
    sh_rzrq.set_index('opDate', inplace=True)
    sh_rzrq = sh_rzrq.sort_index(0)
    if is_debug:
        print(sh_rzrq.head(10))
        print(sh_rzrq.tail(10))
    sz_rzrq['opDate'] = pd.to_datetime(sz_rzrq['opDate'], format='%Y-%m-%d')
    sz_rzrq.set_index('opDate', inplace=True)
    sz_rzrq = sz_rzrq.sort_index(0)
    if is_debug:
        print(sz_rzrq.head(10))
        print(sz_rzrq.tail(10))
    
    #
    # Merge RZRQ Data
    #
    if (i == 0):
        sh_rzrq_all = sh_rzrq
        sz_rzrq_all = sz_rzrq
    else:
        sh_frames = [sh_rzrq_all, sh_rzrq]
        sh_rzrq_all = pd.concat(sh_frames)
        sz_frames = [sz_rzrq_all, sz_rzrq]
        sz_rzrq_all = pd.concat(sz_frames)

#
# Output RZRQ Data
#
sh_rzrq_all.to_csv(path_datacenter+'sh_rzrq'+'.csv')
sz_rzrq_all.to_csv(path_datacenter+'sz_rzrq'+'.csv')



















