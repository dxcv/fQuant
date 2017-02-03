# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:16:22 2017

@author: freefrom
"""

def quarterStartDay(quarter):
    return 1

def quarterEndDay(quarter):
    if quarter == 1 or quarter == 4:
        return 31
    else:
        return 30

def quarterStartMonth(quarter):
    return (quarter-1)*3 + 1

def quarterEndMonth(quarter):
    return quarter*3

def quarterDate(year, quarter):
    return str(year)+'-'+str(quarterEndMonth(quarter)).zfill(2)+'-'+str(quarterEndDay(quarter)).zfill(2)

