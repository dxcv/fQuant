# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:28:37 2017

@author: freefrom
"""

import Common.GlobalSettings as gs
import Common.Constants as c
import Common.Utilities as u
from Data.GetTrading import loadDailyQFQ
from Data.GetClassifying import loadCXG
import pandas as pd
import numpy as np

bar_range_long = 21
bar_range_short = 13
r_range = 20

def strategyAncleXu(stock_id, is_index):
    # Load Stock Daily QFQ Data
    lshq = loadDailyQFQ(stock_id, is_index)
    if u.isNoneOrEmpty(lshq):
        raise SystemExit

    # Calculate Long Range High/Low
    lshq['range_high_long'] = 0.0
    lshq['range_low_long'] = 0.0
    lshq_number = len(lshq)
    for i in range(lshq_number):
        index_beg = (i-bar_range_long) if (i-bar_range_long) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'range_high_long'] = np.max(lshq['high'][index_beg:index_end])
        lshq.ix[i, 'range_low_long']  = np.min(lshq['low'][index_beg:index_end])

    # Calculate Short Range High/Low
    lshq['range_high_short'] = 0.0
    lshq['range_low_short'] = 0.0
    for i in range(lshq_number):
        index_beg = (i-bar_range_short) if (i-bar_range_short) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'range_high_short'] = np.max(lshq['high'][index_beg:index_end])
        lshq.ix[i, 'range_low_short']  = np.min(lshq['low'][index_beg:index_end])

    # Calculate R and Avg(R)
    lshq['R'] = 0.0
    lshq['Avg_R'] = 0.0
    for i in range(lshq_number):
        prev_close = lshq.ix[i-1, 'close'] if i > 0 else lshq.ix[i, 'open']
        high = lshq.ix[i, 'high']
        low = lshq.ix[i, 'low']
        lshq.ix[i, 'R'] = np.max([np.abs(high-low), np.abs(high-prev_close), np.abs(low-prev_close)])
        index_beg = (i-r_range) if (i-r_range) > 0 else 0
        index_end = i if i > 0 else 1
        lshq.ix[i, 'Avg_R'] = np.mean(lshq['R'][index_beg:index_end])

    # Save to CSV File
    file_postfix = 'AncleXu_%s' % u.stockFileName(stock_id, is_index)
    u.to_csv(lshq, c.path_dict['strategy'], c.file_dict['strategy'] % file_postfix)

    # Run Strategy
    lshq['long_open'] = False
    lshq['long_close'] = False
    lshq['short_open'] = False
    lshq['short_close'] = False
    has_long_open = False
    has_short_open = False
    event_index = []
    for i in range(lshq_number):
        close = lshq.ix[i, 'close']
        range_high_long = lshq.ix[i, 'range_high_long']
        range_low_long = lshq.ix[i, 'range_low_long']
        range_high_short = lshq.ix[i, 'range_high_short']
        range_low_short = lshq.ix[i, 'range_low_short']
        has_event = False
        if has_long_open == False:
            if close > range_high_long: # Long Open
                lshq.ix[i, 'long_open'] = True
                has_long_open = True
                has_event = True
        else:
            if close < range_low_short:
                lshq.ix[i, 'long_close'] = True
                has_long_open = False
                has_event = True
        if has_short_open == False:
            if close < range_low_long: # Short Open
                lshq.ix[i, 'short_open'] = True
                has_short_open = True
                has_event = True
        else:
            if close > range_high_short:
                lshq.ix[i, 'short_close'] = True
                has_short_open = False
                has_event = True
        if has_event:
            event_index.append(i)

    # Strategy Statistics
    stats = lshq.ix[event_index, ['date','close','long_open','long_close','short_open','short_close']]
    if gs.is_debug:
        print(stats.head(10))
    stats_number = len(stats)
    long_number = 0
    short_number = 0
    long_open_date = []
    long_open_price = []
    long_close_date = []
    long_close_price = []
    short_open_date = []
    short_open_price = []
    short_close_date = []
    short_close_price = []
    for i in range(stats_number):
        index = stats.index[i]
        print('Type is:', type(stats.ix[index, 'long_open']))
        if stats.ix[index, 'long_open'] == True: # Long Open
            long_open_date.append(stats.ix[index, 'date'])
            long_open_price.append(stats.ix[index, 'close'])
        if stats.ix[index, 'long_close'] == True: # Long Close
            long_close_date.append(stats.ix[index, 'date'])
            long_close_price.append(stats.ix[index, 'close'])
            long_number = long_number + 1
        if stats.ix[index, 'short_open'] == True: # Short Open
            short_open_date.append(stats.ix[index, 'date'])
            short_open_price.append(stats.ix[index, 'close'])
        if stats.ix[index, 'short_close'] == True: # Short Close
            short_close_date.append(stats.ix[index, 'date'])
            short_close_price.append(stats.ix[index, 'close'])
            short_number = short_number + 1

    # Profit Statistics
    long_profit = []
    total_long_profit = 0.0
    for i in range(long_number):
        profit = long_close_price[i] - long_open_price[i]
        long_profit.append(profit)
        total_long_profit = total_long_profit + profit
    short_profit = []
    total_short_profit = 0.0
    for i in range(short_number):
        profit = short_open_price[i] - short_close_price[i]
        short_profit.append(profit)
        total_short_profit = total_short_profit + profit
    print('\nStrategy Complete:')
    print('Total Long Trading = %04d, Total Long Profit = %.2f' % (long_number, total_long_profit))
    print('Total Short Trading = %04d, Total Short Profit = %.2f' % (short_number, total_short_profit))
    print('Total Trading = %04d, Total Profit = %.2f' % (long_number + short_number, total_long_profit + total_short_profit))
    for i in range(long_number):
        print('  B%04d, Open (%s) = %4.2f, Close (%s) = %4.2f, Profit = %4.2f' % (i+1, long_open_date[i], long_open_price[i], long_close_date[i], long_close_price[i], long_profit[i]))
    print('  -------------------------------------------------------------------')
    for i in range(short_number):
        print('  S%04d, Open (%s) = %4.2f, Close (%s) = %4.2f, Profit = %4.2f' % (i+1, short_open_date[i], short_open_price[i], short_close_date[i], short_close_price[i], short_profit[i]))

    # Trading Dataframe
    data_index_number = long_number+short_number
    data_columns=['type','open_date','open_price','close_date','close_price','profit']
    data_columns_number = len(data_columns)
    data_init = np.random.randn(data_index_number * data_columns_number)
    for i in range(data_index_number * data_columns_number):
        data_init[i] = np.nan
    data_index = []
    for i in range(data_index_number):
        data_index.append(i)
    trading = pd.DataFrame(data_init.reshape(data_index_number, data_columns_number),
                           index = data_index, columns = data_columns)
    for i in range(long_number):
        trading.ix[i,'type'] = 'B%04d'%(i+1)
        trading.ix[i,'open_date'] = long_open_date[i]
        trading.ix[i,'open_price'] = long_open_price[i]
        trading.ix[i,'close_date'] = long_close_date[i]
        trading.ix[i,'close_price'] = long_close_price[i]
        trading.ix[i,'profit'] = long_profit[i]
    for i in range(short_number):
        trading.ix[i+long_number,'type'] = 'S%04d'%(i+1)
        trading.ix[i+long_number,'open_date'] = short_open_date[i]
        trading.ix[i+long_number,'open_price'] = short_open_price[i]
        trading.ix[i+long_number,'close_date'] = short_close_date[i]
        trading.ix[i+long_number,'close_price'] = short_close_price[i]
        trading.ix[i+long_number,'profit'] = short_profit[i]

    # Save to CSV File
    u.to_csv(trading, c.path_dict['strategy'], c.file_dict['strategy_r'] % file_postfix)

def strategyCXG(hc_segments = 5, yk_segments = 10):
    '''
    函数功能：
    --------
    运行次新股策略：选出打开涨停板后仍旧创新高的个股。

    输入参数：
    --------
    hc_segments, 回撤分段数量
    yk_segments, 盈亏分段数量

    输出参数：
    --------
    DataFrame
        code,代码
        name,名称
        industry,所属行业
        area,地区
        timeToMarket,上市日期
        ss_price, 上市价
        kb_price, 开板价
        zx_price, 最新价
        ss_ratio, 上市以来涨幅
        kb_ratio, 开板以来涨幅
        new_high, 是否创开板后新高

    假定：CXG数据文件和对应的日后复权数据文件都已经更新。
    '''
    # Load CXG Data
    cxg = loadCXG()
    cxg_number = len(cxg)

    # Init New Columns
    for column in ['ss_price','kb_price','zx_price','ss_ratio','kb_ratio','kb_index']:
        cxg[column] = 0
    for column in ['kb','high_than_kb','new_high']:
        cxg[column] = False

    # Setup Back Test Parameters
    # 第一组：给定回撤比例（相对于开板价），统计能够获得的最高收益及比例
    hc_price_columns = []
    hc_ratio_columns = []
    hc_index_columns = []
    hc_ratios = []
    for j in range(hc_segments):
        hc_price_columns.append('hc_%d_price' % (10*(j+1)))
        hc_ratio_columns.append('hc_%d_ratio' % (10*(j+1)))
        hc_index_columns.append('hc_%d_index' % (10*(j+1)))
        hc_ratios.append(0.1*(j+1))
    hc_price_columns.append('hc_high_price')
    hc_ratio_columns.append('hc_high_ratio')
    hc_index_columns.append('hc_high_index')
    hc_price_columns.append('hc_low_price')
    hc_ratio_columns.append('hc_low_ratio')
    hc_index_columns.append('hc_low_index')
    for column in hc_price_columns:
        cxg[column] = 0
    for column in hc_ratio_columns:
        cxg[column] = 0
    for column in hc_index_columns:
        cxg[column] = 0
    print(hc_price_columns)
    print(hc_ratio_columns)
    print(hc_index_columns)
    print(hc_ratios)
    # 第二组：给定止盈止损区间，统计止盈止损触及的次数
    yk_columns = []
    yk_ratios = []
    for j in range(yk_segments):
        ratio = float(j+1) / float(yk_segments)
        yk_columns.append('yk_%.1f%%' % (100.0 * ratio))
        yk_ratios.append(ratio)
    for column in yk_columns:
        cxg[column] = 0
    print(yk_columns)
    print(yk_ratios)

    #
    # Iterate Over Each CXG Stock Data - Find KaiBai and Back Test
    #
    kb_type = 'close'
    for i in range(cxg_number):
        stock_id = u.stockID(cxg.ix[i,'code'])
        # Load Stock Daily QFQ Data
        lshq = loadDailyQFQ(stock_id, False)
        if u.isNoneOrEmpty(lshq):
            continue
        else:
            lshq.set_index('date', inplace=True)
            lshq.sort_index(ascending = True, inplace=True)
            cxg.ix[i,'ss_price'] = lshq.ix[0,'open']
            cxg.ix[i,'zx_price'] = lshq.ix[-1,'close']
            cxg.ix[i,'ss_ratio'] = cxg.ix[i,'zx_price']/cxg.ix[i,'ss_price'] - 1

            # Whether Reach New High After KaiBan
            lshq_number = len(lshq)
            kb_price = lshq.ix[0,kb_type]
            kb_index = 0
            # Find KaiBan Price and Index
            for j in range(1,lshq_number):
                if lshq.ix[j,'high'] > lshq.ix[j,'low']:
                    kb_price = lshq.ix[j,kb_type]
                    kb_index = j
                    break
            if kb_index == 0:
                cxg.ix[i,'kb'] = False
                cxg.ix[i,'kb_index'] = lshq_number # 连续封板的次数
                cxg.ix[i,'high_than_kb'] = 'No'
                cxg.ix[i,'new_high'] = 'No'
            else:
                cxg.ix[i,'kb'] = True
                ls_high = kb_price
                for j in range(kb_index,lshq_number):
                    ls_high = lshq.ix[j,'close'] if lshq.ix[j,'close'] > ls_high else ls_high
                cxg.ix[i,'kb_price'] = kb_price
                cxg.ix[i,'kb_index'] = kb_index # 连续封板的次数，也是开板的索引
                cxg.ix[i,'kb_ratio'] = cxg.ix[i,'zx_price']/cxg.ix[i,'kb_price'] - 1
                cxg.ix[i,'high_than_kb'] = 'Yes' if cxg.ix[i,'zx_price'] >= kb_price else 'No'
                cxg.ix[i,'new_high'] = 'Yes' if cxg.ix[i,'zx_price'] == ls_high else 'No'

            # Only back test stocks that have already KaiBan
            if cxg.ix[i,'kb'] == False:
                continue

            # Back Test - Group 1
            high_since_kb = kb_price
            low_since_kb = kb_price
            high_index = kb_index
            low_index = kb_index
            for j in range(kb_index+1, lshq_number):
                close = lshq.ix[j,'close']
                if close > high_since_kb:
                    high_since_kb = close
                    high_index = j
                if close < low_since_kb:
                    low_since_kb = close
                    low_index = j
                high_ratio = high_since_kb/kb_price - 1
                low_ratio = 1 - low_since_kb/kb_price
                # Update high_since_kb for each bucket
                for k in range(hc_segments):
                    hc_ratio = hc_ratios[k]
                    if j == kb_index+1 or low_ratio <= hc_ratio: # First bar after KaiBan may exceed threshold
                        cxg.ix[i,hc_price_columns[k]] = high_since_kb # 'hc_%d_price'
                        cxg.ix[i,hc_ratio_columns[k]] = high_ratio # 'hc_%d_ratio'
                        cxg.ix[i,hc_index_columns[k]] = high_index # 'hc_%d_index'
            # Update high_since_kb
            cxg.ix[i,hc_price_columns[-2]] = high_since_kb
            cxg.ix[i,hc_ratio_columns[-2]] = high_since_kb/kb_price - 1
            cxg.ix[i,hc_index_columns[-2]] = high_index
            # Update low_since_kb
            cxg.ix[i,hc_price_columns[-1]] = low_since_kb
            cxg.ix[i,hc_ratio_columns[-1]] = 1 - low_since_kb/kb_price
            cxg.ix[i,hc_index_columns[-1]] = low_index

            # Back Test - Group 2
            high_since_kb = kb_price
            low_since_kb = kb_price
            high_index = kb_index
            low_index = kb_index
            for j in range(kb_index+1, lshq_number):
                close = lshq.ix[j,'close']
                ratio_prev = 2.0
                ratio = 2.0
                value = 0
                if close > high_since_kb: # 收盘价创开板以来新高
                    ratio_prev = high_since_kb/kb_price - 1
                    ratio = close/kb_price - 1
                    value = 1 * j
                    high_since_kb = close
                elif close < low_since_kb: # 收盘价创开板以来新低
                    ratio_prev = 1 - low_since_kb/kb_price
                    ratio = 1 - close/kb_price
                    value = -1 * j
                    low_since_kb = close
                # Fill Corresponding yk_segments
                for k in range(yk_segments):
                    yk_ratio = yk_ratios[k]
                    if cxg.ix[i,yk_columns[k]] == 0: # This range has NOT been touched before
                        if yk_ratio > ratio_prev and yk_ratio <= ratio: # For those ranges contain yk_ratio
                            cxg.ix[i,yk_columns[k]] = value

    # Format Data Frame
    jg_columns = ['ss_price','kb_price','zx_price','ss_ratio','kb_ratio']
    data_columns = [jg_columns,hc_price_columns,hc_ratio_columns,hc_index_columns,yk_columns]
    for column in [x for j in data_columns for x in j]:
        cxg[column] = cxg[column].map(lambda x: '%.3f' % x)
        cxg[column] = cxg[column].astype(float)
    cxg.set_index('code', inplace=True)

    # Save to CSV File
    file_postfix = 'CXG'
    u.to_csv(cxg, c.path_dict['strategy'], c.file_dict['strategy_r'] % file_postfix)

    # Statistics for Back Test - Group 2
    stats_indexs = yk_columns
    stats_indexs_number = len(stats_indexs)
    stats_columns = ['ratio','win_count','win_mean','win_std','win_min','win_25%','win_50%','win_75%','win_max',
                     'lose_count','lose_mean','lose_std','lose_min','lose_25%','lose_50%','lose_75%','lose_max']
    stats_columns_number = len(stats_columns)
    data_init = np.random.randn(stats_indexs_number * stats_columns_number)
    for i in range(stats_indexs_number * stats_columns_number):
        data_init[i] = np.nan
    stats = pd.DataFrame(data_init.reshape(stats_indexs_number, stats_columns_number),
                         index = stats_indexs, columns = stats_columns)
    for r in range(yk_segments):
        win_days = []
        lose_days = []
        for i in range(cxg_number):
            value = cxg.ix[cxg.index[i],yk_columns[r]]
            if value == 0: # No data
                continue
            elif value > 0:
                win_days.append(value)
            else:
                lose_days.append(-value)
        stats_win_days = pd.Series(win_days).describe()
        stats_lose_days = pd.Series(lose_days).describe()
        for j in range(8):
            stats.iloc[r, 1+j] = stats_win_days.iloc[j]
            stats.iloc[r, 9+j] = stats_lose_days.iloc[j]
        stats.iloc[r,0] = float(stats.iloc[r,1]) / (float(stats.iloc[r,1]) + float(stats.iloc[r,9]))

    # Save Statistics to CSV File
    file_postfix = 'CXG_Stats'
    u.to_csv(stats, c.path_dict['strategy'], c.file_dict['strategy_r'] % file_postfix)