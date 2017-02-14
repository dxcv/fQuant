# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import os

dates = pd.date_range('2017-01-01', periods = 6, freq = 'D')
print(dates)

# Create CSV File
if not os.path.isfile('df.csv'):
    df = pd.DataFrame(np.random.randn(6,4), index = dates, columns = list('ABCD'))
    df.index.names = ['date']
    df.sort_index(ascending=True, inplace=True)
    print(df)
    df.to_csv('df.csv')

# Load CSV File
df = pd.read_csv('df.csv', index_col = 0)
print(df)

# Create More DataFrame Rows
dates_more = pd.date_range('2017-01-07', periods = 6, freq = 'D')
print(dates_more)

df_more = pd.DataFrame(np.random.randn(6,4), index = dates_more, columns = list('ABCD'))
df_more.index.names = ['date']
df_more.sort_index(ascending=True, inplace=True)
print(df_more)

df_more.to_csv('df.csv', header = False, mode = 'a')