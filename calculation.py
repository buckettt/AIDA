# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:49:51 2018

Reference - Liddament - Guide to Energy Efficient Ventilation
pp. 264

@author: O.Beckett
"""

### AIDA ####
import numpy as np
from building import Building, DEFAULT, FIXTEMP, FIXHEAT
from surface import Opening
from weather import Weather
from room import Room
from constants import *
from analysis_settings import AnalysisSettings
import math as m

#HOUSEKEEPING
np.set_printoptions(precision=4)

def main():
    '''main'''

    print("Welcome to AIDA")
    print("Air Infiltration Development Algorithm")
    print("M Liddament - AIVC Guide to Ventilation 1995")
    print("Extended to multizone - O Beckett 2018")

    analysis_settings = AnalysisSettings()
    test_case_mz = Building()
    for i in range(8):
        test_case_mz.rooms.append(Room())
    
    test_case_mz.openings.append(Opening(openingtype=0, zone1=test_case_mz.rooms[0]))
    test_case_mz.openings.append(Opening(openingtype=0, zone1=test_case_mz.rooms[1]))
    test_case_mz.openings.append(Opening(openingtype=0, zone1=test_case_mz.rooms[2]))
    test_case_mz.openings.append(Opening(openingtype=0, zone1=test_case_mz.rooms[3]))
    test_case_mz.openings.append(Opening(openingtype=0, zone1=test_case_mz.rooms[3]))
    test_case_mz.openings.append(Opening(openingtype=1, zone1=test_case_mz.rooms[0], zone2=test_case_mz.rooms[1]))
    test_case_mz.openings.append(Opening(openingtype=1, zone1=test_case_mz.rooms[1], zone2=test_case_mz.rooms[2]))
    test_case_mz.openings.append(Opening(openingtype=1, zone1=test_case_mz.rooms[2], zone2=test_case_mz.rooms[3]))


    test_case_mz.height = np.array( [1.2, 3.6, 6.0, 8.4, 12, 2.4, 4.8, 7.2]) #Height of opening
    test_case_mz.wind_coeff = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) #Wind Pressure Coefficient
    test_case_mz.internal_gains = np.array([17000.0, 11000.0, 16000.0, 20000.0, 0.0, 0.0, 0.0, 0.0]) #Internal Gains
    #test_case_mz.exponent = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) #Exponent
    #C = num_openings*[0.6*1*m.sqrt(2./rho)] #pp. 225
    openingCdA = 0.6*np.array([30.0, 0.0, 20.0, 22.0, 35.0, 40.0, 40.0, 40.0])
    C = openingCdA*m.sqrt(2./1.2)
    test_case_mz.flow_coeff = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])
    test_case_mz.flow_coeff = C
    #Flow coefficienct #can add mechanical here.

    #LIDDAMENT TEST CASES. pp. 266
    
    test_case = Building()

    test_case.rooms = [Room()]
    for i in range(3):
        test_case.openings.append(Opening(zone1=test_case.rooms[0]))

   
    print(test_case.num_openings)
    test_case.height = np.array([2., 4., 7.])
    test_case.wind_coeff = np.array([0.3, -0.25, -0.4])
    test_case.exponent = np.array([0.7, 0.5, 0.6])
    test_case.flow_coeff = np.array([0.03, 0.06, 0.02])

    weather1 = Weather()
    weather1.ext_temp = 0
    weather1.int_temp = 20
    weather1.wind_speed = 0
    
    weather2 = Weather()
    weather2.ext_temp = 20
    weather2.int_temp = 22
    weather2.wind_speed = 0
    
    test_case.room_temps = np.array([15.])
    test_case.room_heat = 599.382 #Watts

    weather3 = Weather()
    weather3.ext_temp = 18
    weather3.int_temp = 17
    weather3.wind_speed = 3
    
    weather2.load_epw(r".\GBR_London.epw")
    weather2.type = 2
    #test_case.solve(weather1, PERCERROR, print_message=False)
    #test_case.solve(weather2, PERCERROR, print_message=False)
    #test_case.solve(weather2, analysis_settings, print_message=True, temp_type=DEFAULT)
    #test_case.solve(weather2, PERCERROR, print_message=True, temp_type=FIXTEMP)
    #test_case.solve(weather2, PERCERROR, print_message=True, temp_type=FIXHEAT)

    #test_case_mz.solve(weather1, PERCERROR)
    #test_case_mz.solve(weather2, PERCERROR)
    test_case_mz.solve(weather2, analysis_settings, print_message=True, temp_type=FIXHEAT)

    return test_case
    #return test_case.solve(weather3, PERCERROR, print_message=False)

if __name__ == "__main__":
    tc = main()
