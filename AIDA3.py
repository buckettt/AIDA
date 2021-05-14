"""
Reference - Liddament - Guide to Energy Efficient Ventilation
pp. 264

@author: O.Beckett
"""

### AIDA ####

import math as m
import numpy as np
import time

print("Welcome to AIDA")
print("Air Infiltration Development Algorithm")
print("M Liddament - AIVC Guide to Ventilation 1995")

D = 1.26 #density of air

class Opening():

    def __init__(self):
        self.area = 1.0
        self.height = 0.0 #height of centre
        self.cp = 0.0 #wind pressure coefficient
        self.exponent = 0.5 #exponent
        self.C = 0.6*self.area*m.sqrt(2/D)

    @classmethod
    def from_params(cls, area, height, cp, exponent, C=None):
        result = cls()
        result.area = area
        result.height = height
        result.cp = cp
        result.exponent = exponent
        if C:
            result.C = C #pp. 225
        else:
            result.C = result.default_C()
        return result

    def default_C(self):
        return 0.6*self.area*m.sqrt(2./D)

class AIDA():

    def __init__(self):

        self.V = 250. #Building Volume
        self.openings = []

        TotalA = 3.8 #Area of an opening.
        h1 = 1.0

        self.openings.append(Opening.from_params(3.8, 8, 0.0, 0.5))
        self.openings.append(Opening.from_params(3.8, 9, 0.0, 0.5))

        self.external_temp = 24. #External Temp
        self.internal_temp = 27. #Internal Temp
        self.wind_speed  = 0. #Wind Speed

    @property
    def L(self):
        return len(self.openings)

    def add_meshed_opening(self, totalA, num, h1, height):
        self.L += num
        for i in range(num):
            self.H.append(h1 + (i+0.5)*height/num)
            self.P.append(0)
            self.N.append(0.5)
            self.C.append(0.4*totalA*m.sqrt(2./D)/num)


            

    def solve(self):
        L = self.L
        H = np.array([x.height for x in self.openings])
        P = np.array([x.cp for x in self.openings])
        N = np.array([x.exponent for x in self.openings])
        C = np.array([x.C for x in self.openings])

        boolMech = N==0
        E = self.external_temp
        I = self.internal_temp
        U = self.wind_speed

        ###Pressure Calculation###
        W = np.zeros(L)
        S = np.zeros(L)
        T = np.zeros(L)

        W = 0.5*D*U*U*P
        S = -3455*H*((1/(E+273.15))-(1/(I+273.15)))
        T = W + S

        ### Calculate Flows###
        R = -100. #Internal Pressure
        X = 3. #Iteration pressure step
        Y = 0 #Iteration counter
        B = -1

        F = np.zeros(L) #Calculated flow rate

        print(L)
        while((B<=0 or B/np.sum(abs(F))>0.01) and Y<20000):
            Y+=1
            B = 0 #Flow balance

            R = R+X
            T[boolMech] = R
            O = T - R #Pressure difference across each flow path.
            divisor = abs(O)
            numerator = O
            numerator[divisor==0]=1
            divisor[divisor==0]=1
            F = np.nan_to_num(C*abs(O)**N*O/divisor)
            B = np.sum(F)

            if B<0:
                R = R-X
                X = X*0.99
                if Y%100==0: X=100/Y
            else:
                pass

        self.F = F
        self.Q = sum(F)
        self.QT = sum(F[F>0])
        print(T,O,S,R)
        print("Flowrates", F)
        print("Balance",self.Q,"m3/s")
        print("Flow rate",self.QT,"m3/s")

my_case = AIDA()

for i in range(5):
    t = time.time()
    my_case.H = np.array([i,9])
    my_case.solve()
    print("Time taken {0}".format(time.time() - t))