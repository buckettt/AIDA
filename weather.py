# -*- coding: utf-8 -*-
'''All things relating to weather'''

import pandas as pd
import numpy as np
from constants import BOLTZMANN

EPW_LABELS = ['year', 'month', 'day', 'hour', 'minute', 'datasource', '_ext_temp', 'dewpoint_C', 'relhum_percent',
      'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
      'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux', 'difhorillum_lux',
      'zenlum_lux', 'winddir_deg', '_wind_speed', 'totskycvr_tenths', 'opaqskycvr_tenths', 'visibility_km',
      'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
      'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']

###Types###
EPW_DATA = 1
DESIGN_CONDITION = 2

class Weather():
    '''weather conditions'''

    def __init__(self):
        self.type = DESIGN_CONDITION
        self.wind_speed = 3
        self.ext_temp = 5
        self.int_temp = 18
        self.epw_data = None
        self.current_hour = 0
        
    #Generic setter and getter for counters.
    def setter(var):
        def set(self, value):
            if self.type is DESIGN_CONDITION:
                setattr(self, var, value)
            else:
                pass
        return set

    def getter(var):
        def get(self):
            if self.type is DESIGN_CONDITION:
                return getattr(self, var)
            elif self.type is EPW_DATA:
                return self.epw_data[var][self.current_hour]
        return get

    ext_temp = property(getter('_ext_temp'), setter('_ext_temp'))
    wind_speed = property(getter('_wind_speed'), setter('_wind_speed'))

        
    def load_epw(self, epw_file):
        result = pd.read_csv(epw_file, skiprows=8, header=None, names=EPW_LABELS).drop('datasource', axis=1)
        result['dayofyear'] = pd.date_range('1/1/2016', periods=8760, freq='H').dayofyear
        result['ratio_diffhout'] = result['difhorrad_Whm2'] / result['glohorrad_Whm2']
        result['skycover'] = result['ratio_diffhout'].fillna(1)
        result['skytemp_C'] = np.vectorize(calc_skytemp)(result['_ext_temp'], result['dewpoint_C'], result['skycover'])
        self.epw_data = result.to_dict()
        self.type = EPW_DATA
    
    def hour(self, h):
        index = h%self.num_hours
        if self.type is DESIGN_CONDITION:
            return 1
        elif self.type is EPW_DATA:
            return self.epw_data.iloc[index]
        
    
    @property
    def num_hours(self):
        if self.type is DESIGN_CONDITION:
            return 1
        elif self.type is EPW_DATA:
            return len(self.epw_data['year'])

def calc_skytemp(Tdrybulb, Tdewpoint, N):
    '''
    __author__ = "Clayton Miller"
    __copyright__ = "Copyright 2014, Architecture and Building Systems - ETH Zurich"
    __credits__ = ["Clayton Miller", "Jimeno A. Fonseca"]
    __license__ = "MIT"
    __version__ = "0.1"
    __maintainer__ = "Daren Thomas"
    __email__ = "cea@arch.ethz.ch"
    __status__ = "Production"
    '''

    sky_e = (0.787 + 0.764 * ((Tdewpoint + 273) / 273)) * 1 + 0.0224 * N + 0.0035 * N ** 2 + 0.00025 * N ** 3
    hor_IR = sky_e * BOLTZMANN * (Tdrybulb + 273) ** 4
    sky_T = ((hor_IR / BOLTZMANN) ** 0.25) - 273

    return sky_T  # sky temperature in C