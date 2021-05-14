# -*- coding: utf-8 -*-

from termite_object import TermObject
import numpy as np
from constants import *

class Gain(TermObject):
    '''internal heat gain'''
    ''' Units:
        0 - W/m2
        1 - W
        2 - W/K (Function of room temperature)
        '''
    def __init__(self):
        super(Gain, self).__init__()
        self.units = WATTSPERM2
        self.value = 0
        self.profile = None
        
    def value_at_time(self, hour):
        return self.value

class RoomType(TermObject):
    ''' template for a room'''
    
    def __init__(self):
        super(RoomType, self).__init__()

class Room(TermObject):
    ''' Room '''

    def __init__(self):
        super(Room, self).__init__()
        self.surfaces = []
        self.gains = []
        self.my_room_type = None
        self.temp = 0.
        self.pressure = 0.

    @property
    def centre_of_mass(self):
        '''return the average centroid of all surfaces'''
        surfaces_coms = np.array([x.centre_of_mass() for x in self.surfaces])
        return np.mean(surfaces_coms, 0)


class Outside(Room):
    '''Outside is a special type of room.'''

    def __init__(self):
        super(Outside, self).__init__()
        self.exists = True
        

class Adjacency(TermObject):
    '''
    connection between two rooms via a surface


    Connection types: Room1 to Room2 - normal
                      Room1 to Room1 - adiabatic
                      Room1 to Outside
                      Room1 to Ground
                      Room1 to Profiles/Condition
    '''

    def __init__(self):
        super(Adjacency, self).__init__()
        self.zones = []
        self.surface = None
