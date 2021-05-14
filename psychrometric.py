# -*- coding: utf-8 -*-
''' Useful psychrometric functions. Mostly taken from CIBSE Guide A/C '''


from constants import ABS_ZERO, PATMOS
from math import log10, log

'''
press = pressure
sat = saturation
vap = vapour
'''

def kelvin(celsius):
    return celsius - ABS_ZERO

def dry_air_density(temperature, g):
    R_da = 287.055
    result = 1000*PATMOS/(R_da*(kelvin(temperature))*(1 + 1.6078*g))
    return result

def sat_vap_press(temperature):
    '''Saturation vapour presure. CIBSE Guide C eq 1.3'''
    temp = kelvin(temperature)
    log10_ps = 30.59051 - 8.2*log10(temp) + \
                2.4804*temp*0.001 - (3142.31/temp)
                
    ps = 10**log10_ps
    return ps

def humidity_saturation(temperature, g):
    return 100*g/sat_moisture_content(temperature)

def sat_moisture_content(temperature):
    '''CIBSE Guide C eq 1.5'''
    p_s = sat_vap_press(temperature)
    fs = 1.0 #TODO
    g_s = (0.62197*fs*p_s)/(101.325-fs*p_s)    
    return g_s

def moisture_content(temperature, RH):
    p_s = sat_vap_press(temperature)
    fs = 1.0 #TODO
    g = (0.62197*RH*fs*p_s)/(101.325-RH*fs*p_s)  
    return g

def moisture_content2(temperature, wetbulb):
    g_s = sat_moisture_content(temperature)
    if temperature>=0:
        g = (((2501 - 2.326*wetbulb)*g_s - 1.006*(temperature - wetbulb))/
                  (2501 + 1.86*temperature - 4.186*wetbulb))
    else:
        g = (((2830 - 0.24*wetbulb)*g_s - 1.006*(temperature - wetbulb))/
                  (2830 + 1.86*temperature - 2.1*wetbulb))        
    return g

def perc_saturation(g, temperature):
    '''CIBSE Guide C eq 1.6'''
    return 100*g/sat_moisture_content(temperature)

def vap_press(g):
    '''CIBSE Guide C eq 1.7'''
    f_s = 1
    p_v = PATMOS*g / (f_s*0.62197 + g)
    return p_v

def relative_humidity(temperature, g):
    '''CIBSE Guide C eq 1.8'''
    return 100*vap_press(g)/sat_vap_press(temperature)


def relative_humidity2(temperature, wetbulb):
    g = moisture_content2(temperature, wetbulb)
    return relative_humidity(g)

def dew_point(g):
    C14 = 6.54
    C15 = 14.526
    C16 = 0.7389
    C17 = 0.09486
    C18 = 0.4569
    
    Pw = vap_press(g)
    alpha = log(Pw)
    Tdp1 = C14 + C15*alpha + C16*alpha**2 + C17*alpha**3 + C18*Pw**0.1984
    Tdp2 = 6.09 + 12.608*alpha + 0.4959*alpha**2
    if Tdp1 >= 0:
        result = Tdp1
    else:
        result = Tdp2
    return result
    

def wet_bulb(temperature, RH, ambient_pressure):
    
    ''' Calculates the Wet Bulb temp given:        
            Tdb = Dry bulb temperature [degC]
            RH = Relative humidity ratio [Fraction or %]
            P = Ambient Pressure [kPa]
        Uses Newton-Rhapson iteration to converge quickly
    '''

    W_normal = moisture_content(temperature, RH)
    wetbulb = temperature
    
    ' Solves to within 0.001% accuracy using Newton-Rhapson'    
    W_new = moisture_content2(temperature, wetbulb)
    while abs((W_new - W_normal) / W_normal) > 0.00001:
        W_new2 = moisture_content2(temperature, wetbulb - 0.001)
        dw_dtwb = (W_new - W_new2) / 0.001
        wetbulb = wetbulb - (W_new - W_normal) / dw_dtwb
        W_new = moisture_content2(temperature, wetbulb)
    return wetbulb