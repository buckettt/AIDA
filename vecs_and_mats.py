# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 17:26:31 2018

@author: o.beckett
"""

import numpy as np

def skew_sym_cross_product(v):
    ''' skew symmetric cross product matrix for a 3dim vector'''
    return np.matrix([[0, -v[2], v[1]],
                      [v[2], 0, -v[0]],
                      [-v[1], v[0], 0]])