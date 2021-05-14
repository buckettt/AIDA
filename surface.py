
import numpy as np
import math as m
import vecs_and_mats as vam
from termite_object import TermObject

class Surface(TermObject):
    '''Surface'''

    def __init__(self):
        super(Surface, self).__init__()
        self.nodes = np.array([])
        self.local_nodes = np.array([])
        self.wind_coeff = 0.

    def update_local_nodes(self):
        '''updates nodes to local coords centre on origin and aligned with xaxis'''
        if len(self.nodes) < 2:
            return False
        translation = -self.nodes[0] #move first node to origin

        vec_a = self.nodes[1] - self.nodes[0]
        vec_b = np.array([1, 0, 0]) #translate onto x direction.

        vec_v = np.cross(vec_a, vec_b)
        cos = np.dot(vec_a, vec_b) #cosine of angle

        v_sscp = vam.skew_sym_cross_product(vec_v)

        rot = np.identity(3) + v_sscp + ((v_sscp*v_sscp) * 1/(1+cos))

        self.local_nodes = [] #rest
        for node  in self.nodes:
            self.local_nodes.append(np.dot(rot, np.transpose((node+translation))))
        self.local_nodes = np.array(self.local_nodes)

        return True

    @property
    def bool_planar(self):
        ''' check that a surface is planar'''
        if not self.update_local_nodes():
            return False

        for node in self.local_nodes:
            if node[2] > 0.0000001: #when doing the translation there shouldnt be any z coords.
                return False

        return True

    @property
    def area(self):
        '''https://www.mathopenref.com/coordpolygonarea2.html'''
        area = 0

        if not self.update_local_nodes():
            return -1
        if not self.bool_planar:
            return -1

        for i, _n in enumerate(self.local_nodes):
            ii = i
            jj = (i+1)%(len(self.local_nodes))
            area += (self.local_nodes[jj][0] + self.local_nodes[ii][0]) \
                 *(self.local_nodes[jj][1] - self.local_nodes[ii][1])
        area = area/2.
        return area

    @property
    def centre_of_mass(self):
        '''centre of mass of surface'''
        return np.mean(self.nodes, 0)

EXTERNALOPENING = 0
INTERNALOPENING = 1
MECHINLET = 2
MECHEXTRACT = 3
    
class Opening(Surface):
    '''Opening'''
    
    def __init__(self, openingtype=EXTERNALOPENING, zone1=None, zone2 =None):
        super(Opening, self).__init__()
        self.height = 0
        self.openingtype = openingtype
        self.zones = [zone1, zone2]
        self.flow_rate = 0
        self.exponent = 0.5
        self.temp = 20.
        
    @property
    def bool_internal(self):
        return self.openingtype == INTERNALOPENING

    @property
    def bool_mech(self):
        return self.openingtype == MECHEXTRACT or self.openingtype == MECHINLET
        
    def opening_temps(self):
        if self.openingtype == EXTERNALOPENING: return None
        if self.openingtype == INTERNALOPENING:
            if self.flow_rate>0:
                return self.zone1.temp
            else:
                return self.zone2.temp
        else: return self.temp
    
def connection_matrix(building):
    '''construct the connection matrix of openings in building'''
    result = np.zeros([building.num_zones, building.num_openings])
    for i, r in enumerate(building.rooms):
        row = []
        for j, o in enumerate(building.openings):
            row.append(int(r in o.zones))
        result[i] = np.array(row)
    if building.num_zones == 1: return result[0]
    return result
    
def c_from_area(area, rho, c_d=0.6):
    ''' flow coefficient from area and Cd'''
    return c_d*area*m.sqrt(2./rho)

