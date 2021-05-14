# -*- coding: utf-8 -*-

from termite_object import TermObject
import numpy as np

class Profile(TermObject):
    
    def __init__(self):
        super(Profile, self).__init__()
        self.reset_values()
        self.backup()
        
    def reset_values(self, day=None):
        if day is None:
            self.values = np.full([7,24], None)
        else:
            self.values[day,:] = None
    
    def get_value(self, day, hour):
        #print(hour, day)
        if self.values[day, hour] is None:
            return self.get_value(day, hour-1)
        return self.values[day, hour]
    
    def set_always_on(self, day=None):
        self.set_always_value(1, day)        
        
    def set_always_off(self, day=None):
        self.set_always_value(0, day)
        
    def set_always_value(self, val, day=None):
        self.reset_values(day=day)
        if day is None:
            self.values[:, 0] = val
            self.values[:, -1] = val
        else:
            self.values[day,0] = val
            self.values[day,-1] = val   
            
    def set_increasing(self):
        self.reset_values()
        for i in range(0,24):
            self.values[:, i] = float(i/(24))
        
    def set_nine_to_five(self, day=None):
        self.set_always_off(day)
        
        if day is None:
            self.values[:, 9] = 1
            self.values[:, 18] = 0
        else:
            self.values[day, 9] = 1
            self.values[day, 18] = 0
        
    def copy(self, day_from, day_to):
        self.values[day_to, :] = self.values[day_from, :]
        
    def restore(self):
        if self.values_backup is None:
            print("no backup")
        else:
            self.values = self.values_backup
            self.values_backup = None
        
    def backup(self):
        self.values_backup = self.values