
import math
import time 
import random 
import csv 

# ================================
#   Constrants 
# ================================

hv = 1.5 # height of the vehicle 
hr = 9.0 # height of the RSU

drr = 10.0 # distance from the road to RSU 
r = 200.0 # radio radious of rsu 
speed = 5.0 # meter per second 
dvr = 0 # radio distance of the vehicle to RSU
dvv = 0
t = 0 

# Results to csv 
header = ["time", "v2v_distance", "v2r_distance"]

def distance_v2v(s1, s2, t):
	# s1 and s2  = speed of the vehicles
	dvv = (s1 - s2) * 1
	return dvv 

def distance_v2r(speed, t):
	dvr = math.sqrt(drr**2 + (hr - hv)**2 + (r - speed * t)**2)
	return dvr 

# generate the speed of the vehicle using truncated gaussian distribution 
s1 = random.randint(5, 10)
s2 = 5.0
s0 = 5.0 # speed of the vehicle 

while True:
	print ("At time:", t)
	dvr = distance_v2r(s2, t)

	if (dvr > 210):
		print ("Out of the radio range")

	else:
		print ("Distance v2r: ", round(distance_v2r(s2, t)), "Speed of v1:", s1, "Speed v2:", s2)

	dvv = distance_v2v(s1, s2, t)
	print (" ")

	with open('results/distance.csv', 'a', encoding="UTF8", newline='') as f:
		writer = csv.writer(f)

		# write the data
		data = [t, dvr, dvv]
		writer.writerow(data)

	time.sleep(1)
	t = t + 1

	if (t == 120):
		break


