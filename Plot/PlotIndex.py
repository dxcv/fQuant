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

    # Define Font
    font = {'family' : 'serif',
            'color'  : 'black',
            'weight' : 'normal',
            'size'   : 18,
    }

    # Plot Sub-figure 1
    title = '%s vs. %s' % (index_name, benchmark_name)
    ax1.set_title(title, fontdict=font)
    ax1.set_xlabel('', fontdict=font)
    ax1.set_ylabel('Ratio', fontdict=font)
    for column in ['ratio', 'b_ratio']:
        df.plot(x='date', y=column, ax=ax1)

    # Plot Sub-figure 2
    title = 'Index %s' % index_name
    ax2.set_title(title, fontdict=font)
    ax2.set_xlabel('', fontdict=font)
    ax2.set_ylabel('Close Price', fontdict=font)
    df.plot(x='date', y='index', ax=ax2)

    # Plot Sub-figure 3
    title = 'Index %s' % benchmark_name
    ax3.set_title(title, fontdict=font)
    ax3.set_xlabel('', fontdict=font)
    ax3.set_ylabel('Close Price', fontdict=font)
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

def plot_index_series(index_names, series_name, benchmark_name):
    # Load Index Data Files
    series_path = c.path_dict['index']
    series_file = c.file_dict['index_r'] % series_name
    df = u.read_csv(series_path + series_file)

    # Plot Figure
    fig = plt.figure(figsize=(32, 18), dpi=72, facecolor="white")
    axes = plt.subplot(111)
    axes.cla() # Clear Axes

    # Define Font
    font = {'family' : 'serif',
            'color'  : 'black',
            'weight' : 'normal',
            'size'   : 18,
    }

    # Plot Sub-figure 1
    title = '%s vs. %s' % (series_name, benchmark_name)
    plt.title(title, fontdict=font)
    axes.set_xlabel('', fontdict=font)
    axes.set_ylabel('Ratio', fontdict=font)
    df.plot(x='date', y='ratio_benchmark', ax=axes, color='grey', lw=2.0, ls='--')
    index_number = len(index_names)
    for i in range(index_number):
        index_name = index_names[i]
        column = 'ratio_'+index_name
        df.plot(x='date', y=column, ax=axes)

    # Common Format for Both Sub-figures
    axes.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.show()

    # Save Figure
    fig_key = 'fig_index'
    fig_path = c.path_dict[fig_key]
    fig_file = c.file_dict[fig_key] % (series_name + '_' + u.dateToStr(u.today()))
    u.saveFigure(fig, fig_path, fig_file)