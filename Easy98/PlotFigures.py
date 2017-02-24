# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:25:05 2017

@author: freefrom
"""

import matplotlib.pyplot as plt
import Constants as c
import Utilities as u

from CalcIndicators import loadHPE

def plotHPE(stock_id, period, ratio):
    # Check Input Parameters
    if not isinstance(stock_id, str) or not isinstance(period, str):
        print('Incorrect type of one or more input parameters!')
        raise SystemExit

    # Check Period
    period_types = ['W','M','Q']
    if not period in period_types:
        print('Un-supported period type - should be one of:', period_types)
        raise SystemExit

    # Check Ratio
    ratio_types = ['PE','EP']
    if not ratio in ratio_types:
        print('Un-supported ratio type - should be one of:', ratio_types)
        raise SystemExit

    # Check Pre-requisite: HPE File
    key = 'hpe' if ratio == 'PE' else 'hep'
    path = c.path_dict[key] % period
    file = c.file_dict[key] % (period, stock_id)
    hpe_fullpath = path+file
    if not u.hasFile(hpe_fullpath):
        print('Require File Exists:', hpe_fullpath)
        raise SystemExit

    # Load Data File
    hpe = loadHPE(stock_id=stock_id, period=period, ratio=ratio)

    # Plot Figure
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
#    fig = plt.figure()
    fig.set_size_inches(32, 18)

    # Plot Sub-figure 1
#    ax1 = plt.subplot(211)
    ratio_name = 'P/E Ratio' if ratio == 'PE' else 'E/P Ratio'
    title = ratio_name + ' Ratio of Stock %s' % stock_id
    ax1.set_title(title, fontsize=14)
    ax1.set_xlabel('')
    ax1.set_ylabel(ratio_name)
    if ratio == 'PE':
#       hpe.plot(x='date', y='pe_high', ax=ax1)
        hpe.plot(x='date', y='pe_close', ax=ax1)
#       hpe.plot(x='date', y='pe_low', ax=ax1)
    else:
#       hpe.plot(x='date', y='ep_high', ax=ax1)
        hpe.plot(x='date', y='ep_close', ax=ax1)
#       hpe.plot(x='date', y='ep_low', ax=ax1)

    # Plot Sub-figure 2
#    ax2 = plt.subplot(212)
    ax2.set_title('Price of Stock %s' % stock_id, fontsize=14)
    ax2.set_xlabel('')
    ax2.set_ylabel('Price')
#    hpe.plot(x='date', y='high', ax=ax2)
    hpe.plot(x='date', y='close', ax=ax2)
#    hpe.plot(x='date', y='low', ax=ax2)
    # Common Format for Both Sub-figures
    for ax in [ax1, ax2]:
        ax.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

    # Save Figure
    fig_key = 'fig_hpe' if ratio == 'PE' else 'fig_hep'
    fig_path = c.path_dict[fig_key] % period
    fig_file = c.file_dict[fig_key] % (period, stock_id)
    u.saveFigure(fig, fig_path, fig_file)
