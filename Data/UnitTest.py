# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 11:36:28 2017

@author: freefrom
"""

import sys
sys.path.append('..')
import Common.Utilities as u
import Common.Constants as c

from GetFundamental import loadStockBasics

src_path = ''
tar_path = ''

def lshqCompare():
    # Check pre-requisite
    basics = loadStockBasics()
    if u.isNoneOrEmpty(basics):
        print('Need to have stock basics!')
        raise SystemExit

    # Iterate over all stocks
    stocks_number = len(basics)
    for i in range(stocks_number):
        stock_id = basics.loc[i,'code']
        file = c.file_trading_lshq % u.stockFileName(stock_id, False)
        fileCompare(src_path + file, tar_path + file)

def fileCompare(src_fullpath, tar_fullpath):
    # Check File Existence
    if not u.hasFile(src_fullpath):
        print('Source File %s Does Not Exist' % src_fullpath)
        raise SystemExit
    if not u.hasFile(tar_fullpath):
        print('Target File %s Does Not Exist' % tar_fullpath)
        raise SystemExit

    # Load Data Files
    src = u.read_csv(src_fullpath)
    tar = u.read_csv(tar_fullpath)
    src_row_number = len(src)
    tar_row_number = len(tar)
    src_col_number = len(src.columns)
    tar_col_number = len(tar.columns)
    matched = True
    print('File Compare Start: %s vs %s' % (src_fullpath, tar_fullpath))
    if src_row_number != tar_row_number:
        matched = False
        print('Row Number Un-matched')
    elif src_col_number != tar_col_number:
        matched = False
        print('Col Number Un-matched')
    else:
        for i in range(src_row_number):
            for j in range(src_col_number):
                if src.iloc[i,j] != tar.iloc[i,j]:
                    matched = False
                    print('Element(%s,%s) Un-matched' % (i,j))
    print('File Compare End: %s' % ('Matched' if matched else 'Un-Matched'))

###############################################################################

lshqCompare()