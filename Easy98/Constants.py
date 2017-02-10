# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:35:27 2017

@author: freefrom
"""
# Data Center Root
path_datacenter = '../DataCenter/'

# Data Folders (Relative to Data Center Root)
folder_trading = 'Trading/'
folder_trading_lshq = folder_trading + 'LSHQ/'

folder_reference = 'Reference/'
folder_reference_rzrq = folder_reference + 'RZRQ/'

folder_classifying = 'Classifying/'
folder_classifying_industry     = folder_classifying + 'Industry/'
folder_classifying_concept      = folder_classifying + 'Concept/'
folder_classifying_area         = folder_classifying + 'Area/'
folder_classifying_sme          = folder_classifying + 'SME/'
folder_classifying_gem          = folder_classifying + 'GEM/'
folder_classifying_st           = folder_classifying + 'ST/'
folder_classifying_hs300        = folder_classifying + 'HS300/'
folder_classifying_sz50         = folder_classifying + 'SZ50/'
folder_classifying_zz500        = folder_classifying + 'ZZ500/'
folder_classifying_terminated   = folder_classifying + 'Terminated/'
folder_classifying_suspended    = folder_classifying + 'Suspended/'

folder_fundamental = 'Fundamental/'
folder_fundamental_basics       = folder_fundamental + 'Basics/'
folder_fundamental_report       = folder_fundamental + 'Report/'
folder_fundamental_profit       = folder_fundamental + 'Profit/'
folder_fundamental_operation    = folder_fundamental + 'Operation/'
folder_fundamental_growth       = folder_fundamental + 'Growth/'
folder_fundamental_debtpaying   = folder_fundamental + 'DebtPaying/'
folder_fundamental_cashflow     = folder_fundamental + 'Cashflow/'
folder_fundamental_financesummary = folder_fundamental + 'FinanceSummary/'
folder_fundamental_historicalpe = folder_fundamental + 'HistoricalPE/'

folder_macro = 'Macro/'

folder_newsevent = 'NewsEvent/'

folder_billboard = 'BillBoard/'

folder_shibor = 'Shibor/'

folder_boxoffice = 'BoxOffice/'

# Data Files (Relative to Data Folders)
file_trading_lshq_stock         = 'Trading_LSHQ_Stock_%s.csv'
file_trading_lshq_index         = 'Trading_LSHQ_Index_%s.csv'

file_reference_rzrq_market_sh   = 'Reference_RZRQ_Market_SH.csv'
file_reference_rzrq_market_sz   = 'Reference_RZRQ_Market_SZ.csv'
file_reference_rzrq_stock       = 'Reference_RZRQ_Stock_%s.csv'

file_classifying_industry       = 'Classifying_Industry.csv'
file_classifying_concept        = 'Classifying_Concept.csv'
file_classifying_area           = 'Classifying_Area.csv'
file_classifying_sme            = 'Classifying_SME.csv'
file_classifying_gem            = 'Classifying_GEM.csv'
file_classifying_st             = 'Classifying_ST.csv'
file_classifying_hs300          = 'Classifying_HS300.csv'
file_classifying_sz50           = 'Classifying_SZ50.csv'
file_classifying_zz500          = 'Classifying_ZZ500.csv'
file_classifying_terminated     = 'Classifying_Terminated.csv'
file_classifying_suspended      = 'Classifying_Suspended.csv'

file_fundamental_basics         = 'Fundamental_Basics.csv'
file_fundamental_report_stock   = 'Fundamental_Report_Stock_%s.csv'
file_fundamental_profit_stock   = 'Fundamental_Profit_Stock_%s.csv'
file_fundamental_operation_stock  = 'Fundamental_Operation_Stock_%s.csv'
file_fundamental_growth_stock     = 'Fundamental_Growth_Stock_%s.csv'
file_fundamental_debtpaying_stock = 'Fundamental_DebtPaying_Stock_%s.csv'
file_fundamental_cashflow_stock   = 'Fundamental_Cashflow_Stock_%s.csv'
file_fundamental_financesummary_stock = 'Fundamental_FinanceSummary_Stock_%s.csv'
file_fundamental_historicalpe_stock   = 'Fundamental_HistoricalPE_Stock_%s.csv'

# Convenient Shorts
path_dict = {
        'basics' : path_datacenter + folder_fundamental_basics
        }

file_dict = {
        'basics' : file_fundamental_basics
        }

fullpath_dict = {
        'basics' : path_dict['basics'] + file_dict['basics']
        }

# Magic Numbers
magic_date_YYYYmmdd_str = '1000-00-00'

























