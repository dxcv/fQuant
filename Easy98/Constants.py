# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:35:27 2017

@author: freefrom
"""
# Data Center Root
path_datacenter = '../../../DataCenter/'

# Data Folders (Relative to Data Center Root)
folder_trading = 'Trading/'
folder_trading_lshq = folder_trading + 'LSHQ/'

folder_reference = 'Reference/'
folder_reference_rzrq = folder_reference + 'RZRQ/'

folder_classifying = 'Classifying/'
folder_classifying_industry_sina = folder_classifying + 'Industry_Sina/'
folder_classifying_concept_sina = folder_classifying + 'Concept_Sina/'
folder_classifying_area         = folder_classifying + 'Area/'

folder_fundamental = 'Fundamental/'
folder_fundamental_basics       = folder_fundamental + 'Basics/'
folder_fundamental_report       = folder_fundamental + 'Report/'
folder_fundamental_profit       = folder_fundamental + 'Profit/'
folder_fundamental_operation    = folder_fundamental + 'Operation/'
folder_fundamental_growth       = folder_fundamental + 'Growth/'
folder_fundamental_debtpaying   = folder_fundamental + 'DebtPaying/'
folder_fundamental_cashflow     = folder_fundamental + 'Cashflow/'
folder_fundamental_financesummary = folder_fundamental + 'FinanceSummary/'

folder_macro = 'Macro/'

folder_newsevent = 'NewsEvent/'

folder_billboard = 'BillBoard/'

folder_shibor = 'Shibor/'

folder_boxoffice = 'BoxOffice/'

folder_indicator                = 'Indicator/'
folder_indicator_hpew           = folder_indicator + 'HPEW/'
folder_indicator_hpem           = folder_indicator + 'HPEM/'
folder_indicator_hpeq           = folder_indicator + 'HPEQ/'
folder_indicator_qfqw           = folder_indicator + 'QFQW/'
folder_indicator_qfqm           = folder_indicator + 'QFQM/'
folder_indicator_qfqq           = folder_indicator + 'QFQQ/'

# Data Files (Relative to Data Folders)
file_trading_lshq_stock         = 'Trading_LSHQ_Stock_%s.csv'

file_reference_rzrq_market_sh   = 'Reference_RZRQ_Market_SH.csv'
file_reference_rzrq_market_sz   = 'Reference_RZRQ_Market_SZ.csv'
file_reference_rzrq_stock       = 'Reference_RZRQ_Stock_%s.csv'

file_classifying_industry_sina  = 'Classifying_Industry_Sina.csv'
file_classifying_concept_sina   = 'Classifying_Concept_Sina.csv'
file_classifying_area           = 'Classifying_Area.csv'
file_classifying_sme            = 'Classifying_SME.csv'
file_classifying_gem            = 'Classifying_GEM.csv'
file_classifying_st             = 'Classifying_ST.csv'
file_classifying_hs300          = 'Classifying_HS300.csv'
file_classifying_sz50           = 'Classifying_SZ50.csv'
file_classifying_zz500          = 'Classifying_ZZ500.csv'
file_classifying_terminated     = 'Classifying_Terminated.csv'
file_classifying_suspended      = 'Classifying_Suspended.csv'
file_classifying_industry_list  = 'Classifying_Industry_List.csv'
file_classifying_industry_stock = 'Classifying_Industry_%s.csv'
file_classifying_concept_list   = 'Classifying_Concept_List.csv'
file_classifying_concept_stock  = 'Classifying_Concept_%s.csv'
file_classifying_area_list      = 'Classifying_Area_List.csv'
file_classifying_area_stock     = 'Classifying_Area_%s.csv'

file_fundamental_basics         = 'Fundamental_Basics.csv'
file_fundamental_basics_nottm   = 'Fundamental_Basics_NoTTM.csv'
file_fundamental_report_stock   = 'Fundamental_Report_Stock_%s.csv'
file_fundamental_profit_stock   = 'Fundamental_Profit_Stock_%s.csv'
file_fundamental_operation_stock  = 'Fundamental_Operation_Stock_%s.csv'
file_fundamental_growth_stock     = 'Fundamental_Growth_Stock_%s.csv'
file_fundamental_debtpaying_stock = 'Fundamental_DebtPaying_Stock_%s.csv'
file_fundamental_cashflow_stock   = 'Fundamental_Cashflow_Stock_%s.csv'
file_fundamental_financesummary_stock = 'Fundamental_FinanceSummary_Stock_%s.csv'

file_indicator_hpew_stock       = 'Indicator_HPEW_Stock_%s.csv'
file_indicator_hpem_stock       = 'Indicator_HPEM_Stock_%s.csv'
file_indicator_hpeq_stock       = 'Indicator_HPEQ_Stock_%s.csv'
file_indicator_qfqw_stock       = 'Indicator_QFQW_Stock_%s.csv'
file_indicator_qfqm_stock       = 'Indicator_QFQM_Stock_%s.csv'
file_indicator_qfqq_stock       = 'Indicator_QFQQ_Stock_%s.csv'

# Convenient Shorts
path_dict = {
        'basics' : path_datacenter + folder_fundamental_basics,
        'hpe_w'  : path_datacenter + folder_indicator_hpew,
        'hpe_m'  : path_datacenter + folder_indicator_hpem,
        'hpe_q'  : path_datacenter + folder_indicator_hpeq,
        'qfq_w'  : path_datacenter + folder_indicator_qfqw,
        'qfq_m'  : path_datacenter + folder_indicator_qfqm,
        'qfq_q'  : path_datacenter + folder_indicator_qfqq,
        'lshq'   : path_datacenter + folder_trading_lshq,
        'finsum' : path_datacenter + folder_fundamental_financesummary,
        'classify'  : path_datacenter + folder_classifying,
        'indu_sina' : path_datacenter + folder_classifying_industry_sina,
        'conc_sina' : path_datacenter + folder_classifying_concept_sina,
        'area'      : path_datacenter + folder_classifying_area
        }

file_dict = {
        'basics' : file_fundamental_basics,
        'basics_nottm' : file_fundamental_basics_nottm,
        'hpe_w'  : file_indicator_hpew_stock,
        'hpe_m'  : file_indicator_hpem_stock,
        'hpe_q'  : file_indicator_hpeq_stock,
        'qfq_w'  : file_indicator_qfqw_stock,
        'qfq_m'  : file_indicator_qfqm_stock,
        'qfq_q'  : file_indicator_qfqq_stock,
        'lshq'   : file_trading_lshq_stock,
        'finsum' : file_fundamental_financesummary_stock,
        'indu_sina' : file_classifying_industry_sina,
        'conc_sina' : file_classifying_concept_sina,
        'area'   : file_classifying_area,
        'sme'    : file_classifying_sme,
        'gem'    : file_classifying_gem,
        'st'     : file_classifying_st,
        'hs300'  : file_classifying_hs300,
        'sz50'   : file_classifying_sz50,
        'zz500'  : file_classifying_zz500,
        'terminated' : file_classifying_terminated,
        'suspended'  : file_classifying_suspended,
        'indu_list'  : file_classifying_industry_list,
        'indu_stock' : file_classifying_industry_stock,
        'conc_list'  : file_classifying_concept_list,
        'conc_stock' : file_classifying_concept_stock,
        'area_list'  : file_classifying_area_list,
        'area_stock' : file_classifying_area_stock
        }

fullpath_dict = {
        'basics' : path_dict['basics'] + file_dict['basics'],
        'hpe_w'  : path_dict['hpe_w']  + file_dict['hpe_w'],
        'hpe_m'  : path_dict['hpe_m']  + file_dict['hpe_m'],
        'hpe_q'  : path_dict['hpe_q']  + file_dict['hpe_q'],
        'qfq_w'  : path_dict['qfq_w']  + file_dict['qfq_w'],
        'qfq_m'  : path_dict['qfq_m']  + file_dict['qfq_m'],
        'qfq_q'  : path_dict['qfq_q']  + file_dict['qfq_q'],
        'lshq'   : path_dict['lshq']   + file_dict['lshq'],
        'finsum' : path_dict['finsum'] + file_dict['finsum'],
        'indu_sina' : path_dict['classify'] + file_classifying_industry_sina,
        'conc_sina' : path_dict['classify'] + file_classifying_concept_sina,
        'area'   : path_dict['classify'] + file_classifying_area,
        'sme'    : path_dict['classify'] + file_classifying_sme,
        'gem'    : path_dict['classify'] + file_classifying_gem,
        'st'     : path_dict['classify'] + file_classifying_st,
        'hs300'  : path_dict['classify'] + file_classifying_hs300,
        'sz50'   : path_dict['classify'] + file_classifying_sz50,
        'zz500'  : path_dict['classify'] + file_classifying_zz500,
        'terminated' : path_dict['classify'] + file_classifying_terminated,
        'suspended'  : path_dict['classify'] + file_classifying_suspended,
        'indu_list'  : path_dict['indu_sina'] + file_classifying_industry_list,
        'indu_stock' : path_dict['indu_sina'] + file_classifying_industry_stock,
        'conc_list'  : path_dict['conc_sina'] + file_classifying_concept_list,
        'conc_stock' : path_dict['conc_sina'] + file_classifying_concept_stock,
        'area_list'  : path_dict['area'] + file_classifying_area_list,
        'area_stock' : path_dict['area'] + file_classifying_area_stock
        }

path_map_qfq = {
        'W' : path_dict['qfq_w'],
        'M' : path_dict['qfq_m'],
        'Q' : path_dict['qfq_q']
        }

file_map_qfq = {
        'W' : file_dict['qfq_w'],
        'M' : file_dict['qfq_m'],
        'Q' : file_dict['qfq_q']
        }

fullpath_map_qfq = {
        'W' : fullpath_dict['qfq_w'],
        'M' : fullpath_dict['qfq_m'],
        'Q' : fullpath_dict['qfq_q']
        }

path_map_hpe = {
        'W' : path_dict['hpe_w'],
        'M' : path_dict['hpe_m'],
        'Q' : path_dict['hpe_q']
        }

file_map_hpe = {
        'W' : file_dict['hpe_w'],
        'M' : file_dict['hpe_m'],
        'Q' : file_dict['hpe_q']
        }

fullpath_map_hpe = {
        'W' : fullpath_dict['hpe_w'],
        'M' : fullpath_dict['hpe_m'],
        'Q' : fullpath_dict['hpe_q']
        }

# Magic Numbers
magic_date = '1000-00-00'

























