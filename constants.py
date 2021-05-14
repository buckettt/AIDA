# -*- coding: utf-8 -*-

###Physical Constants###
ABS_ZERO = -273.15 #degC
PATMOS = 101.325
RHO = 1.2 #density of air
CP = 1005 #heat capacity of air.
BOLTZMANN= 1.3807 * 10**-23

###CONFIG###
PICKLE_FOLDER = "pkl\\"

###TYPES AND DESCRIPTORS###
DEFAULT = 0
#SETPOINT TYPE
FIXTEMP = 1 #SETPOINT
FIXHEAT = 2 #FREE RUNNING

###Heat Gain Types###
WATTSPERM2 = 0
WATTS = 1
WATTSPERK = 2