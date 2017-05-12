# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:47:47 2017

@author: freefrom
"""

from Index.GenerateIndex import generateIndexFeiYan
from Plot.PlotFigures import plotIndex

#
# All-in-one entry for daily report of FeiYan Index Series
#

#index_names = ['FeiYan_NewEnergyVehicle', 'FeiYan_NewMaterial', 'FeiYan_BatteryMaterial', 'FeiYan_RareMaterial', 'FeiYan_AI']

index_names = ['FeiYan_NewEnergyVehicle', 'FeiYan_BatteryMaterial', 'FeiYan_FY50', 'FeiYan_FY20']
generateIndexFeiYan(index_names)
plotIndex(index_names)

#
# Test for single functionality
#
