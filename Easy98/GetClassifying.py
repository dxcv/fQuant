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
import GlobalSettings as gs
import Constants as c
import Utilities as u


def getIndustrySina():
    # Download Sina Industry Data
    industry = get_industry_sina()
    if gs.is_debug:
        print(industry.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(industry):
        u.to_csv(industry, c.path_dict['classify'], c.file_dict['indu_sina'])

def loadIndustrySina():
    industry = u.read_csv(c.fullpath_dict['indu_sina'])
    return industry

def getConceptSina():
    # Download Sina Concept Data
    concept = get_concept_sina()
    if gs.is_debug:
        print(concept.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(concept):
        u.to_csv(concept, c.path_dict['classify'], c.file_dict['conc_sina'])

def loadConceptSina():
    concept = u.read_csv(c.fullpath_dict['conc_sina'])
    return concept

def getArea():
    # Download Area Data
    area = get_area()
    if gs.is_debug:
        print(area.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(area):
        u.to_csv(area, c.path_dict['classify'], c.file_dict['area'])

def loadArea():
    area = u.read_csv(c.fullpath_dict['area'])
    return area

###############################################################################

def getSME():
    # Download SME Data
    sme = get_sme()
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
    if gs.is_debug:
        print(suspended.head(10))

    # Save to CSV File
    if not u.isNoneOrEmpty(suspended):
        u.to_csv(suspended, c.path_dict['classify'], c.file_dict['suspended'])

def loadSuspended():
    suspended = u.read_csv(c.fullpath_dict['suspended'])
    return suspended