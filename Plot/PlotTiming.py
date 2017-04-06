# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 16:05:55 2017

@author: freefrom
"""

import matplotlib.pyplot as plt

import sys
sys.path.append('..')

import Common.Constants as c
import Common.Utilities as u

def plotTiming(stock_id, is_index):
    # Load Timing Data File
    stock_filename = u.stockFileName(stock_id, is_index)
    file_postfix = 'PriceFollow_%s_All' % stock_filename
    df = u.read_csv(c.path_dict['strategy'] + c.file_dict['strategy'] % file_postfix)
    df = df[-60:]

    # Plot Figure
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.set_size_inches(32, 18)

    # Plot Sub-figure 1
    title = 'Automatic Trend Prediction of %s' % u.stockFileName(stock_id, is_index)
    ax1.set_title(title, fontsize=14)
    ax1.set_xlabel('')
    ax1.set_ylabel('Trend Prediction')
    for column in ['wpredict_0.03', 'wpredict_0.05', 'wpredict_0.08', 'wpredict_0.13', 'wpredict_0.21']:
        df.plot(x='date', y=column, ax=ax1)

    # Plot Sub-figure 2
    title = 'Price of %s' % stock_filename
    ax2.set_title(title, fontsize=14)
    ax2.set_xlabel('')
    ax2.set_ylabel('Close Price')
    df.plot(x='date', y='close', ax=ax2)

    # Common Format for Both Sub-figures
    for ax in [ax1, ax2]:
        ax.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

    # Save Figure
    fig_key = 'fig_timing'
    fig_path = c.path_dict[fig_key]
    fig_file = c.file_dict[fig_key] % (stock_filename + '_' + u.dateToStr(u.today()))
    u.saveFigure(fig, fig_path, fig_file)