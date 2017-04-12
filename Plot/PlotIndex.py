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

def plot_index(index_name, benchmark_name):
    # Load Index Data File
    index_path = c.path_dict['index']
    index_file = c.file_dict['index_r'] % index_name
    df = u.read_csv(index_path + index_file)

    # Plot Figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    fig.set_size_inches(32, 18)

    # Plot Sub-figure 1
    title = '%s vs. %s' % (index_name, benchmark_name)
    ax1.set_title(title, fontsize=14)
    ax1.set_xlabel('')
    ax1.set_ylabel('Ratio')
    for column in ['ratio', 'b_ratio']:
        df.plot(x='date', y=column, ax=ax1)

    # Plot Sub-figure 2
    title = 'Index %s' % index_name
    ax2.set_title(title, fontsize=14)
    ax2.set_xlabel('')
    ax2.set_ylabel('Close Price')
    df.plot(x='date', y='index', ax=ax2)

    # Plot Sub-figure 3
    title = 'Index %s' % benchmark_name
    ax3.set_title(title, fontsize=14)
    ax3.set_xlabel('')
    ax3.set_ylabel('Close Price')
    df.plot(x='date', y='b_index', ax=ax3)

    # Common Format for Both Sub-figures
    for ax in [ax1, ax2, ax3]:
        ax.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

    # Save Figure
    fig_key = 'fig_index'
    fig_path = c.path_dict[fig_key]
    fig_file = c.file_dict[fig_key] % (index_name + '_' + u.dateToStr(u.today()))
    u.saveFigure(fig, fig_path, fig_file)