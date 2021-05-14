# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 15:46:10 2018

@author: O.Beckett
"""

import numpy as np
from numpy import array
from termite_object import TermObject
from weather import Weather
from room import Room
from natvent_python import solve_airflow, wind_pressure, buoy_pressure, resid_calc, mech_pressures, internal_driving, flows, driving_press
from heat import temp_from_gain
from constants import *
from surface import connection_matrix

class Building(TermObject):
    '''building'''

    def __init__(self):
        super(Building, self).__init__()
        self.connections = None
        self.flow = None
        self.surfaces = []
        self.openings = []
        self.rooms = []

    #Generic setter and getter for attributes of the list of rooms.
    def room_setter(var):
        def set(self, value):
            for i, v in enumerate(value):
                setattr(self.rooms[i], var, v)
        return set

    def room_getter(var):
        def get(self):
            return array([getattr(r, var) for r in self.rooms])
        return get

    room_temps = property(room_getter('temp'), room_setter('temp'), None, "Room Temperatures")
    room_gains = property(room_getter('gains'), room_setter('gains'), None, "Room Temperatures")
    room_press = property(room_getter('pressure'), room_setter('pressure'), None, 'Room Pressures')
    room_com = property(room_getter('centre_of_mass'), room_setter('centre_of_mass'), None, 'Room Pressures')

    #Generic setter and getter for counters.
    def counter_setter(var):
        def set(self, value):
            setattr(self, var, value)
        return set

    def counter_getter(var):
        def get(self):
            return len(getattr(self, var))
        return get

    num_openings = property(counter_getter('openings'), None)
    num_zones = property(counter_getter('rooms'), None)

    #Generic setter and getter for attributes of the list of openings.
    def opening_setter(var):
        def set(self, value):
            for i, v in enumerate(value):
                setattr(self.openings[i], var, v)
        return set

    def opening_getter(var):
        def get(self):
            #return array([getattr(o, var) for o in self.openings])
            if var not in self.openings[0].__dict__.keys():
                return array([getattr(o, var) for o in self.openings])
            else: 
                return array([o.__dict__.get(var) for o in self.openings])

        return get

    wind_coeff = property(opening_getter('wind_coeff'), opening_setter('wind_coeff'), None)
    height = property(opening_getter('height'), opening_setter('height'), None)
    exponent = property(opening_getter('exponent'), opening_setter('exponent'), None)
    flow_coeff = property(opening_getter('flow_coeff'), opening_setter('flow_coeff'), None)
    flow_rate = property(opening_getter('flow_rate'), opening_setter('flow_rate'), None)
    bool_internal = property(opening_getter('bool_internal'), opening_setter('bool_internal'), None)
    bool_mech = property(opening_getter('bool_mech'), opening_setter('bool_mech'), None)
    opening_temps = property(opening_getter('opening_temps'), opening_setter('opening_temps'), None)

    #Generic setter and getter for attributes of the list of openings.
    def surface_setter(var):
        def set(self, value):
            for i, v in enumerate(value):
                setattr(self.surfaces[i], var, v)
        return set

    def surface_getter(var):
        def get(self):
            return array([getattr(r, var) for r in self.surfaces])
        return get

    surface_areas = property(opening_getter('area'), None, None)

    def solve(self, weather, analysis_settings, print_message=True, temp_type=DEFAULT):
        for h in range(weather.num_hours):
            print("Hour: ", h)
            weather.current_hour = h #Update the hour we are looking at.
            solve_airflow(self, weather, analysis_settings, print_message, temp_type)
        return self



