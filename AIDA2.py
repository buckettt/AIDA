"""
Reference - Liddament - Guide to Energy Efficient Ventilation
pp. 264

@author: O.Beckett
"""

### AIDA ####

import math as m
import numpy as np

print("Welcome to AIDA")
print("Air Infiltration Development Algorithm")
print("M Liddament - AIVC Guide to Ventilation 1995")

D = 1.26 #density of air
V = 250. #Building Volume
L =2 #Number of flow paths

TotalA = 3.8 #Area of an opening.
h1 = 1.0
#H = L*[0]

#H = []
#for i in range(L):
#    H.append(h1 + (i+0.5)*TotalA/L)

H = np.array([8,9]) #Height of opening
P = np.array(L*[0.0]) #Wind Pressure Coefficient
N = np.array(L*[0.5]) #Exponent
C = L*[0.4*TotalA*m.sqrt(2./D)] #pp. 225
#C = np.array([0.03,0.06,0.02,-1.0]) #Flow coefficienct #can add mechanical here.
boolMech = N==0 #For mechanical N = 0 and C = flow rate.

E = 24. #External Temp
I = 27. #Internal Temp
U  = 0. #Wind Speed

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

Q = sum(F)
QT = sum(F[F>0])
print(T,O,S,R)

print("Balance",Q,"m3/s")
print("Flow rate",QT,"m3/s")
