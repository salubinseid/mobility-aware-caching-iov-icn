

import math
import time 

from math import log10, pi


# Given data 
Pt = 50 # Transmission power in watt
fc = 900.0 * 10 **6 # Carrier frequency in Hz

C = 3.0*10**8 # speed of light -- meter per second 

# Transmitter power in dbm 

Ptdbm = round(10*math.log10(Pt/(1*10**(-3)))) # Transmitter power in dbm 
print ("Transmitter power: dBm", Ptdbm, "dbm")


# Find the receiver power as reference ditance, let d0 = 5m 
Gt = 1.0 # Transmitter gain
Gr = 1.0 # Receiver gain 

d = 100.0 # Free space distance from antenna in m 

L = 1.0 
lamda = C/fc

Pr = (Pt*Gt*Gr*lamda**2) / ((4 * pi)**2*d**2*L) # Receiver power in W

PrdBm = 10*math.log10(Pr/(10**(-3))) # receiver power in dBm 
print ("Receiver power", PrdBm, "dBm")


d0 = 100.0
d = 10000.0 # free space distance from antenna 
n = 2.0 

Pr10km = PrdBm + 10 * n * math.log10(d0/d)

# print displaying the result 

print ("Receiver power at 10km from antenna", Pr10km, "dBm")




