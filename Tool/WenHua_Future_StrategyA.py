# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

def calcReturn(fullpath, base, coef, capital):
    df = pd.read_excel(fullpath)
    for column in ['win','win_accu','pos','pos_accu','drawdown','drawdown_base','drawdown_ratio','net_value']:
        df[column] = np.nan
    accu = 0.0
    do_accu = False
    accu_list = []
    drawdown_base = capital
    for i in range(len(df)):
        df.ix[i,'win'] = 1 if df.ix[i,'amount'] > 0 else -1
        if i == 0:
            df.ix[i,'win_accu'] = df.ix[i,'win']
            df.ix[i,'pos'] = df.ix[i,'win'] * base
            df.ix[i,'pos_accu'] = df.ix[i,'pos']
        else:
            df.ix[i,'win_accu'] = df.ix[i,'win'] + df.ix[i-1,'win_accu']
            if do_accu:
                df.ix[i,'pos'] = df.ix[i,'win'] * abs(df.ix[i-1,'pos']) * ((1.0-coef) if df.ix[i-1,'win'] > 0 else (1.0+coef))
            else:
                df.ix[i,'pos'] = df.ix[i,'win'] * base
            df.ix[i,'pos_accu'] = df.ix[i,'pos'] + df.ix[i-1,'pos_accu']

        # Calculate net value
        df.ix[i,'net_value'] = 1.0 + df.ix[i,'pos_accu'] / capital

        # Calculate draw down and check if we need to reset position
        df.ix[i,'drawdown'] = 0.0
        df.ix[i,'drawdown_ratio'] = 0.0
        df.ix[i,'drawdown_base'] = drawdown_base
        if (do_accu == False) and (df.ix[i,'win'] < 0):
            do_accu = True
            accu = 0.0
            accu_list = []
            drawdown_base = capital + (0.0 if i==0 else df.ix[i-1,'pos_accu'])
        if do_accu:
            accu += df.ix[i,'pos']
            accu_list.append(accu)
            if accu > 0:
                do_accu = False
            else:
                df.ix[i,'drawdown'] = accu
                df.ix[i,'drawdown_ratio'] = df.ix[i,'drawdown'] / drawdown_base
                df.ix[i,'drawdown_base'] = drawdown_base

    # Format Columns
    df['date'] = df['date'].map(lambda x: str(x[0:8]))
    df.set_index('date', inplace=True)
#    for column in ['pos','pos_accu','drawdown','drawdown_base','drawdown_ratio','net_value']:
#        df[column] = df[column].map(lambda x: '%.2f' % x)

    return df

df = calcReturn('D:\AssetMgmt\DataCenter\Tool\Cotton.xlsx', 3000, 0.1, 150000)
df.to_excel('D:\AssetMgmt\DataCenter\Tool\Cotton_10%.xlsx')
print df