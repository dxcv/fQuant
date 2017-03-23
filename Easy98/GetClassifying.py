# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:48:46 2017

@author: freefrom
"""

#
# Import Libraries and Methods
#

from Classifying import get_industry_sina, get_concept_sina, get_area
from Classifying import get_sme, get_gem, get_st
from Classifying import get_hs300, get_sz50, get_zz500
from Classifying import get_terminated, get_suspended
from Classifying import get_cxg
import GlobalSettings as gs
import Constants as c
import Utilities as u


def getIndustrySina():
    # Download Sina Industry Data
    industry = get_industry_sina()
    industry.set_index('code', inplace=True)
    if gs.is_debug:
        print(industry.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(industry):
        u.to_csv(industry, c.path_dict['classify'], c.file_dict['indu_sina'])

def loadIndustrySina():
    industry = u.read_csv(c.fullpath_dict['indu_sina'])
    return industry

def extractIndustrySina():
    # Load Sina Industry Data
    industry_sina = loadIndustrySina()
    if gs.is_debug:
        print(industry_sina.head(10))

    # Extract Industry List
    industry_list = industry_sina.drop(['code', 'name'], axis=1)
    industry_list.drop_duplicates(['industry'], inplace=True)
    industry_list.set_index('industry', inplace=True)
    if gs.is_debug:
        print(industry_list.index)

    # Save to CSV File
    if not u.isNoneOrEmpty(industry_list):
        u.to_csv(industry_list, c.path_dict['indu_sina'], c.file_dict['indu_list'])

    # Extract Stocks for Each Industry
    industry_number = len(industry_list)
    print('#Industry =', industry_number)
    for i in range(industry_number):
        industry_name = industry_list.index[i]
        industry_stock = industry_sina[industry_sina.industry.isin([industry_name])]
        industry_stock['code'] = industry_stock['code'].map(lambda x:str(x).zfill(6))
        industry_stock.set_index('code', inplace=True)
        if gs.is_debug:
            print(industry_stock.head(10))

        # Save to CSV File
        if not u.isNoneOrEmpty(industry_stock):
            u.to_csv(industry_stock, c.path_dict['indu_sina'], c.file_dict['indu_stock'] % industry_name)

def getConceptSina():
    # Download Sina Concept Data
    concept = get_concept_sina()
    concept.set_index('code', inplace=True)
    if gs.is_debug:
        print(concept.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(concept):
        u.to_csv(concept, c.path_dict['classify'], c.file_dict['conc_sina'])

def loadConceptSina():
    concept = u.read_csv(c.fullpath_dict['conc_sina'])
    return concept

def extractConceptSina():
    # Load Sina Concept Data
    concept_sina = loadConceptSina()
    if gs.is_debug:
        print(concept_sina.head(10))

    # Extract Concept List
    concept_list = concept_sina.drop(['code', 'name'], axis=1)
    concept_list.drop_duplicates(['concept'], inplace=True)
    concept_list.set_index('concept', inplace=True)
    if gs.is_debug:
        print(concept_list.index)

    # Save to CSV File
    if not u.isNoneOrEmpty(concept_list):
        u.to_csv(concept_list, c.path_dict['conc_sina'], c.file_dict['conc_list'])

    # Extract Stocks for Each Concept
    concept_number = len(concept_list)
    print('#Concept =', concept_number)
    for i in range(concept_number):
        concept_name = concept_list.index[i]
        concept_stock = concept_sina[concept_sina.concept.isin([concept_name])]
        concept_stock['code'] = concept_stock['code'].map(lambda x:str(x).zfill(6))
        concept_stock.set_index('code', inplace=True)
        if gs.is_debug:
            print(concept_stock.head(10))

        # Save to CSV File
        if not u.isNoneOrEmpty(concept_stock):
            u.to_csv(concept_stock, c.path_dict['conc_sina'], c.file_dict['conc_stock'] % concept_name)

def getArea():
    # Download Area Data
    area = get_area()
    area.set_index('code', inplace=True)
    if gs.is_debug:
        print(area.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(area):
        u.to_csv(area, c.path_dict['classify'], c.file_dict['area'])

def loadArea():
    area = u.read_csv(c.fullpath_dict['area'])
    return area

def extractArea():
    # Load Area Data
    area = loadArea()
    if gs.is_debug:
        print(area.head(10))

    # Extract Area List
    area_list = area.drop(['code', 'name'], axis=1)
    area_list.drop_duplicates(['area'], inplace=True)
    area_list.set_index('area', inplace=True)
    if gs.is_debug:
        print(area_list.index)

    # Save to CSV File
    if not u.isNoneOrEmpty(area_list):
        u.to_csv(area_list, c.path_dict['area'], c.file_dict['area_list'])

    # Extract Stocks for Each Area
    area_number = len(area_list)
    print('#Area =', area_number)
    for i in range(area_number):
        area_name = area_list.index[i]
        area_stock = area[area.area.isin([area_name])]
        area_stock['code'] = area_stock['code'].map(lambda x:str(x).zfill(6))
        area_stock.set_index('code', inplace=True)
        if gs.is_debug:
            print(area_stock.head(10))

        # Save to CSV File
        if not u.isNoneOrEmpty(area_stock):
            u.to_csv(area_stock, c.path_dict['area'], c.file_dict['area_stock'] % area_name)

###############################################################################

def getSME():
    # Download SME Data
    sme = get_sme()
    sme.set_index('code', inplace=True)
    if gs.is_debug:
        print(sme.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(sme):
        u.to_csv(sme, c.path_dict['classify'], c.file_dict['sme'])

def loadSME():
    sme = u.read_csv(c.fullpath_dict['sme'])
    return sme

def getGEM():
    # Download GEM Data
    gem = get_gem()
    gem.set_index('code', inplace=True)
    if gs.is_debug:
        print(gem.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(gem):
        u.to_csv(gem, c.path_dict['classify'], c.file_dict['gem'])

def loadGEM():
    gem = u.read_csv(c.fullpath_dict['gem'])
    return gem

def getST():
    # Download ST Data
    st = get_st()
    st.set_index('code', inplace=True)
    if gs.is_debug:
        print(st.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(st):
        u.to_csv(st, c.path_dict['classify'], c.file_dict['st'])

def loadST():
    st = u.read_csv(c.fullpath_dict['st'])
    return st

###############################################################################

def getHS300():
    # Download HS300 Data
    hs300 = get_hs300()
    hs300.set_index('code', inplace=True)
    if gs.is_debug:
        print(hs300.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(hs300):
        u.to_csv(hs300, c.path_dict['classify'], c.file_dict['hs300'])

def loadHS300():
    hs300 = u.read_csv(c.fullpath_dict['hs300'])
    return hs300

def getSZ50():
    # Download SZ50 Data
    sz50 = get_sz50()
    sz50.set_index('code', inplace=True)
    if gs.is_debug:
        print(sz50.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(sz50):
        u.to_csv(sz50, c.path_dict['classify'], c.file_dict['sz50'])

def loadSZ50():
    sz50 = u.read_csv(c.fullpath_dict['sz50'])
    return sz50

def getZZ500():
    # Download ZZ500 Data
    zz500 = get_zz500()
    zz500.set_index('code', inplace=True)
    if gs.is_debug:
        print(zz500.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(zz500):
        u.to_csv(zz500, c.path_dict['classify'], c.file_dict['zz500'])

def loadZZ500():
    zz500 = u.read_csv(c.fullpath_dict['zz500'])
    return zz500

###############################################################################

def getTerminated():
    # Download Terminated Stock Data
    terminated = get_terminated()
    terminated.set_index('code', inplace=True)
    if gs.is_debug:
        print(terminated.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(terminated):
        u.to_csv(terminated, c.path_dict['classify'], c.file_dict['terminated'])

def loadTerminated():
    terminated = u.read_csv(c.fullpath_dict['terminated'])
    return terminated

def getSuspended():
    # Download Suspended Data
    suspended = get_suspended()
    suspended.set_index('code', inplace=True)
    if gs.is_debug:
        print(suspended.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(suspended):
        u.to_csv(suspended, c.path_dict['classify'], c.file_dict['suspended'])

def loadSuspended():
    suspended = u.read_csv(c.fullpath_dict['suspended'])
    return suspended

###############################################################################

def getCXG(date):
    # Get CXG Stock Data
    cxg = get_cxg(date)
    cxg['code'] = cxg['code'].map(lambda x:str(x).zfill(6))
    cxg.set_index('code', inplace=True)
    if gs.is_debug:
        print(cxg.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(cxg):
        u.to_csv(cxg, c.path_dict['classify'], c.file_dict['cxg'])