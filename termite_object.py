# -*- coding: utf-8 -*-

'''termite_object.py'''

from uuid import uuid4
import pickle
import os
import glob
from constants import PICKLE_FOLDER


class TermObject():
    '''Generic Object for Termites.
    Contains generic functions'''

    def __init__(self):
        self.uuid = uuid4()
        self.name = "test"

    def backup_filename(self):
        '''returns a backup filename at a given point'''
        return  PICKLE_FOLDER + "BACKUP" + str(self.uuid) + ".pkl"

    def backup(self):
        '''saves a backup of the object - useful when hitting cancel or reverting.'''
        pickle.dump(self, open(self.backup_filename(), "wb"))
        return True
    
    def restore(self):
        '''restore the object from the backup file'''
        if os.path.exists(self.backup_filename):
            unpickled = pickle.load(open(self.backup_filename(), "rb"))
            os.remove(self.backup_filename())
            return unpickled
        return self

    def new_pickle_filename(self):
        '''returns a new unique pickling filename'''
        number = 0
        filename = PICKLE_FOLDER + str(self.uuid)+ "_" + "{:05d}".format(number) + ".pkl"
        while os.path.isfile(filename):
            number += 1
            filename = PICKLE_FOLDER + str(self.uuid)+ "_" + "{:05d}".format(number) +".pkl"
        return filename

    def get_latest_pickle_filename(self):
        '''returns the latest pickled filename'''
        fnames = glob.glob(PICKLE_FOLDER + str(self.uuid) + "*")
        if fnames:
            return fnames[-1]
        return False

    def pickle_me(self):
        '''save a temp file of the object - useful for undos and redos.'''
        pickle.dump(self, open(self.new_pickle_filename(), "wb"))
        return True

    def clear_pickle(self):
        '''clear the objects pickled files'''
        while self.get_latest_pickle_filename():
            os.remove(self.get_latest_pickle_filename())
        return True

    def unpickle_me(self):
        ''' restore the pickled file'''
        if self.get_latest_pickle_filename():
            unpickled = pickle.load(open(self.get_latest_pickle_filename(), "rb"))
            os.remove(self.get_latest_pickle_filename())
            return unpickled
            ## Show an error ##
        print("Error: %s file not found" % self.get_latest_pickle_filename())
        return self
