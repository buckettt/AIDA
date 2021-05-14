# -*- coding: utf-8 -*-

import numpy as np

def temp_from_gain(heat_gain, vdot, tin, rho=1.2, c_p=1005):
    ''' calculate simple heat balance returns temperature'''
    #Q = mdot.Cp.delT
    tin_average = vdot*tin/np.sum(vdot)
    return tin_average + heat_gain/(rho*c_p*vdot)