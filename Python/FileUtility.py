# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:42:57 2017

@author: freefrom
"""

import os

def hasFile(path, file):
    return os.path.isfile(path+file)