# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:49:51 2018

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

D = 1.2 #density of air
V = 250. #Building Volume
L =2 #Number of flow paths

TotalA = 9.25
Width = TotalA/2.
h1 = 1.45
#H = L*[0]
H = []
for i in range(L):
    H.append(h1 + (i+0.5)*TotalA/(L*Width))
print("Opening Heights: ", H)
H = [1,2.5]
H = np.array(H) #Height of opening
P = np.array(L*[0.0]) #Wind Pressure Coefficient
N = np.array(L*[0.5]) #Exponent
N[1] = 0
C = L*[1.0*TotalA/L*m.sqrt(2./D)] #pp. 225
openingCdA = np.array([0.5*7.4,0.5*37*0.25])
C = openingCdA*m.sqrt(2./D)
#C = np.array([0.03,0.06,0.02,-1.0]) #Flow coefficienct #can add mechanical here.
boolMech = N==0

E = 24. #External Temp
I = 29. #Internal Temp
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
X = 5. #Iteration pressure step
Y = 0 #Iteration counter
B = -1

F = np.zeros(L) #Calculated flow rate

print("no. Openings: ", L)
while((B<=0 or B/np.sum(abs(F))>0.01) and Y<20000):
    Y+=1
    B = 0 #Flow balance

    #print(Y)
    R = R+X
    #print(R)
    #print(X)
    T[boolMech] = R
    O = T - R #Pressure difference across each flow path.
    #print(O)
    divisor = abs(O)
    numerator = O
    numerator[divisor==0]=1
    divisor[divisor==0]=1
    F = np.nan_to_num(C*abs(O)**N*O/divisor)
    B = np.sum(F)

    #print(X)
    #print(B)
    if B<0:
        R = R-X
        X = X*0.99
        if Y%100==0: X = 100/Y
    else:
        pass

Q = sum(F)
QT = sum(F[F>0])
print("T,O,S,R: ", T,O,S,R)

print("Balance",Q,"m3/s")
print("Openings", F)
print("Flow rate",QT,"m3/s")
print("NPL", H[0] - (H[1]-H[0])*O[0]/(O[1]-O[0]))
    
    
    
    
    